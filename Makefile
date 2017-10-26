.PHONY: help setup clean pep8 tests run

# Version package
VERSION=$(shell python -c 'import globomap_api; print globomap_api.VERSION')

PROJECT_HOME = "`pwd`"

help:
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

setup: ## Install project dependencies
	@pip install -r $(PROJECT_HOME)/requirements_test.txt

clean: ## Clear *.pyc files, etc
	@rm -rf build dist *.egg-info
	@find . \( -name '*.pyc' -o  -name '__pycache__' -o -name '**/*.pyc' -o -name '*~' \) -delete

pep8: ## Check source-code for PEP8 compliance
	@-pep8 globomap_api

exec_tests: clean pep8 ## Run all tests with coverage
	@python3.6 -m unittest discover -s tests/
	#@run --source=globomap_api -m unittest2 discover -s tests/; coverage report -m

tests:
	@docker exec -it globomap_api make exec_tests

run: ## Run a development web server
	@PYTHONPATH=`pwd`:$PYTHONPATH python3.6 globomap_api/run.py

docker: ## Run a development web server
	@docker-compose build
	@docker-compose up -d

dist: clean
	@python setup.py sdist

publish: clean dist
	@echo 'Ready to release version ${VERSION}? (ctrl+c to abort)' && read
	twine upload dist/*
	@git tag ${VERSION}
	@git push --tags

deploy:
	@tsuru app-deploy -a $(project) globomap_api .python-version Procfile requirements.txt
