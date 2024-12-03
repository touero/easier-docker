.PHONY: test clean install build upload all

TWINE_UPLOAD := twine upload --repository pypi --username __token__ --password $(TWINE_API_TOKEN)

all: clean build

test:
	coverage run -m unittest discover
	coverage report
	coverage html
	google-chrome htmlcov/index.html


clean:
	find . -name '__pycache__' -type d -exec rm -rf {} +
	find . -name 'easier_docker.egg-info' -type d -exec rm -rf {} +
	find . -name 'example.egg-info' -type d -exec rm -rf {} +
	rm -rf htmlcov
	rm -rf build
	rm -rf dist
	rm -rf .coverage
	rm -rf htmlcov

install:
	pip install -e .

uninstall:
	pip uninstall -y easier_docker

build:
	python -m build

upload:
	@echo "Uploading the package..."
	@if [ -z "$(TWINE_API_TOKEN)" ]; then \
		echo "Error: TWINE_API_TOKEN is not set. Please export it as an environment variable."; \
		exit 1; \
	fi
	$(TWINE_UPLOAD) dist/*
