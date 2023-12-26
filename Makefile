ENV_FILE = .env.docker

.DEFAULT_GOAL := help
.PHONY: *

help:
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
	| sed -n 's/^\(.*\): \(.*\)\(##\)\(.*\)/\1\3-\4/p' \
	| column -t -s '##'

build: ## Build application
	@docker-compose --env-file $(ENV_FILE) build gitlab-auto-approve

rebuild: ## Build application without cache
	@docker-compose --env-file $(ENV_FILE) build --no-cache gitlab-auto-approve

run: ## Run application
	@docker-compose --env-file $(ENV_FILE) up gitlab-auto-approve

build-dev: ## Build dev application
	@docker-compose --env-file $(ENV_FILE) build gitlab-auto-approve-dev

rebuild-dev: ## Build dev application without cache
	@docker-compose --env-file $(ENV_FILE) build --no-cache gitlab-auto-approve-dev

run-dev: ## Run dev application
	@docker-compose --env-file $(ENV_FILE) up gitlab-auto-approve-dev

test: ## Run tests
	@docker-compose --env-file $(ENV_FILE) run --entrypoint "pytest /tests" gitlab-auto-approve-dev

publish: ## Publish application
	@./publish.sh