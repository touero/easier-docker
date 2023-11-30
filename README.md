<h1 align="center">easier-docker</h1>

<p align="center">
  <a href="https://www.python.org/" ><img src="https://img.shields.io/badge/python_-%3E%3D3.8-blue" alt=""></a> 
  <a href="https://opensource.org/license/mit/" ><img src="https://img.shields.io/badge/license_-MIT-blue" alt=""></a> 
  <a href="https://www.python.org/" ><img src="https://img.shields.io/badge/-python-grey?style=plastic&logo=python" alt=""/></a> 
  <a href="https://www.docker.com/"><img src="https://img.shields.io/badge/-docker-grey?style=plastic&logo=docker" alt=""/></a>
</p>


## Repository Introduction
This is based on [docker-py](https://github.com/docker/docker-py?tab=readme-ov-file) which makes it easier to run your program in docker.
It can create a container based on the local image. If the image does not exist, the image will be pulled down. 
If the container exists, it will be started directly. Then execute any service you want to execute in the container.


## Install
```bash
pip install easier-docker
```

## Usage
💡 Please check config parameters in [Docker SDK for Python](https://docker-py.readthedocs.io/en/stable/containers.html)

### Use examples in code
```bash
python example.py
```
```python
# example.py
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
                                'python docker_example.py'],
    }
    easier_docker = EasierDocker(config)
    easier_docker.start()
    """
    >>> 2023-11-27 14:40:29,264 - INFO - easier-docker ==> Find docker image: [python:3.9] locally...: 
    >>> 2023-11-27 14:40:29,280 - INFO - easier-docker ==> Image: [python:3.9] is found locally
    >>> 2023-11-27 14:40:29,280 - INFO - easier-docker ==> Find docker container: [python_test] locally...: 
    >>> 2023-11-27 14:40:29,284 - INFO - easier-docker ==> ContainerNotFound: [python_test], it will be created
    >>> 2023-11-27 14:40:29,558 - INFO - easier-docker ==> Container name: [python_test] is running
    >>> 2023-11-27 14:40:29,558 - INFO - easier-docker ==> Container id: [58509ced60ba] is running
    >>> 2023-11-27 14:40:29,559 - INFO - easier-docker ==> Successfully container is running and be created at 2023-11-27T06:40:29.291320745Z
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

### Run directly from configuration file
Currently supports yaml
```bash
easier-docker -c config.yaml
```
The content of config.yaml is
```yaml
# config.yaml
image: python:3.9
name: python_test
volumes:
  /Users/admin/data/code_project/easier-docker/tests:
    bind: /path/to/container
    mode: rw
detach: true
command:
  - sh
  - -c
  - cd /path/to/container && python docker_example.py

```


|                                                                                                        |
|--------------------------------------------------------------------------------------------------------|
| ![containers.png](https://github.com/weiensong/easier-docker/blob/master/image/containers.png)         |
| ![containers_log.png](https://github.com/weiensong/easier-docker/blob/master/image/containers_log.png) |


## Related Repository
- [docker-py](https://github.com/docker/docker-py) — A Python library for the Docker Engine API.


## Related Materials
- [Docker SDK for Python](https://docker-py.readthedocs.io/en/stable/)


## Related Uses Repository
- [opsariichthys-bidens](https://github.com/weiensong/opsariichthys-bidens) — About
Building a Basic Information API for Chinese National Universities in the Handheld College Entrance Examination Based on Fastapi.


## Maintainers
[@touero](https://github.com/touero)


## Contributing
How I wish I could add more content in this repo !
Feel free to dive in! [Open an issue](https://github.com/weiensong/easier_docker/issues) or submit PRs.
Standard Python follows the [Python PEP-8](https://peps.python.org/pep-0008/) Code of Conduct.


### Contributors
This project exists thanks to all the people who contribute.

<a href="https://github.com/weiensong/carp/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=weiensong/easier_docker"  alt=""/>
</a>


## License
[Apache License 2.0](https://github.com/weiensong/easier-docker/blob/master/LICENSE)

