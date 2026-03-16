import importlib
import runpy
import sys
import unittest
from unittest.mock import MagicMock, patch

import src.easierdocker as easierdocker


class TestInitAndCli(unittest.TestCase):
    def test_package_exports(self):
        self.assertEqual(easierdocker.__version__, "2.2.6")
        self.assertTrue(callable(easierdocker.log))
        self.assertTrue(callable(easierdocker.EasierDocker))
        self.assertTrue(callable(easierdocker.Config))

    @patch("src.easierdocker.__main__.log")
    @patch("src.easierdocker.__main__.EasierDocker")
    @patch("src.easierdocker.__main__.Config")
    def test_main_loads_config_and_starts_docker(self, mock_config_cls, mock_easier_docker_cls, mock_log):
        main = importlib.import_module("src.easierdocker.__main__").main
        mock_config_cls.return_value.load_file.return_value = {
            "container": {"image": "demo", "name": "demo-container"},
            "network": {"name": "demo-network"},
            "extra": {"is_remove": 1, "days_ago_remove": 3, "remove_now": 0},
        }
        docker_instance = mock_easier_docker_cls.return_value

        with patch.object(sys, "argv", ["easier-docker", "--config", "example/config.yaml"]):
            main()

        mock_config_cls.assert_called_once()
        config_path = mock_config_cls.call_args.args[0]
        self.assertTrue(config_path.endswith("example/config.yaml"))
        mock_log.assert_called_once()
        mock_easier_docker_cls.assert_called_once_with(
            {"image": "demo", "name": "demo-container"},
            network_config={"name": "demo-network"},
            extra_config={"is_remove": 1, "days_ago_remove": 3, "remove_now": 0},
        )
        docker_instance.start.assert_called_once_with()

    @patch.object(easierdocker, "log")
    @patch.object(easierdocker, "EasierDocker")
    @patch.object(easierdocker, "Config")
    def test_module_entrypoint_runs_main(self, mock_config_cls, mock_easier_docker_cls, mock_log):
        mock_config_cls.return_value.load_file.return_value = {
            "container": {"image": "demo", "name": "demo-container"},
        }
        docker_instance = mock_easier_docker_cls.return_value

        sys.modules.pop("src.easierdocker.__main__", None)
        with patch.object(sys, "argv", ["easier-docker", "--config", "example/config.yaml"]):
            runpy.run_module("src.easierdocker.__main__", run_name="__main__")

        mock_config_cls.assert_called_once()
        mock_log.assert_called_once()
        mock_easier_docker_cls.assert_called_once_with(
            {"image": "demo", "name": "demo-container"},
            network_config={},
            extra_config={},
        )
        docker_instance.start.assert_called_once_with()
