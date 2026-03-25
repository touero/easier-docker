# Install

## Requirements

- Python 3.8 or newer
- Docker installed on the host
- Access to a running Docker daemon

If Docker is installed but the daemon is unavailable, the package raises `DockerConnectionError` during initialization.

## Install From PyPI

```shell
pip install easier-docker
```

## Install From Source

```shell
git clone https://github.com/touero/easier-docker.git
cd easier-docker
pip install -e .
```

## Verify Installation

Check the CLI:

```shell
easier-docker --help
```

Check the Python import:

```shell
python -c "from easierdocker import EasierDocker; print(EasierDocker.__name__)"
```
