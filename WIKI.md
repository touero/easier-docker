# Welcome to the eaiser-docker wiki!

## Install
It should be a package for your real environment.
```shell
pip install easier-docker
```

## Explain 
Two params it need now, and `network_config` and `extra_config` are kwargs:
> [!Note]
> - __container_config__: Necessary, run and manage containers on the server. Run a container. By default, it will wait for the container to finish and return its logs, similar to `docker run`.  
> - __network_config__: Unnecessary, create and manage networks on the server. For more information about networks, see the [Engine documentation](https://docs.docker.com/network/). Create a network. Similar to the `docker network create`.
> - __extra_config__: Unnecessary, add extra configurations to the container.Currently used to control whether existing containers will be automatically removed.   

Two params config please check:
> [!Important]
> 1. __container_config__: [Docker SDK for Python with Container](https://docker-py.readthedocs.io/en/7.1.0/containers.html)
> 2. __network_config__: [Docker SDK for Python with Network](https://docker-py.readthedocs.io/en/7.1.0/networks.html)
> 3. __extra_config__: Include and default value: `is_remove`, `days_ago_remove`, `remove_now`, 
>> `is_remove`: default value is `0`, if it is `1`, enable function that will remove the existing container with the same name.  
>> `days_ago_remove`: default value is `3`, it will remove the existing container with the same name if it is older than the specified number of days.  
>> `remove_now`: default value is `0`, if it is `1`, `days_ago_remove`will be ineffective, it will remove the existing container with the same name immediately.
 

## Usage
### Use examples in code
[example.py](https://github.com/touero/easier-docker/blob/master/example/example.py)
```bash
python example.py
```
[docker_example.py](https://github.com/touero/easier-docker/blob/master/example/docker_example.py)
![code_start](/image/code_start.gif)

and the docker container logs will be shown in the console.

![docker_logs](/image/docker_log.gif)

### Run directly from configuration file
> [!Note]
> Currently supports type of file: _yml_, _yaml_, _json_

```bash
easier-docker -c config.yaml
```
[config.yaml](https://github.com/touero/easier-docker/blob/master/example/config.yaml)
![file](/image/file.gif)
