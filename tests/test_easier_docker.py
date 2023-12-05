import os
import unittest

from easierdocker import EasierDocker


class TestEasierDocker(unittest.TestCase):
    def test_init(self):
        parent_dir = os.path.dirname(os.getcwd())
        host_script = os.path.join(parent_dir, 'example')
        container_script = '/path/to/container'
        config = {
            'image': 'python:3.9',
            'name': 'python_test',
            'volumes': {
                f'{host_script}': {'bind': container_script, 'mode': 'rw'}
            },
            'detach': True,
            'command': ["sh", "-c", f'cd {container_script} &&'
                                    'python docker_example.py'],
        }
        test_config = {
                'image': 'python:3.9',
                'name': 'python_test',
                'volumes': {
                    '/Users/weiensong/data/code_project/easier-docker/example': {
                        'bind': container_script, 'mode': 'rw'
                    }
                },
                'detach': True,
                'command': ["sh", "-c", f'cd {container_script} &&'
                                        'python docker_example.py'],
            }
        easier_docker = EasierDocker(config)
        self.assertEqual(easier_docker.config, test_config)
        self.assertEqual(easier_docker.image_name, 'python:3.9')
        self.assertEqual(easier_docker.container_name, 'python_test')

    def test_get_image(self):
        ...

    def test_get_container(self):
        ...
