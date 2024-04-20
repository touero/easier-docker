import os
import unittest

from easierdocker import EasierDocker


class TestEasierDocker(unittest.TestCase):
    def test_init_container_config(self):
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

        easier_docker = EasierDocker(container_config)
        self.assertEqual(easier_docker.image_name, 'python:3.9')
        self.assertEqual(easier_docker.container_name, 'python_test')
