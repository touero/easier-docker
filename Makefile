clean:
	find . -name '__pycache__' -type d -exec rm -rf {} +
	rm -rf build/*
	rm -rf dist/*
	rm -rf dist/*
	rm -rf easier_docker.egg-info/*
	rm -rf .coverage

.PHONY: clean