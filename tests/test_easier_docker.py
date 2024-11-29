import unittest
from unittest.mock import patch, MagicMock

from src.easierdocker import EasierDocker
from docker.errors import ImageNotFound, APIError, NotFound, DockerException
from src.easierdocker.exceptions import DockerConnectionError, NotFoundImageInDockerHub


class TestEasierDocker(unittest.TestCase):
    def setUp(self):
        self.container_config = {
            "image": "test_image",
            "name": "test_container",
            "detach": True
        }
        self.network_config = {"name": "test_network"}
        self.easier_docker = EasierDocker(self.container_config, self.network_config)

    @patch("docker.from_env")
    def test_docker_connection_error(self, mock_from_env):
        mock_from_env.side_effect = DockerException("Docker connection failed")
        with self.assertRaises(DockerConnectionError):
            EasierDocker(container_config={}, network_config={})

    @patch("docker.from_env")
    def test_init_success(self, mock_from_env):
        client_mock = MagicMock()
        mock_from_env.return_value = client_mock
        docker_instance = EasierDocker(self.container_config)
        self.assertIsNotNone(docker_instance.client)

    @patch("docker.from_env", side_effect=DockerConnectionError("Docker connection failed"))
    def test_init_failure(self, mock_from_env):
        with self.assertRaises(DockerConnectionError):
            EasierDocker(self.container_config)

    @patch("docker.models.images.ImageCollection.get")
    def test_get_image_found_locally(self, mock_image_get):
        self.easier_docker._EasierDocker__get_image()
        mock_image_get.assert_called_once_with("test_image")

    @patch("docker.models.images.ImageCollection.get", side_effect=ImageNotFound("Image not found"))
    @patch("docker.api.APIClient.pull", return_value=[
        '{"status": "Pulling", "progress": "50%"}'.encode("utf-8"),
        '{"status": "Complete"}'.encode("utf-8")
    ])
    def test_get_image_pull_success(self, mock_pull, mock_image_get):
        self.easier_docker._EasierDocker__get_image()
        mock_pull.assert_called_once_with("test_image", stream=True)

    @patch("docker.models.images.ImageCollection.get", side_effect=ImageNotFound("Image not found"))
    @patch("docker.api.APIClient.pull", side_effect=NotFound("Image not in Docker Hub"))
    def test_get_image_pull_failure(self, mock_pull, mock_image_get):
        with self.assertRaises(NotFoundImageInDockerHub):
            self.easier_docker._EasierDocker__get_image()

    @patch("docker.models.containers.ContainerCollection.list", return_value=[])
    @patch("docker.models.containers.ContainerCollection.run")
    def test_run_container_success(self, mock_run, mock_list):
        container_mock = MagicMock()
        container_mock.attrs = {"NetworkSettings": {"IPAddress": "127.0.0.1"}, "Created": "now"}
        container_mock.name = "test_container"
        container_mock.short_id = "12345"
        mock_run.return_value = container_mock

        self.easier_docker._EasierDocker__run_container()
        mock_run.assert_called_once_with(**self.container_config)

    @patch("docker.models.containers.ContainerCollection.list", return_value=[])
    @patch("docker.models.containers.ContainerCollection.run", side_effect=APIError("API Error"))
    def test_run_container_failure(self, mock_run, mock_list):
        with self.assertRaises(APIError):
            self.easier_docker._EasierDocker__run_container()

    @patch("docker.models.containers.ContainerCollection.list", return_value=[MagicMock()])
    def test_get_container_found(self, mock_list):
        container_mock = mock_list.return_value[0]
        container_mock.name = "test_container"
        container_mock.attrs = {"NetworkSettings": {"IPAddress": "127.0.0.1"}, "Created": "now"}
        container_mock.start = MagicMock()

        container = self.easier_docker._EasierDocker__get_container()
        self.assertEqual(container_mock, container)
        container_mock.start.assert_called_once()

    @patch("docker.models.containers.ContainerCollection.list", return_value=[])
    def test_get_container_not_found(self, mock_list):
        container = self.easier_docker._EasierDocker__get_container()
        self.assertIsNone(container)

    @patch("docker.models.networks.NetworkCollection.list", return_value=[])
    @patch("docker.models.networks.NetworkCollection.create")
    def test_create_network(self, mock_create, mock_list):
        self.easier_docker._EasierDocker__create_network()
        mock_create.assert_called_once_with(**self.network_config)

    @patch("docker.client.DockerClient.networks", new_callable=MagicMock)
    def test_create_network_exists(self, mock_networks):
        mock_network = MagicMock(name="test_network", short_id="short_id_1")
        mock_networks.list.return_value = [mock_network]
        self.easier_docker._EasierDocker__create_network()
        mock_networks.list.assert_called_once()
