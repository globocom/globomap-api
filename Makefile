# Version package
VERSION=$(shell python -c 'import globomap_api; print globomap_api.VERSION')

PROJECT_HOME = "`pwd`"

help:
	@echo
	@echo "Please use 'make <target>' where <target> is one of"
	@echo

	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

setup: ## Install project dependencies
	@pip install -r $(PROJECT_HOME)/requirements_test.txt

clean: ## Clear *.pyc files, etc
	@rm -rf build dist *.egg-info
	@find . \( -name '*.pyc' -o  -name '__pycache__' -o -name '**/*.pyc' -o -name '*~' \) -delete

exec_tests: clean ## Run all tests with coverage
	@nosetests --verbose --rednose  --nocapture --cover-package=globomap_api --with-coverage; coverage report -m

test: ## Run tests
	@docker exec -it globomap_api make exec_tests

run: ## Run a development web server
	@PYTHONPATH=`pwd`:$PYTHONPATH python3.6 globomap_api/run.py

containers_start:## Start containers
	docker-compose up -d

keystone_config: ## Config keystone
	@docker exec globomap_keystone "/home/keystone.sh"

containers_build: ## Build containers
	docker-compose build

deploy: ## Deploy in Tsuru
	@tsuru app-deploy -a $(project) globomap_api .python-version Procfile requirements.txt api_plugins
