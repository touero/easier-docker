import docker
from typing import Union
from docker.models.containers import Container
from docker import DockerClient


class EasierDocker:
    def __init__(self, config: dict) -> None:
        self._config = config
        self._image_name = self._config['image']
        self._container_name = self._config['name']
        self._client: DockerClient() = docker.from_env()
        """
            Initialize client, config, image name, container name
        """

    @property
    def config(self) -> dict:
        """
            Return the config.
        """
        return self._config

    @property
    def image_name(self) -> str:
        """
            Return the image name.
        """
        return self._image_name

    @property
    def container_name(self) -> str:
        """
            Return the container name.
        """
        return self._container_name

    @property
    def client(self) -> DockerClient:
        """
            Return the client.
        """
        return self._client

    def __get_image(self) -> None:
        """
            Search for the image that exists locally. If it does not exist, the image will be pulled.
        """
        ...

    def __get_container(self) -> Union[Container, None]:
        """
            Find and return the locally existing container.
        """
        ...

    def __run_container(self) -> None:
        """
            Start the found container. If the container does not exist, it will create one according to the image.
        """
        ...

    def start(self) -> None:
        """
            Start the portal.
        """
        ...
