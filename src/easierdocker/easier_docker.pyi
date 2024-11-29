import docker
from typing import Union
from docker.models.containers import Container
from docker import DockerClient


class EasierDocker:
    def __init__(self, container_config: dict, network_config=None) -> None:
        if network_config is None:
            network_config = {}

        self._container_config = container_config
        self._network_config = network_config
        self._client: DockerClient() = docker.from_env()
        """
            Initialize client, config, image name, container name
        """

    @property
    def container_config(self) -> dict:
        """
            Return the container config.
        """
        return self._container_config

    @property
    def network_config(self):
        """
            Return the network config.
        :return:
        """

    @property
    def image_name(self) -> str:
        """
            Return the image name.
        """
        return self._container_config['image']

    @property
    def container_name(self) -> str:
        """
            Return the container name.
        """
        return self._container_config['name']

    @property
    def client(self) -> DockerClient:
        """
            Return the client.
        """
        return self._client

    def __get_image(self) -> None:
        """
            Search for the image that exists locally. If it does not exist, the image will be pulled.
        :return:
        """
        ...

    def __get_container(self) -> Union[Container, None]:
        """
            Find and return the locally existing container.
        :return: obj of the container or None
        """
        ...

    def __run_container(self) -> None:
        """
            Start the found container. If the container does not exist, it will create one according to the image.
        :return:
        """
        ...

    def __get_all_networks(self) -> list:
        """
        :return: list, all already exits networks
        """
        ...

    def __create_network(self) -> None:
        """
            create and manage networks on the server.
        :return:
        """
        ...

    def start(self) -> None:
        """
            where to start.
        :return:
        """
        ...
