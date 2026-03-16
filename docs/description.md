# Description

## What It Is

`easier-docker` is a small wrapper around the Docker SDK for Python. It helps you run Docker containers from Python code or from a YAML/JSON file without repeating the same client setup in each project.

## Why Use It

- Less boilerplate: define container settings once and call `start()`.
- Config-file support: use the same structure from the CLI or Python.
- Automatic image pull: if the image is missing locally, it is pulled first.
- Optional cleanup: replace containers with the same name using simple rules.
- Network support: create and attach a network when needed.

## Typical Workflow

1. Define `container_config`.
2. Optionally define `network_config`.
3. Optionally define `extra_config` for cleanup behavior.
4. Run `easier-docker -c config.yaml` or call `EasierDocker(...).start()`.

## Why It Exists

The project was created to make Docker-backed Python workflows easier to reuse across multiple programs. Instead of wiring Docker client calls in each codebase, you can keep the runtime settings in one place and let `easier-docker` handle image lookup, network creation, and container startup.
