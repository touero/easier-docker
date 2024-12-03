import docker
from typing import Union
from docker.models.containers import Container
from docker import DockerClient


class EasierDocker:
    def __init__(self, container_config: dict, **kwargs) -> None:
        self._container_config: dict = container_config
        self._network_config: dict = kwargs.get('network_config', {})
        self._extra_config: dict = kwargs.get('extra_config', {})

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
        """
        return self._network_config

    @property
    def extra_config(self):
        """
            Return the extra config.
        """
        return self._extra_config

    @property
    def client(self) -> DockerClient:
        """
            Return the client.
        """
        return self._client

    @property
    def get_container_status(self) -> str:
        """
            Return the status of the container.
        """
        ...

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

    def __wait_container_status(self, status: str) -> bool:
        """
            Wait for the container to reach a certain status.
        :param status: str, current status of the container
        :return: boolean.
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
