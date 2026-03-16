import unittest
from unittest.mock import MagicMock, PropertyMock, patch

from docker.errors import APIError, DockerException, ImageNotFound, NotFound

from src.easierdocker.constants import ContainerStatus
from src.easierdocker.easier_docker import EasierDocker
from src.easierdocker.exceptions import DockerConnectionError, NotFoundImageInDockerHub


class TestEasierDocker(unittest.TestCase):
    def setUp(self):
        self.container_config = {
            "image": "test_image",
            "name": "test_container",
            "detach": True,
        }
        self.network_config = {"name": "test_network"}

    def build_docker(self, *, container_config=None, network_config=None, extra_config=None):
        client = MagicMock()
        with patch("src.easierdocker.easier_docker.docker.from_env", return_value=client):
            easier_docker = EasierDocker(
                container_config or dict(self.container_config),
                network_config=network_config if network_config is not None else dict(self.network_config),
                extra_config=extra_config if extra_config is not None else {},
            )
        return easier_docker, client

    def test_init_raises_custom_connection_error(self):
        with patch(
            "src.easierdocker.easier_docker.docker.from_env",
            side_effect=DockerException("Docker connection failed"),
        ):
            with self.assertRaises(DockerConnectionError):
                EasierDocker(self.container_config)

    def test_init_and_properties(self):
        easier_docker, client = self.build_docker(extra_config={"is_remove": 1, "days_ago_remove": 3, "remove_now": 0})
        client.containers.get.return_value.status = "running"

        self.assertEqual(easier_docker.container_config["image"], "test_image")
        self.assertEqual(easier_docker.network_config["name"], "test_network")
        self.assertEqual(easier_docker.extra_config["is_remove"], 1)
        self.assertIs(easier_docker.client, client)
        self.assertEqual(easier_docker.image_name, "test_image")
        self.assertEqual(easier_docker.container_name, "test_container")
        self.assertEqual(easier_docker.get_container_status, "running")
        client.containers.get.assert_called_once_with("test_container")

    def test_get_image_found_locally(self):
        easier_docker, client = self.build_docker()

        easier_docker._EasierDocker__get_image()

        client.images.get.assert_called_once_with("test_image")

    def test_get_image_pulls_when_missing(self):
        easier_docker, client = self.build_docker()
        client.images.get.side_effect = ImageNotFound("Image missing")
        client.api.pull.return_value = [
            b'{"id": "layer-1"}',
            b'{"status": "Pulling", "progress": "50%"}',
            b'{"status": "Complete"}',
        ]

        easier_docker._EasierDocker__get_image()

        client.api.pull.assert_called_once_with("test_image", stream=True)

    def test_get_image_raises_when_not_in_docker_hub(self):
        easier_docker, client = self.build_docker()
        client.images.get.side_effect = ImageNotFound("Image missing")
        client.api.pull.side_effect = NotFound("Image not in Docker Hub")

        with self.assertRaises(NotFoundImageInDockerHub):
            easier_docker._EasierDocker__get_image()

    @patch("src.easierdocker.easier_docker.log")
    def test_get_image_logs_non_image_not_found_errors(self, mock_log):
        easier_docker, client = self.build_docker()
        client.images.get.side_effect = RuntimeError("boom")

        easier_docker._EasierDocker__get_image()

        mock_log.assert_any_call("boom")

    @patch("src.easierdocker.easier_docker.check_container_status", return_value=ContainerStatus.EXITED)
    def test_get_container_returns_existing_container_when_status_exited(self, mock_check_status):
        easier_docker, client = self.build_docker()
        container = MagicMock()
        container.name = "test_container"
        container.short_id = "abc123"
        container.status = ContainerStatus.RUNNING.name.lower()
        container.attrs = {
            "Created": "2024-01-01T12:00:00.123456789Z",
            "NetworkSettings": {"IPAddress": "127.0.0.1"},
        }
        client.containers.list.return_value = [container]

        result = easier_docker._EasierDocker__get_container()

        self.assertIs(result, container)
        container.start.assert_called_once_with()
        mock_check_status.assert_called_once_with(container)

    @patch("src.easierdocker.easier_docker.check_container_status", return_value=ContainerStatus.RUNNING)
    @patch("src.easierdocker.easier_docker.log")
    def test_get_container_returns_existing_container_when_running(self, mock_log, mock_check_status):
        easier_docker, client = self.build_docker()
        other_container = MagicMock()
        other_container.name = "other_container"
        container = MagicMock()
        container.name = "test_container"
        container.short_id = "abc123"
        container.status = ContainerStatus.RUNNING.name.lower()
        container.attrs = {
            "Created": "2024-01-01T12:00:00.123456789Z",
            "NetworkSettings": {"IPAddress": "127.0.0.1"},
        }
        client.containers.list.return_value = [other_container, container]

        result = easier_docker._EasierDocker__get_container()

        self.assertIs(result, container)
        container.start.assert_called_once_with()
        mock_check_status.assert_called_once_with(container)
        self.assertIn("ip address: [127.0.0.1]", mock_log.call_args_list[-1].args[0])

    def test_get_container_returns_none_when_missing(self):
        easier_docker, client = self.build_docker()
        client.containers.list.return_value = []

        self.assertIsNone(easier_docker._EasierDocker__get_container())

    @patch("src.easierdocker.easier_docker.check_time", return_value=True)
    def test_get_container_removes_old_running_container(self, mock_check_time):
        easier_docker, client = self.build_docker(
            extra_config={"is_remove": 1, "days_ago_remove": 3, "remove_now": 0}
        )
        container = MagicMock()
        container.name = "test_container"
        container.status = ContainerStatus.RUNNING.name.lower()
        container.attrs = {
            "Created": "2024-01-01T12:00:00.123456789Z",
            "NetworkSettings": {"IPAddress": "127.0.0.1"},
        }
        client.containers.list.return_value = [container]

        with patch.object(easier_docker, "_EasierDocker__wait_container_status", return_value=True) as mock_wait:
            result = easier_docker._EasierDocker__get_container()

        self.assertIsNone(result)
        mock_check_time.assert_called_once_with("2024-01-01T12:00:00.123456789Z", 3)
        container.stop.assert_called_once_with()
        mock_wait.assert_called_once_with(ContainerStatus.EXITED)
        container.remove.assert_called_once_with()

    @patch("src.easierdocker.easier_docker.check_time", return_value=False)
    @patch("src.easierdocker.easier_docker.check_container_status", return_value=ContainerStatus.RUNNING)
    def test_get_container_keeps_existing_container_when_remove_conditions_not_met(
        self, mock_check_status, mock_check_time
    ):
        easier_docker, client = self.build_docker(
            extra_config={"is_remove": 1, "days_ago_remove": 3, "remove_now": 0}
        )
        container = MagicMock()
        container.name = "test_container"
        container.short_id = "abc123"
        container.status = ContainerStatus.EXITED.name.lower()
        container.attrs = {
            "Created": "2024-01-01T12:00:00.123456789Z",
            "NetworkSettings": {"IPAddress": "127.0.0.1"},
        }
        client.containers.list.return_value = [container]

        result = easier_docker._EasierDocker__get_container()

        self.assertIs(result, container)
        mock_check_time.assert_called_once_with("2024-01-01T12:00:00.123456789Z", 3)
        container.stop.assert_not_called()
        container.remove.assert_not_called()
        mock_check_status.assert_called_once_with(container)

    @patch("src.easierdocker.easier_docker.check_time", return_value=True)
    def test_get_container_returns_none_when_wait_for_exit_fails(self, mock_check_time):
        easier_docker, client = self.build_docker(
            extra_config={"is_remove": 1, "days_ago_remove": 3, "remove_now": 0}
        )
        container = MagicMock()
        container.name = "test_container"
        container.status = ContainerStatus.EXITED.name.lower()
        container.attrs = {
            "Created": "2024-01-01T12:00:00.123456789Z",
            "NetworkSettings": {"IPAddress": "127.0.0.1"},
        }
        client.containers.list.return_value = [container]

        with patch.object(easier_docker, "_EasierDocker__wait_container_status", return_value=False) as mock_wait:
            result = easier_docker._EasierDocker__get_container()

        self.assertIsNone(result)
        mock_check_time.assert_called_once_with("2024-01-01T12:00:00.123456789Z", 3)
        container.stop.assert_not_called()
        mock_wait.assert_called_once_with(ContainerStatus.EXITED)
        container.remove.assert_not_called()

    def test_wait_container_status_returns_true(self):
        easier_docker, _ = self.build_docker()

        with patch.object(
            EasierDocker,
            "get_container_status",
            new_callable=PropertyMock,
            side_effect=["created", "created", "exited"],
        ):
            with patch("src.easierdocker.easier_docker.time.sleep", return_value=None):
                self.assertTrue(easier_docker._EasierDocker__wait_container_status(ContainerStatus.EXITED))

    def test_wait_container_status_returns_false(self):
        easier_docker, _ = self.build_docker()

        with patch.object(
            EasierDocker,
            "get_container_status",
            new_callable=PropertyMock,
            side_effect=["running"] * 61,
        ):
            with patch("src.easierdocker.easier_docker.time.sleep", return_value=None):
                self.assertFalse(easier_docker._EasierDocker__wait_container_status(ContainerStatus.EXITED))

    @patch("src.easierdocker.easier_docker.check_container_status", return_value=ContainerStatus.RUNNING)
    @patch("src.easierdocker.easier_docker.log")
    def test_run_container_logs_success(self, mock_log, mock_check_status):
        easier_docker, client = self.build_docker()
        container = MagicMock()
        container.name = "test_container"
        container.short_id = "abc123"
        container.attrs = {
            "Created": "2024-01-01T12:00:00.123456789Z",
            "NetworkSettings": {"IPAddress": "127.0.0.1"},
        }
        client.containers.run.return_value = container

        easier_docker._EasierDocker__run_container()

        client.containers.run.assert_called_once_with(**self.container_config)
        mock_check_status.assert_called_once_with(container)
        self.assertIn(
            "Successfully container name: [test_container] is running",
            mock_log.call_args_list[-1].args[0],
        )

    @patch("src.easierdocker.easier_docker.check_container_status", return_value=ContainerStatus.EXITED)
    def test_run_container_returns_early_when_container_exited(self, mock_check_status):
        easier_docker, client = self.build_docker()
        container = MagicMock()
        client.containers.run.return_value = container

        self.assertIsNone(easier_docker._EasierDocker__run_container())
        mock_check_status.assert_called_once_with(container)

    @patch("src.easierdocker.easier_docker.log")
    def test_run_container_raises_api_error(self, mock_log):
        easier_docker, client = self.build_docker()
        client.containers.run.side_effect = APIError("API Error")

        with self.assertRaises(APIError):
            easier_docker._EasierDocker__run_container()

        mock_log.assert_any_call("Error starting container: API Error")

    @patch("src.easierdocker.easier_docker.log")
    def test_run_container_raises_unexpected_error(self, mock_log):
        easier_docker, client = self.build_docker()
        client.containers.run.side_effect = RuntimeError("boom")

        with self.assertRaisesRegex(RuntimeError, "boom"):
            easier_docker._EasierDocker__run_container()

        mock_log.assert_any_call("An error occurred: boom")

    @patch("src.easierdocker.easier_docker.log")
    def test_get_all_networks_returns_networks(self, mock_log):
        easier_docker, client = self.build_docker()
        network = MagicMock()
        network.short_id = "net123"
        network.name = "test_network"
        client.networks.list.return_value = [network]

        result = easier_docker._EasierDocker__get_all_networks()

        self.assertEqual(result, [network])
        mock_log.assert_called_once_with("Network id: [net123], name: [test_network]")

    def test_create_network_returns_when_name_missing(self):
        easier_docker, client = self.build_docker(network_config={})

        self.assertIsNone(easier_docker._EasierDocker__create_network())
        client.networks.list.assert_not_called()
        self.assertNotIn("network", easier_docker.container_config)

    def test_create_network_uses_existing_network(self):
        easier_docker, client = self.build_docker()
        first_network = MagicMock()
        first_network.name = "other_network"
        network = MagicMock()
        network.name = "test_network"
        client.networks.list.return_value = [first_network, network]

        easier_docker._EasierDocker__create_network()

        client.networks.create.assert_not_called()
        self.assertEqual(easier_docker.container_config["network"], "test_network")

    def test_create_network_creates_new_network(self):
        easier_docker, client = self.build_docker()
        client.networks.list.return_value = []

        easier_docker._EasierDocker__create_network()

        client.networks.create.assert_called_once_with(**self.network_config)
        self.assertEqual(easier_docker.container_config["network"], "test_network")

    def test_container_execute_command_uses_explicit_container_name(self):
        easier_docker, client = self.build_docker()
        exec_result = MagicMock()
        exec_result.exit_code = 0
        exec_result.output = b"done"
        client.containers.get.return_value.exec_run.return_value = exec_result

        result = easier_docker.container_execute_command("custom-container", "echo hi")

        self.assertEqual(result, "exit_code: 0, standard output: done")
        client.containers.get.assert_called_once_with("custom-container")
        client.containers.get.return_value.exec_run.assert_called_once_with("echo hi")

    def test_container_execute_command_falls_back_to_default_container_name(self):
        easier_docker, client = self.build_docker()
        exec_result = MagicMock()
        exec_result.exit_code = 1
        exec_result.output = b"failed"
        client.containers.get.return_value.exec_run.return_value = exec_result

        result = easier_docker.container_execute_command("", "echo hi")

        self.assertEqual(result, "exit_code: 1, standard output: failed")
        client.containers.get.assert_called_once_with("test_container")

    def test_start_runs_container_when_missing(self):
        easier_docker, _ = self.build_docker()

        with patch.object(easier_docker, "_EasierDocker__get_image") as mock_get_image, \
                patch.object(easier_docker, "_EasierDocker__create_network") as mock_create_network, \
                patch.object(easier_docker, "_EasierDocker__get_container", return_value=None) as mock_get_container, \
                patch.object(easier_docker, "_EasierDocker__run_container") as mock_run_container:
            easier_docker.start()

        mock_get_image.assert_called_once_with()
        mock_create_network.assert_called_once_with()
        mock_get_container.assert_called_once_with()
        mock_run_container.assert_called_once_with()

    def test_start_skips_run_when_container_exists(self):
        easier_docker, _ = self.build_docker()
        existing_container = MagicMock()

        with patch.object(easier_docker, "_EasierDocker__get_image") as mock_get_image, \
                patch.object(easier_docker, "_EasierDocker__create_network") as mock_create_network, \
                patch.object(
                    easier_docker,
                    "_EasierDocker__get_container",
                    return_value=existing_container,
                ) as mock_get_container, \
                patch.object(easier_docker, "_EasierDocker__run_container") as mock_run_container:
            easier_docker.start()

        mock_get_image.assert_called_once_with()
        mock_create_network.assert_called_once_with()
        mock_get_container.assert_called_once_with()
        mock_run_container.assert_not_called()
