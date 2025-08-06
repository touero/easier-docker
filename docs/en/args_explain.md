# Args Explain
Two params it need now, and `network_config` and `extra_config` are kwargs:
- `container_config`: Necessary, run and manage containers on the server. Run a container. By default, it will wait for the container to finish and return its logs, similar to `docker run`.  
- `network_config`: Unnecessary, create and manage networks on the server. For more information about networks, see the [Engine documentation](https://docs.docker.com/network/). Create a network. Similar to the `docker network create`.
- `extra_config`: Unnecessary, add extra configurations to the container.Currently used to control whether existing containers will be automatically removed.

Two params config please check:
1. `container_config`: [Docker SDK for Python with Container](https://docker-py.readthedocs.io/en/7.1.0/containers.html)
2. `network_config`: [Docker SDK for Python with Network](https://docker-py.readthedocs.io/en/7.1.0/networks.html)
3. `extra_config`: Include and default value: `is_remove`, `days_ago_remove`, `remove_now`, 
> `is_remove`: default value is `0`, if it is `1`, enable function that will remove the existing container with the same name.  
> `days_ago_remove`: default value is `3`, it will remove the existing container with the same name if it is older than the specified number of days.  
> `remove_now`: default value is `0`, if it is `1`, `days_ago_remove`will be ineffective, it will remove the existing container with the same name immediately.
