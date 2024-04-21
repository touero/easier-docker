import os

import unittest
from unittest.mock import patch, MagicMock

from easierdocker import EasierDocker


class TestEasierDocker(unittest.TestCase):
    @patch('docker.from_env')
    def test_init(self, mock_from_env):
        parent_dir = os.path.dirname(os.getcwd())
        host_script = os.path.join(parent_dir, 'example')
        container_script = '/path/to/container'
        container_config = {
            'image': 'python:3.9',
            'name': 'python_test',
            'volumes': {
                f'{host_script}': {'bind': container_script, 'mode': 'rw'}
            },
            'detach': True,
            'command': ["sh", "-c", f'cd {container_script} &&'
                                    'python docker_example.py'],
        }

        network_config = {
            'name': 'bridge',
            'driver': 'bridge',
        }

        mock_client = MagicMock()
        mock_from_env.return_value = mock_client
        easier_docker = EasierDocker(container_config=container_config, network_config={})

        self.assertEqual(easier_docker._container_config, container_config)
        self.assertEqual(easier_docker._network_config, {})

        mock_from_env.assert_called_once()
        self.assertEqual(easier_docker._client, mock_client)

        easier_docker = EasierDocker(container_config=container_config, network_config=network_config)
        self.assertEqual(easier_docker._container_config, container_config)
        self.assertEqual(easier_docker._network_config, network_config)

    @patch('docker.from_env')
    def test_properties(self, mock_from_env):
        parent_dir = os.path.dirname(os.getcwd())
        host_script = os.path.join(parent_dir, 'example')
        container_script = '/path/to/container'
        container_config = {
            'image': 'python:3.9',
            'name': 'python_test',
            'volumes': {
                f'{host_script}': {'bind': container_script, 'mode': 'rw'}
            },
            'detach': True,
            'command': ["sh", "-c", f'cd {container_script} &&'
                                    'python docker_example.py'],
        }

        network_config = {
            'name': 'bridge',
            'driver': 'bridge',
        }
        mock_client = MagicMock()
        mock_from_env.return_value = mock_client
        easier_docker = EasierDocker(container_config=container_config, network_config=network_config)
        self.assertEqual(easier_docker.container_config, container_config)
        self.assertEqual(easier_docker.network_config, network_config)
        self.assertEqual(easier_docker.client, mock_client)
        self.assertEqual(easier_docker.image_name, container_config['image'])
        self.assertEqual(easier_docker.container_name, container_config['name'])
