.PHONY: help build up down restart logs ingest shell

help: ## Show this help message
	@echo "Usage: make [target]"
	@echo ""
	@echo "Available targets:"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

build: ## Build Docker images
	docker compose build

up: ## Start all services
	docker compose up -d

down: ## Stop all services
	docker compose down

restart: ## Restart all services
	docker compose restart

logs: ## Show logs from all services
	docker compose logs -f

logs-api: ## Show logs from API service
	docker compose logs -f api

ingest: ## Run data ingestion (one-time job)
	docker compose --profile ingest up ingest

shell: ## Open shell in API container
	docker compose exec api bash

shell-db: ## Open psql shell in database
	docker compose exec postgres psql -U michelin_user -d michelin_db

verify: ## Verify database contents
	docker compose exec api python main.py --verify

health: ## Check API health
	curl http://localhost:8000/health

rebuild: ## Rebuild and restart
	docker compose down
	docker compose build --no-cache
	docker compose up -d
