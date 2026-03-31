.PHONY: test coverage coverage-html clean install uninstall build upload all

UV := uv
TWINE_UPLOAD := $(UV) run twine upload --repository pypi --username __token__ --password $(TWINE_API_TOKEN)
PYTEST := $(UV) run pytest

all: clean build

test:
	$(PYTEST) --cov=src/easierdocker --cov-branch --cov-report=term-missing tests

coverage: test

coverage-html:
	$(PYTEST) --cov=src/easierdocker --cov-branch --cov-report=html tests


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
	$(UV) sync --extra dev

uninstall:
	$(UV) pip uninstall -y easier-docker

build:
	$(UV) run python -m build

upload:
	@echo "Uploading the package..."
	@if [ -z "$(TWINE_API_TOKEN)" ]; then \
		echo "Error: TWINE_API_TOKEN is not set. Please export it as an environment variable."; \
		exit 1; \
	fi
	$(TWINE_UPLOAD) dist/*
