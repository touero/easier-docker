from typing import Union
from docker.models.containers import Container
from docker import DockerClient


class EasierDocker:
    _client: DockerClient

    def __init__(self, config: dict) -> None:
        self.config = config
        self.image_name = self.config['image']
        self.container_name = self.config['name']
        """
            Initialize client, config, image name, container name
        """

    def _get_image(self) -> None:
        """
            Search for the image that exists locally. If it does not exist, the image will be pulled.
        """
        ...

    def _get_container(self) -> Union[Container, None]:
        """
            Find and return the locally existing container.
        """
        ...

    def _run_container(self) -> None:
        """
            Start the found container. If the container does not exist, it will create one according to the image.
        """
        ...

    def start(self) -> None:
        """
            Start the portal.
        """
        ...
