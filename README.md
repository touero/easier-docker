<h1 align="center">easier-docker</h1>

<p align="center">
  <a href="https://www.python.org/" ><img src="https://img.shields.io/badge/python_-%3E%3D3.8-blue" alt=""></a> 
  <a href="https://opensource.org/license/mit/" ><img src="https://img.shields.io/badge/license_-MIT-blue" alt=""></a> 
  <a href="https://www.python.org/" ><img src="https://img.shields.io/badge/-python-grey?style=plastic&logo=python" alt=""/></a> 
  <a href="https://www.docker.com/"><img src="https://img.shields.io/badge/-docker-grey?style=plastic&logo=docker" alt=""/></a>
</p>


## Repository Introduction

It can create a container based on the local image. If the image does not exist, the image will be pulled down. 
If the container exists, it will be started directly. Then execute any service you want to execute in the container.


## Install
```bash
pip install easier-docker
```

## Usage
💡 Please check config parameters in [Docker SDK for Python](https://docker-py.readthedocs.io/en/stable/containers.html)

### Use examples in code
Run the example.py
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
    >>> Finding python:3.9 docker image in local
    >>> Finding python_test docker container in local
    >>> ContainerNotFound: python_test
    >>> container id: d9233f82e9a17627d51d294091b43295fdcf3e2fae204f2d8e2bb7080b88c0b0 is running
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


<div align="center">
  <img src="https://github.com/weiensong/easier-docker/blob/master/image/containers.png" alt="containers" style="max-width:400px; max-height:300px;" />
</div>

<div align="center">
  <img src="https://github.com/weiensong/easier-docker/blob/master/image/containers_log.png" alt="containers log" style="max-width:400px; max-height:300px;" />
</div>



## Related Repository
- [docker-py](https://github.com/docker/docker-py) — A Python library for the Docker Engine API.


## Related Materials
- [Docker SDK for Python](https://docker-py.readthedocs.io/en/stable/)


## Related Uses Repository
- [opsariichthys-bidens](https://github.com/weiensong/opsariichthys-bidens) — About
Building a Basic Information API for Chinese National Universities in the Handheld College Entrance Examination Based on Fastapi.


## Maintainers
[@weiensong](https://github.com/weiensong)


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
[MIT](https://github.com/weiensong/weiensong/blob/main/.universal/LICENSE) © weiensong

