# Description

## What is it
This is based on docker-py which makes it easier to run your program in docker. Configure your container image information more easily in python, allowing the container in docker to execute the configured program you want to execute.No need to `docker client` in different programs.

## What is its advantages
Simplifies Docker container management by providing a more intuitive interface on top of the docker-py SDK. It allows developers to configure and run programs in Docker containers with minimal settings, making containerization more friendly to Python developers.

- Simplified container configuration: define container settings using Python dictionary or config files.
- Automatic mirror management: automatically pull if no mirror is available locally.
- Container Lifecycle Management: Start, stop and manage containers using simple methods.
- Smart Cleanup: Remove old containers based on configurable policies.
- Network Configuration: Easily set up and manage Docker networks.

## Why make it
Initially, I just wanted a quick way to spin up containers from my Python code to avoid repeatedly configuring the Docker client in different projects. Over time, the tool evolved and matured—so I decided to release it as a standalone module.

