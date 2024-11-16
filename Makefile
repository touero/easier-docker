.PHONY: test clean all

all: test clean

test:
	coverage run -m unittest discover
	coverage report

clean:
	find . -name '__pycache__' -type d -exec rm -rf {} +
	rm -rf build/*
	rm -rf dist/*
	rm -rf dist/*
	rm -rf easier_docker.egg-info/*
	rm -rf .coverage
