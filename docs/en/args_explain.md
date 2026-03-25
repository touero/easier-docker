# Configuration Reference

`easier-docker` works with three configuration groups.

## `container_config`

Required. This dictionary is passed to the Docker SDK call that runs the container:

- Reference: [Docker SDK for Python containers](https://docker-py.readthedocs.io/en/7.1.0/containers.html)

Common fields used in this project:

- `image`: Container image name. Required in practice.
- `name`: Container name. Required in practice because the package uses it to find existing containers.
- `command`: Command to run inside the container.
- `detach`: Whether to run the container in detached mode.
- `volumes`: Host-to-container volume mappings.
- `environment`: Optional environment variables.
- `ports`: Optional port mappings.
- `network`: Added automatically when `network_config` is used.

## `network_config`

Optional. When `network_config["name"]` is provided, the package checks whether that network already exists. If not, it creates the network and then sets `container_config["network"]` to that name.

- Reference: [Docker SDK for Python networks](https://docker-py.readthedocs.io/en/7.1.0/networks.html)

Common fields:

- `name`: Network name.
- `driver`: Network driver such as `bridge`.

If `name` is missing, network creation is skipped.

## `extra_config`

Optional. These values control cleanup behavior for an existing container with the same name.

Supported keys:

- `is_remove` (`int`)
- `days_ago_remove` (`int`)
- `remove_now` (`int`)

Behavior:

- `is_remove = 0`: Do not remove an existing container automatically.
- `is_remove = 1`: Allow removal when the age rule or `remove_now` matches.
- `days_ago_remove = 3`: Default runtime fallback if the key is omitted.
- `remove_now = 1`: Remove the existing container immediately, regardless of age.

Validation rules:

- All provided `extra_config` values must be integers.
- Unknown keys raise `ValueError`.
- Invalid value types raise `TypeError`.

## Minimal Example

```python
container_config = {
    "image": "python:3.9",
    "name": "python_test",
    "detach": True,
}

network_config = {
    "name": "bridge",
    "driver": "bridge",
}

extra_config = {
    "is_remove": 1,
    "days_ago_remove": 3,
    "remove_now": 0,
}
```
