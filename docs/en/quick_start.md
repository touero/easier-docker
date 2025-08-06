# Quick Start

## CLI Quick Start
```shell
easier-docker -c config.yaml
```

[`config.yaml`](https://github.com/touero/easier-docker/blob/master/example/config.yaml) is a simple example configuration file with content is:
```yaml
# config.yaml

container:
  image: python:3.9
  name: python_test
  volumes:
    D:\code-project\EasierDocker\example:
      bind: /path/to/container
      mode: rw
  detach: true
  command:
    - sh
    - -c
    - cd /path/to/container && python docker_example.py

network:
  name: bridge
  driver: bridge

extra:
  'is_remove': 1
  'days_ago_remove': 7
  'remove_now': 0

```


## Python API Quick Start
```python
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
```

## Result
This will start a docker container named python_test, inside the container will execute [`docker_example.py`](https://github.com/touero/easier-docker/blob/master/example/docker_example.py)
