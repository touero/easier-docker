import unittest
from datetime import datetime, timedelta
from unittest.mock import patch

from src.easierdocker.constants import ContainerStatus
from src.easierdocker.docker_utils import check_container_status, check_time


class FakeContainer:
    def __init__(self, status, reload_status=None, name="demo-container"):
        self.status = status
        self.reload_status = reload_status
        self.name = name
        self.reload_calls = 0

    def reload(self):
        self.reload_calls += 1
        if self.reload_status is not None:
            self.status = self.reload_status


class TestDockerUtils(unittest.TestCase):
    def test_check_container_status_created_then_running(self):
        container = FakeContainer(ContainerStatus.CREATED.name.lower())
        sleep_calls = {"count": 0}

        def fake_sleep(_):
            sleep_calls["count"] += 1
            if sleep_calls["count"] == 2:
                container.status = ContainerStatus.RUNNING.name.lower()

        with patch("src.easierdocker.docker_utils.time.sleep", side_effect=fake_sleep):
            result = check_container_status(container)

        self.assertEqual(result, ContainerStatus.RUNNING)

    def test_check_container_status_reload_then_running(self):
        container = FakeContainer("paused", reload_status=ContainerStatus.RUNNING.name.lower())

        with patch("src.easierdocker.docker_utils.time.sleep", return_value=None):
            result = check_container_status(container)

        self.assertEqual(result, ContainerStatus.RUNNING)
        self.assertEqual(container.reload_calls, 1)

    @patch("src.easierdocker.docker_utils.log")
    def test_check_container_status_exited(self, mock_log):
        container = FakeContainer(ContainerStatus.EXITED.name.lower())

        with patch("src.easierdocker.docker_utils.time.sleep", return_value=None):
            result = check_container_status(container)

        self.assertEqual(result, ContainerStatus.EXITED)
        mock_log.assert_called_once_with("Container name: [demo-container] is exited")

    def test_check_container_status_returns_none_when_status_never_stabilizes(self):
        container = FakeContainer("paused")

        with patch("src.easierdocker.docker_utils.time.sleep", return_value=None):
            result = check_container_status(container)

        self.assertIsNone(result)
        self.assertEqual(container.reload_calls, 1)

    def test_check_time_returns_true_for_old_container(self):
        target = (datetime.utcnow() - timedelta(days=5)).strftime("%Y-%m-%dT%H:%M:%S.%f123Z")

        self.assertTrue(check_time(target, 3))

    def test_check_time_returns_false_for_recent_container(self):
        target = (datetime.utcnow() - timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%S.%f123Z")

        self.assertFalse(check_time(target, 3))
