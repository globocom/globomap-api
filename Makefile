.PHONY: help setup clean pep8 tests run

PROJECT_HOME = "`pwd`"

help:
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

setup: ## Install project dependencies
	@pip install -r $(PROJECT_HOME)/requirements_test.txt

clean: ## Clear *.pyc files, etc
	@find . -name "*.pyc" -delete
	@find . -name "*.~" -delete

pep8: ## Check source-code for PEP8 compliance
	@-pep8 $(PROJECT_HOME)

tests: clean pep8 ## Run all tests with coverage
	@py.test --cov-config .coveragerc --cov $(PROJECT_HOME) --cov-report term-missing

run: ## Run a development web server
	@echo TODO
