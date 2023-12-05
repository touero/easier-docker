import os

from easierdocker import EasierDocker

if __name__ == '__main__':
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
    easier_docker = EasierDocker(config)
    easier_docker.start()
