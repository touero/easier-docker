# Development

## Tooling

- [uv](https://docs.astral.sh/uv/) for environment and dependency management
- Python 3.8 or newer

## Create Virtual Environment

```shell
uv venv
```

Use a specific Python version if needed:

```shell
uv venv --python 3.11
```

## Sync Dependencies

```shell
uv sync --extra dev
```

## Run Tests

```shell
uv run pytest
```

## Build Package

```shell
uv run python -m build
```

## Makefile Shortcuts

The repository includes a [Makefile](https://github.com/touero/easier-docker/blob/master/Makefile) for common tasks:

```shell
make install
make test
make build
```

## Contributing

- Issues: https://github.com/touero/easier-docker/issues
- Pull requests: https://github.com/touero/easier-docker/pulls
- Branch target: `develop`

Follow standard Python style conventions such as [PEP 8](https://peps.python.org/pep-0008/).
