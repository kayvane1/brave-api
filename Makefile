SHELL=/bin/bash

.DEFAULT_GOAL := help

.PHONY: help
help: ## Shows this help text
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: init
init: clean install test ## Clean environment and reinstall all dependencies

.PHONY: clean
clean: ## Removes project virtual env
	rm -rf .venv cdk.out build dist **/*.egg-info .pytest_cache node_modules .coverage

.PHONY: install
install: ## Install the project dependencies and pre-commit using Poetry.
	poetry install --with lint,test
	poetry run pre-commit install --hook-type pre-commit --hook-type commit-msg --hook-type pre-push

.PHONY: test
test: ## Run tests
	poetry run python -m pytest

.PHONY: lint
lint: ## Apply linters to all files
	poetry run pre-commit run --all-files
