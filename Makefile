ENV_FILE = .env.docker

.DEFAULT_GOAL := help
.PHONY: *

help:
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
	| sed -n 's/^\(.*\): \(.*\)\(##\)\(.*\)/\1\3-\4/p' \
	| column -t -s '##'

build: ## Build application
	@docker-compose --env-file $(ENV_FILE) build

rebuild: ## Build application without cache
	@docker-compose --env-file $(ENV_FILE) build --no-cache

run: ## Run application
	@docker-compose --env-file $(ENV_FILE) up

publish: ## Publish application
	@./publish.sh