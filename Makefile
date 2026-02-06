.PHONY: help install install-backend install-frontend test test-backend test-frontend lint lint-backend lint-frontend format format-backend clean docker-up docker-down docker-logs

# Colors for output
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[1;33m
NC := \033[0m # No Color

help: ## Show this help message
	@echo "$(BLUE)LiveKit Voice Agent - Development Commands$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "$(GREEN)%-20s$(NC) %s\n", $$1, $$2}'

# Installation
install: install-backend install-frontend ## Install all dependencies

install-backend: ## Install backend dependencies
	@echo "$(BLUE)Installing backend dependencies...$(NC)"
	cd backend && pip install -r requirements.txt

install-frontend: ## Install frontend dependencies
	@echo "$(BLUE)Installing frontend dependencies...$(NC)"
	cd frontend && npm install

# Development
dev-backend: ## Run backend in development mode
	@echo "$(BLUE)Starting backend server...$(NC)"
	cd backend && uvicorn server:app --reload --port 5001

dev-frontend: ## Run frontend in development mode
	@echo "$(BLUE)Starting frontend server...$(NC)"
	cd frontend && npm run dev

dev: ## Run both backend and frontend (requires tmux or separate terminals)
	@echo "$(YELLOW)Note: Run 'make dev-backend' and 'make dev-frontend' in separate terminals$(NC)"

# Testing
test: test-backend ## Run all tests

test-backend: ## Run backend tests
	@echo "$(BLUE)Running backend tests...$(NC)"
	cd backend && pytest -v

test-backend-cov: ## Run backend tests with coverage
	@echo "$(BLUE)Running backend tests with coverage...$(NC)"
	cd backend && pytest --cov=. --cov-report=html --cov-report=term

test-frontend: ## Run frontend tests
	@echo "$(BLUE)Running frontend tests...$(NC)"
	cd frontend && npm test

test-watch: ## Run backend tests in watch mode
	@echo "$(BLUE)Running backend tests in watch mode...$(NC)"
	cd backend && pytest-watch

# Linting
lint: lint-backend lint-frontend ## Run all linters

lint-backend: ## Lint backend code
	@echo "$(BLUE)Linting backend code...$(NC)"
	cd backend && ruff check .

lint-frontend: ## Lint frontend code
	@echo "$(BLUE)Linting frontend code...$(NC)"
	cd frontend && npm run lint

# Formatting
format: format-backend ## Format all code

format-backend: ## Format backend code
	@echo "$(BLUE)Formatting backend code...$(NC)"
	cd backend && black .

format-check-backend: ## Check backend code formatting
	@echo "$(BLUE)Checking backend code formatting...$(NC)"
	cd backend && black --check .

# Type checking
typecheck: ## Run type checking
	@echo "$(BLUE)Type checking backend code...$(NC)"
	cd backend && mypy . --ignore-missing-imports

# Docker
docker-build: ## Build Docker images
	@echo "$(BLUE)Building Docker images...$(NC)"
	docker-compose build

docker-up: ## Start all services with Docker Compose
	@echo "$(BLUE)Starting services...$(NC)"
	docker-compose up -d

docker-down: ## Stop all services
	@echo "$(BLUE)Stopping services...$(NC)"
	docker-compose down

docker-logs: ## Show Docker logs
	docker-compose logs -f

docker-clean: ## Clean Docker volumes and images
	@echo "$(YELLOW)Cleaning Docker volumes and images...$(NC)"
	docker-compose down -v
	docker system prune -f

# Database
db-migrate: ## Run database migrations
	@echo "$(BLUE)Running database migrations...$(NC)"
	cd backend && alembic upgrade head

db-rollback: ## Rollback last migration
	@echo "$(BLUE)Rolling back last migration...$(NC)"
	cd backend && alembic downgrade -1

db-shell: ## Open database shell
	@echo "$(BLUE)Opening database shell...$(NC)"
	docker-compose exec postgres psql -U livekit -d livekit_tutor

# Cleaning
clean: ## Clean build artifacts and cache
	@echo "$(BLUE)Cleaning build artifacts...$(NC)"
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete
	find . -type d -name '*.egg-info' -exec rm -rf {} +
	find . -type d -name 'htmlcov' -exec rm -rf {} +
	find . -type f -name '.coverage' -delete
	rm -rf frontend/dist
	rm -rf backend/dist

# Environment setup
env-setup: ## Create .env files from examples
	@echo "$(BLUE)Creating .env files...$(NC)"
	@test -f .env || cp .env.example .env
	@test -f backend/.env || cp backend/.env.example backend/.env
	@test -f frontend/.env || cp frontend/.env.example frontend/.env
	@echo "$(GREEN)Environment files created. Please edit them with your configuration.$(NC)"

# Documentation
docs: ## Generate API documentation
	@echo "$(BLUE)API documentation available at: http://localhost:5001/api/docs$(NC)"

# Health checks
health: ## Check service health
	@echo "$(BLUE)Checking service health...$(NC)"
	@curl -s http://localhost:5001/api/health | python -m json.tool || echo "$(YELLOW)Backend not running$(NC)"

# Monitoring
metrics: ## View Prometheus metrics
	@echo "$(BLUE)Opening Prometheus metrics...$(NC)"
	@open http://localhost:9090 || xdg-open http://localhost:9090 || echo "Visit: http://localhost:9090"

grafana: ## Open Grafana dashboards
	@echo "$(BLUE)Opening Grafana...$(NC)"
	@open http://localhost:3001 || xdg-open http://localhost:3001 || echo "Visit: http://localhost:3001"

# CI/CD
ci: lint test ## Run CI checks locally
	@echo "$(GREEN)All CI checks passed!$(NC)"

# Production
prod-build: ## Build production images
	@echo "$(BLUE)Building production images...$(NC)"
	docker-compose -f docker-compose.yml build

prod-up: ## Start production services
	@echo "$(BLUE)Starting production services...$(NC)"
	docker-compose -f docker-compose.yml up -d

# Quick start
quickstart: env-setup docker-up ## Quick start with Docker
	@echo "$(GREEN)Application started!$(NC)"
	@echo "Frontend: http://localhost"
	@echo "Backend API: http://localhost:5001"
	@echo "API Docs: http://localhost:5001/api/docs"
	@echo "Grafana: http://localhost:3001"

# Version
version: ## Show version information
	@echo "Python: $$(python --version)"
	@echo "Node: $$(node --version)"
	@echo "npm: $$(npm --version)"
	@echo "Docker: $$(docker --version)"
	@echo "Docker Compose: $$(docker-compose --version)"
