import docker
import json
import time

from typing import Union
from docker.errors import ImageNotFound, APIError, DockerException, NotFound
from docker.models.containers import Container
from .exceptions import DockerConnectionError, NotFoundImageInDockerHub
from .log_re import log
from .constants import ContainerStatus, ExtraConfigModel
from .docker_utils import check_container_status, check_time


class EasierDocker:
    def __init__(self, container_config: dict, **kwargs):
        self._container_config: dict = container_config
        self._network_config: dict = kwargs.get('network_config', {})
        self._extra_config: dict = kwargs.get('extra_config', {})
        ExtraConfigModel.validate_dict(self._extra_config)

        try:
            self._client = docker.from_env()
        except DockerException:
            raise DockerConnectionError

    @property
    def container_config(self):
        return self._container_config

    @property
    def network_config(self):
        return self._network_config

    @property
    def extra_config(self):
        return self._extra_config

    @property
    def client(self):
        return self._client

    @property
    def get_container_status(self):
        return self.client.containers.get(self.container_name).status

    @property
    def image_name(self):
        return self._container_config['image']

    @property
    def container_name(self):
        return self._container_config['name']

    def __get_image(self):
        log(f'Find docker image: [{self.image_name}] locally...')
        try:
            self._client.images.get(self.image_name)
            log(f'Image: [{self.image_name}] is found locally')
        except Exception as e:
            if isinstance(e, ImageNotFound):
                log(f'ImageNotFound: {str(e)}, it will be pulled')
                log(f'Waiting docker pull {self.image_name}...')
                try:
                    for event in self._client.api.pull(self.image_name, stream=True):
                        event_info = json.loads(event.decode('utf-8'))
                        if 'status' in event_info:
                            status = event_info['status']
                            progress = event_info.get('progress', '')
                            log(f'Status: {status}, Progress: {progress}')
                except NotFound:
                    raise NotFoundImageInDockerHub(self.image_name)
                log(f'Docker pull {self.image_name} finish')
            else:
                log(str(e))

    def __get_container(self) -> Union[Container, None]:
        log(f'Find docker container: [{self.container_name}] locally...')
        containers = self._client.containers.list(all=True)
        for container in containers:
            if self.container_name == container.name:
                created_time = container.attrs['Created']
                log(f'Container name: [{container.name}] is found locally')
                if self.extra_config.get('is_remove', 0):
                    if (check_time(created_time, self.extra_config.get('days_ago_remove', 3)) or
                            self.extra_config.get('remove_now', 0)):
                        log(f'Container: [{container.name}] is created {self.extra_config.get("days_ago_remove", 3)} '
                            f'days ago or remove_now is {self.extra_config.get("remove_now", 0)}, '
                            f'it will be removed...')
                        if container.status == ContainerStatus.RUNNING.name.lower():
                            log(f'Stopping container: [{container.name}]')
                            container.stop()
                        if self.__wait_container_status(ContainerStatus.EXITED):
                            log(f'Removing container: [{container.name}]')
                            container.remove()
                        return None
                container.start()
                ip_address = container.attrs['NetworkSettings']['IPAddress']
                if check_container_status(container) is ContainerStatus.EXITED:
                    return container
                log(f'Container name: [{container.name}] is found locally, id: [{container.short_id}], '
                    f'ip address: [{ip_address}], created time: [{created_time}]')
                return container
        log(f'ContainerNotFound: [{self.container_name}], it will be created')
        return None

    def __wait_container_status(self, status: ContainerStatus) -> bool:
        container_status = self.get_container_status
        for _ in range(60):
            container_status = self.get_container_status
            log(f'Waiting for container [{container_status}] to be [{status.name.lower()}]')
            if container_status != status.name.lower():
                time.sleep(1)
                continue
            break

        if container_status == status.name.lower():
            return True
        else:
            return False

    def __run_container(self):
        try:
            container: Container = self._client.containers.run(**self.container_config)
            if check_container_status(container) is ContainerStatus.EXITED:
                return
            ip_address = container.attrs['NetworkSettings']['IPAddress']
            created_time = container.attrs['Created']
            log(f'Successfully container name: [{container.name}] is running, id: [{container.short_id}], '
                f'ip address: [{ip_address}], created time: [{created_time}]')
        except Exception as e:
            if isinstance(e, APIError):
                log(f'Error starting container: {str(e)}')
            else:
                log(f'An error occurred: {str(e)}')
            raise e

    def __get_all_networks(self) -> list:
        networks = self._client.networks.list()
        for network in networks:
            log(f'Network id: [{network.short_id}], name: [{network.name}]')
        return networks

    def __create_network(self) -> None:
        if not self._network_config.get('name'):
            return
        network_name = self._network_config['name']
        networks = self.__get_all_networks()
        for network in networks:
            if network.name == network_name:
                log(f'Network: [{network_name}] is found locally...')
                self._container_config['network'] = network_name
                return
        log(f'Network: [{network_name}] is not found locally, it will be created')
        self._client.networks.create(**self.network_config)
        log(f'Network: [{network_name}] is created')
        self._container_config['network'] = network_name

    def start(self):
        self.__get_image()
        self.__create_network()
        container = self.__get_container()
        if container is None:
            self.__run_container()
