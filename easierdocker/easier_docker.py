import json
import docker

from .log_re import log

from typing import Union
from docker.errors import ImageNotFound, APIError
from docker.models.containers import Container


class EasierDocker:
    def __init__(self, config: dict):
        self._client = docker.from_env()
        self.config = config
        self.image_name = self.config['image']
        self.container_name = self.config['name']

    def _get_image(self):
        log(f'Finding {self.image_name} docker image in local')
        try:
            self._client.images.get(self.image_name)
        except Exception as e:
            if isinstance(e, ImageNotFound):
                log(f'ImageNotFound: {str(e)}')
                log(f'Waiting docker pull {self.image_name}')
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
        log(f'Finding {self.container_name} docker container in local')
        containers = self._client.containers.list(all=True)
        for container in containers:
            if self.container_name == container.name:
                log(f'Finding docker container: {container.id}')
                return container
        log(f'ContainerNotFound: {self.container_name}')
        return None

    def _run_container(self):
        try:
            container: Container = self._client.containers.run(**self.config)
            log(f'Container name: {container.name} is running')
            log(f'Container id: {container.id} is running')
            log('Successfully started container')
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
