import json
import docker

from typing import Union
from docker.errors import ImageNotFound
from docker.models.containers import Container


class EasierDocker:
    def __init__(self, config: dict):
        self._client = docker.from_env()
        self.config = config
        self.image_name = self.config['image']
        self.container_name = self.config['name']

    def _get_image(self):
        print(f'Finding {self.image_name} docker image in local')
        try:
            self._client.images.get(self.image_name)
        except ImageNotFound as e:
            print(f'ImageNotFound: {str(e)}')
            print(f'Waiting docker pull {self.image_name}')
            for event in self._client.api.pull(self.image_name, stream=True):
                event_info = json.loads(event.decode('utf-8'))
                if 'status' in event_info:
                    status = event_info['status']
                    progress = event_info.get('progress', '')
                    print(f'Status: {status}, Progress: {progress}')
            print(f'Docker pull {self.image_name} finish')
        except Exception as e:
            print(str(e))

    def _get_container(self) -> Union[Container, None]:
        print(f'find {self.container_name} docker container in local')
        containers = self._client.containers.list(all=True)
        for container in containers:
            if self.container_name == container.name:
                print(f'find docker container: {container.id}')
                return container
        print(f'ContainerNotFound: {self.container_name}')
        return None

    def _run_container(self):
        try:
            container = self._client.containers.run(**self.config)
            print(f'container id: {container.id} is running')
        except docker.errors.APIError as e:
            print(f'Error starting container: {e}')
        except Exception as e:
            print(f'An error occurred: {e}')

    def start(self):
        self._get_image()
        container = self._get_container()
        if container:
            container.start()
        else:
            self._run_container()
