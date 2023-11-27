import docker
import json
from .exceptions import DockerConnectionError
from .log_re import log

from typing import Union
from docker.errors import ImageNotFound, APIError, DockerException
from docker.models.containers import Container


class EasierDocker:
    def __init__(self, config: dict):
        try:
            self._client = docker.from_env()
        except Exception as e:
            if isinstance(e, DockerException):
                raise DockerConnectionError
            raise e
        self.config = config
        self.image_name = self.config['image']
        self.container_name = self.config['name']

    def _get_image(self):
        log(f'Find docker image: [{self.image_name}] locally...')
        try:
            self._client.images.get(self.image_name)
            log(f'Image: [{self.image_name}] is found locally')
        except Exception as e:
            if isinstance(e, ImageNotFound):
                log(f'ImageNotFound: {str(e)}, it will be pulled')
                log(f'Waiting docker pull {self.image_name}...')
                for event in self._client.api.pull(self.image_name, stream=True):
                    event_info = json.loads(event.decode('utf-8'))
                    if 'status' in event_info:
                        status = event_info['status']
                        progress = event_info.get('progress', '')
                        log(f'Status: {status}, Progress: {progress}')
                log(f'Docker pull {self.image_name} finish')
            else:
                log(str(e))

    def _get_container(self) -> Union[Container, None]:
        log(f'Find docker container: [{self.container_name}] locally...')
        containers = self._client.containers.list(all=True)
        for container in containers:
            if self.container_name == container.name:
                log(f'Container name: [{container.name}] is found locally')
                log(f'Container id: [{container.short_id}] is found locally')
                created_time = container.attrs['Created']
                log(f'Successfully container continue running and be created at {created_time}')
                return container
        log(f'ContainerNotFound: [{self.container_name}], it will be created')
        return None

    def _run_container(self):
        try:
            container: Container = self._client.containers.run(**self.config)
            log(f'Container name: [{container.name}] is running')
            log(f'Container id: [{container.short_id}] is running')
            created_time = container.attrs['Created']
            log(f'Successfully container is running and be created at {created_time}')
        except Exception as e:
            if isinstance(e, APIError):
                log(f'Error starting container: {str(e)}')
            else:
                log(f'An error occurred: {str(e)}')
            raise e

    def start(self):
        self._get_image()
        container = self._get_container()
        if container:
            container.start()
        else:
            self._run_container()
