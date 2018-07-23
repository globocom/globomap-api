# Version package
VERSION=$(shell python -c 'import globomap_api; print globomap_api.VERSION')

PROJECT_HOME = "`pwd`"

DOCKER_COMPOSE_FILE=$(shell make docker_file)

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

tests: ## Run tests
	@docker exec -it globomap_api make exec_tests

run: ## Run a development web server
	@/home/meta_collections.sh
	@PYTHONPATH=`pwd`:$PYTHONPATH python3.6 globomap_api/run.py

containers_start:## Start containers
	docker-compose --file $(DOCKER_COMPOSE_FILE) up -d

containers_build: ## Build containers
	docker-compose --file $(DOCKER_COMPOSE_FILE) build --no-cache

containers_stop: ## Stop containers
	docker-compose --file $(DOCKER_COMPOSE_FILE) stop

containers_clean: ## Destroy containers
	docker-compose --file $(DOCKER_COMPOSE_FILE) rm -s -v -f

dynamic_ports: ## Set ports to services
	./scripts/docker/ports.sh

docker_file:
	@if [[ -f "docker-compose-temp.yml" ]]; then \
		echo "docker-compose-temp.yml"; 		 \
	else                                         \
		echo "docker-compose.yml";               \
    fi
