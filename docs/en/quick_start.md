# Quick Start

## Before You Start

Make sure Docker is running and your current user can access it.

## CLI Example

Run with a config file:

```shell
easier-docker -c config.yaml
```

Example `config.yaml`:

```yaml
container:
  image: python:3.9
  name: python_test
  volumes:
    ./example:
      bind: /workspace
      mode: rw
  detach: true
  command:
    - sh
    - -c
    - cd /workspace && python docker_example.py

network:
  name: bridge
  driver: bridge

extra:
  is_remove: 1
  days_ago_remove: 7
  remove_now: 0
```

Notes:

- The CLI accepts `.yaml`, `.yml`, and `.json` files.
- `container.image` and `container.name` should always be set.
- Volume keys should use paths valid on the machine that runs Docker.

## Python API Example

```python
import os

from easierdocker import EasierDocker


if __name__ == "__main__":
    host_script = os.path.join(os.getcwd(), "example")
    container_script = "/workspace"

    container_config = {
        "image": "python:3.9",
        "name": "python_test",
        "volumes": {
            host_script: {"bind": container_script, "mode": "rw"},
        },
        "detach": True,
        "command": [
            "sh",
            "-c",
            f"cd {container_script} && python docker_example.py",
        ],
    }

    network_config = {
        "name": "bridge",
        "driver": "bridge",
    }

    extra_config = {
        "is_remove": 1,
        "days_ago_remove": 3,
        "remove_now": 1,
    }

    EasierDocker(
        container_config,
        network_config=network_config,
        extra_config=extra_config,
    ).start()
```

## What Happens At Runtime

When you call `start()`:

1. The package checks whether the image exists locally.
2. If the image is missing, it pulls it from the registry.
3. If `network_config.name` is set, it reuses or creates that network.
4. It looks for a container with the same name.
5. Depending on `extra_config`, it reuses the container or removes it and starts a new one.

## Example Files

- Example config: [example/config.yaml](https://github.com/touero/easier-docker/blob/master/example/config.yaml)
- Example script: [example/docker_example.py](https://github.com/touero/easier-docker/blob/master/example/docker_example.py)
