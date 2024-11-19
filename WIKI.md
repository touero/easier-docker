# Welcome to the eaiser-docker wiki!

## Install
It should be a package for your real environment.
```shell
pip install easier-docker
```

## Explain 
Two params it need now:
> [!Note]
> 1. __container_config__: Necessary, run and manage containers on the server. Run a container. By default, it will wait for the container to finish and return its logs, similar to `docker run`. 
> 2. __network_config__: Unnecessary, create and manage networks on the server. For more information about networks, see the [Engine documentation](https://docs.docker.com/network/). Create a network. Similar to the `docker network create`.


Two params config please check:
> [!Important]
> 1. __container_config__: [Docker SDK for Python with Container](https://docker-py.readthedocs.io/en/7.1.0/containers.html)
> 2. __network_config__: [Docker SDK for Python with Network](https://docker-py.readthedocs.io/en/7.1.0/networks.html)
## Usage
### Use examples in code
```bash
python example.py
```
```python
# example.py
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
        'command': ["sh", "-c", f'cd {container_script} && python docker_example.py'],
    }
    network_config = {
        'name': 'bridge',
        'driver': 'bridge',
    }
    easier_docker = EasierDocker(container_config, network_config)
    easier_docker.start()

    """
    >>> 2024-02-18 17:02:29,360 - INFO - easier-docker ==> Find docker image: [python:3.9] locally...
    >>> 2024-02-18 17:02:29,364 - INFO - easier-docker ==> Image: [python:3.9] is found locally
    >>> 2024-02-18 17:02:29,367 - INFO - easier-docker ==> Network id: [13c5a6cb0137], name: [host]
    >>> 2024-02-18 17:02:29,368 - INFO - easier-docker ==> Network id: [27d6b39aeef6], name: [none]
    >>> 2024-02-18 17:02:29,368 - INFO - easier-docker ==> Network id: [eb71aacede75], name: [bridge]
    >>> 2024-02-18 17:02:29,368 - INFO - easier-docker ==> Network: [bridge] is found locally...
    >>> 2024-02-18 17:02:29,368 - INFO - easier-docker ==> Find docker container: [python_test] locally...
    >>> 2024-02-18 17:02:29,370 - INFO - easier-docker ==> ContainerNotFound: [python_test], it will be created
    >>> 2024-02-18 17:02:31,744 - INFO - easier-docker ==> Container name: [python_test] is running
    >>> 2024-02-18 17:02:31,744 - INFO - easier-docker ==> Container id: [42f361ef636d] is running
    >>> 2024-02-18 17:02:31,744 - INFO - easier-docker ==> Container ip address: [172.17.0.2]
    >>> 2024-02-18 17:02:31,744 - INFO - easier-docker ==> Successfully container is running and be created at 2024-02-18T09:02:29.381861Z
    """
```
The content of docker_example.py is
```python
# docker_example.py
def main():
    import logging
    import time
    for i in range(1, 101):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        logging.info(f'sleep 30s, times:{i}')
        time.sleep(30)


if __name__ == '__main__':
    main()

```
As mentioned above, it can be executed without `network_config`.

### Run directly from configuration file
> [!Note]
> Currently supports type of file: _yml_, _yaml_, _json_

```bash
easier-docker -c config.yaml
```
The content of config.yaml is
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
    
    # >>> 2023-12-29 15:08:58,703 - INFO - easier-docker ==> config =
    # >>>  {
    # >>>     "image": "python:3.9",
    # >>>     "name": "python_test",
    # >>>     "volumes": {
    # >>>         "D:\\code-project\\EasierDocker\\example": {
    # >>>             "bind": "/path/to/container",
    # >>>             "mode": "rw"
    # >>>         }
    # >>>     },
    # >>>     "detach": true,
    # >>>     "command": [
    # >>>         "sh",
    # >>>         "-c",
    # >>>         "cd /path/to/container && python docker_example.py"
    # >>>     ]
    # >>>  }
    # >>> 2023-12-29 15:08:58,707 - INFO - easier-docker ==> Find docker image: [python:3.9] locally...
    # >>> 2023-12-29 15:08:58,724 - INFO - easier-docker ==> Image: [python:3.9] is found locally
    # >>> 2023-12-29 15:08:58,725 - INFO - easier-docker ==> Find docker container: [python_test] locally...
    # >>> 2023-12-29 15:08:58,730 - INFO - easier-docker ==> ContainerNotFound: [python_test], it will be created
    # >>> 2023-12-29 15:09:00,989 - INFO - easier-docker ==> Container name: [python_test] is running
    # >>> 2023-12-29 15:09:00,990 - INFO - easier-docker ==> Container id: [a9b642f2ddf3] is running
    # >>> 2023-12-29 15:09:00,990 - INFO - easier-docker ==> Container ip address: [172.17.0.2]
    # >>> 2023-12-29 15:09:00,991 - INFO - easier-docker ==> Successfully container is running and be created at 2023-12-29T07:08:58.738605891Z

```
|                                                                                                      |
|------------------------------------------------------------------------------------------------------|
| ![container.png](https://github.com/weiensong/easier-docker/blob/master/image/container.png)         |
| ![container_log.png](https://github.com/weiensong/easier-docker/blob/master/image/container_log.png) |

