import os

from easierdocker import EasierDocker

if __name__ == '__main__':
    host_script = os.path.dirname(os.path.abspath(__file__))
    container_script = '/path/to/container'
    config = {
        'image': 'python:3.9',
        'name': 'python_test',
        'volumes': {
            f'{host_script}': {'bind': container_script, 'mode': 'rw'}
        },
        'detach': True,
        'command': ["sh", "-c", f'cd {container_script} &&'
                                'python test_in_docker.py'],
    }
    easier_docker = EasierDocker(config)
    easier_docker.start()
