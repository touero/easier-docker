import os

from easierdocker import EasierDocker

if __name__ == '__main__':
    parent_dir = os.getcwd()
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
    extra_config = {
        'is_remove': 1,
        'days_ago_remove': 3,
        'remove_now': 1
    }
    easier_docker = EasierDocker(container_config, network_config=network_config, extra_config=extra_config)
    easier_docker.start()
