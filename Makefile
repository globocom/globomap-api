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

exec_tests: ## Make tests
	@nosetests --verbose --rednose  --nocapture --cover-package=globomap_api --with-coverage; coverage report -m

tests: ## Run tests
	@docker exec -it globomap_api make exec_tests || true

tests_ci: ## Run tests
	@docker exec globomap_api make exec_tests || true

run: ## Run a development web server
	@PYTHONPATH=`pwd`:$PYTHONPATH python3.6 globomap_api/run.py

containers_start: dynamic_ports ## Start containers
	docker-compose up -d
	./scripts/docker/keystone/setup.sh

containers_build: dynamic_ports ## Build containers
	docker-compose build --no-cache

containers_stop: ## Stop containers
	docker-compose stop

containers_clean: ## Destroy containers
	docker-compose rm -s -v -f

dynamic_ports: ## Set ports to services
	./scripts/docker/expose_ports.sh
