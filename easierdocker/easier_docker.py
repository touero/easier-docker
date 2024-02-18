import docker
import json

from typing import Union
from docker.errors import ImageNotFound, APIError, DockerException, NotFound
from docker.models.containers import Container
from .exceptions import DockerConnectionError, NotFoundImageInDockerHub
from .log_re import log
from .constants import ContainerStatus
from .docker_utils import check_container


class EasierDocker:
    def __init__(self, container_config: dict, network_config=None):
        if network_config is None:
            network_config = {}

        self._container_config = container_config
        self._network_config = network_config

        try:
            self._client = docker.from_env()
        except Exception as e:
            if isinstance(e, DockerException):
                raise DockerConnectionError
            raise e

    @property
    def container_config(self):
        return self._container_config

    @property
    def network_config(self):
        return self._network_config

    @property
    def client(self):
        return self._client

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
                container.start()
                if check_container(container) is ContainerStatus.EXITED:
                    return container
                log(f'Container name: [{container.name}] is found locally')
                log(f'Container id: [{container.short_id}] is found locally')
                ip_address = container.attrs['NetworkSettings']['IPAddress']
                log(f'Container ip address: [{ip_address}]')
                created_time = container.attrs['Created']
                log(f'Successfully container continue running and be created at {created_time}')
                return container
        log(f'ContainerNotFound: [{self.container_name}], it will be created')
        return None

    def __run_container(self):
        try:
            container: Container = self._client.containers.run(**self.container_config)
            if check_container(container) is ContainerStatus.EXITED:
                return
            log(f'Container name: [{container.name}] is running')
            log(f'Container id: [{container.short_id}] is running')
            ip_address = container.attrs['NetworkSettings']['IPAddress']
            log(f'Container ip address: [{ip_address}]')
            created_time = container.attrs['Created']
            log(f'Successfully container is running and be created at {created_time}')
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
