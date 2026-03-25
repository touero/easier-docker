import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import yaml

from src.easierdocker.config import Config


class TestConfig(unittest.TestCase):
    def test_load_yaml_file(self):
        expected = {"container": {"image": "demo", "name": "demo-container"}}
        with tempfile.TemporaryDirectory() as tmp_dir:
            path = Path(tmp_dir) / "config.yaml"
            path.write_text(yaml.safe_dump(expected), encoding="utf8")

            self.assertEqual(Config(str(path)).load_file(), expected)

    def test_load_json_file(self):
        expected = {"network": {"name": "demo-network"}}
        with tempfile.TemporaryDirectory() as tmp_dir:
            path = Path(tmp_dir) / "config.json"
            path.write_text(json.dumps(expected), encoding="utf8")

            self.assertEqual(Config(str(path)).load_file(), expected)

    @patch("src.easierdocker.config.log")
    def test_load_unsupported_file_type(self, mock_log):
        with tempfile.TemporaryDirectory() as tmp_dir:
            path = Path(tmp_dir) / "config.txt"
            path.write_text("unsupported", encoding="utf8")

            self.assertEqual(Config(str(path)).load_file(), {})
            mock_log.assert_called_once_with(f"Currently unsupported file types: {path}")
