# Menshun Enterprise PAM Tool - Development Makefile
# This Makefile provides convenient commands for development, testing, and deployment

.PHONY: help install dev test lint format security clean docker docs

# Default target
help:
	@echo "Menshun Development Commands"
	@echo "============================"
	@echo ""
	@echo "Setup & Installation:"
	@echo "  install       - Install all dependencies and setup development environment"
	@echo "  install-hooks - Install pre-commit hooks"
	@echo ""
	@echo "Development:"
	@echo "  dev           - Start development environment with hot-reload"
	@echo "  dev-backend   - Start only backend development server"
	@echo "  dev-frontend  - Start only frontend development server"
	@echo ""
	@echo "Code Quality:"
	@echo "  lint          - Run all linting checks"
	@echo "  format        - Format all code"
	@echo "  type-check    - Run type checking"
	@echo "  security      - Run security scans"
	@echo ""
	@echo "Testing:"
	@echo "  test          - Run all tests"
	@echo "  test-backend  - Run backend tests with coverage"
	@echo "  test-frontend - Run frontend tests with coverage"
	@echo "  coverage      - Generate and view coverage reports"
	@echo ""
	@echo "Database:"
	@echo "  db-migrate    - Run database migrations"
	@echo "  db-seed       - Seed database with directory roles"
	@echo "  db-reset      - Reset database (WARNING: destroys data)"
	@echo ""
	@echo "Docker:"
	@echo "  docker-build  - Build all Docker images"
	@echo "  docker-up     - Start all services with Docker Compose"
	@echo "  docker-down   - Stop all Docker services"
	@echo "  docker-logs   - View Docker logs"
	@echo ""
	@echo "Documentation:"
	@echo "  docs          - Generate and serve documentation"
	@echo "  docs-api      - Generate API documentation"
	@echo ""
	@echo "Cleanup:"
	@echo "  clean         - Clean temporary files and caches"
	@echo "  clean-docker  - Clean Docker images and volumes"

# Installation and Setup
install: install-backend install-frontend install-hooks
	@echo "✅ Installation complete! Run 'make dev' to start development."

install-backend:
	@echo "📦 Installing backend dependencies..."
	cd backend && pip install -r requirements.txt -r requirements-dev.txt

install-frontend:
	@echo "📦 Installing frontend dependencies..."
	cd frontend && npm ci

install-hooks:
	@echo "🔧 Installing pre-commit hooks..."
	pip install pre-commit
	pre-commit install
	pre-commit install --hook-type commit-msg

# Development
dev: docker-up
	@echo "🚀 Starting full development environment..."
	@echo "Backend API: http://localhost:8000"
	@echo "Frontend App: http://localhost:3000"
	@echo "API Docs: http://localhost:8000/docs"

dev-backend:
	@echo "🚀 Starting backend development server..."
	cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

dev-frontend:
	@echo "🚀 Starting frontend development server..."
	cd frontend && npm run dev

# Code Quality
lint: lint-backend lint-frontend
	@echo "✅ All linting checks passed!"

lint-backend:
	@echo "🔍 Linting backend code..."
	cd backend && flake8 app/
	cd backend && mypy app/

lint-frontend:
	@echo "🔍 Linting frontend code..."
	cd frontend && npm run lint

format: format-backend format-frontend
	@echo "✨ Code formatting complete!"

format-backend:
	@echo "✨ Formatting backend code..."
	cd backend && black app/
	cd backend && isort app/

format-frontend:
	@echo "✨ Formatting frontend code..."
	cd frontend && npm run format

type-check: type-check-backend type-check-frontend
	@echo "✅ Type checking complete!"

type-check-backend:
	@echo "🔍 Type checking backend..."
	cd backend && mypy app/

type-check-frontend:
	@echo "🔍 Type checking frontend..."
	cd frontend && npm run type-check

security:
	@echo "🛡️  Running security scans..."
	cd backend && bandit -r app/ -f json -o bandit-results.json || true
	cd frontend && npm audit --audit-level moderate || true
	@echo "🛡️  Security scan complete. Check reports for details."

# Testing
test: test-backend test-frontend
	@echo "✅ All tests passed!"

test-backend:
	@echo "🧪 Running backend tests..."
	cd backend && pytest --cov=app --cov-report=html --cov-report=term-missing

test-frontend:
	@echo "🧪 Running frontend tests..."
	cd frontend && npm run test:coverage

coverage:
	@echo "📊 Opening coverage reports..."
	@echo "Backend coverage: backend/htmlcov/index.html"
	@echo "Frontend coverage: frontend/coverage/lcov-report/index.html"
	python -m webbrowser backend/htmlcov/index.html
	python -m webbrowser frontend/coverage/lcov-report/index.html

# Database Management
db-migrate:
	@echo "🗄️  Running database migrations..."
	cd backend && alembic upgrade head

db-seed:
	@echo "🌱 Seeding database with directory roles..."
	cd backend && python -m app.scripts.seed_roles

db-reset:
	@echo "⚠️  WARNING: This will destroy all data!"
	@read -p "Are you sure? [y/N] " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		docker-compose down -v; \
		docker-compose up -d postgres; \
		sleep 5; \
		make db-migrate db-seed; \
	fi

# Docker Management
docker-build:
	@echo "🐳 Building Docker images..."
	docker-compose build

docker-up:
	@echo "🐳 Starting Docker services..."
	docker-compose up -d
	@echo "⏳ Waiting for services to be ready..."
	@timeout 60 bash -c 'until docker-compose exec -T backend curl -f http://localhost:8000/health >/dev/null 2>&1; do sleep 2; done' || true

docker-down:
	@echo "🐳 Stopping Docker services..."
	docker-compose down

docker-logs:
	@echo "📋 Viewing Docker logs..."
	docker-compose logs -f

# Documentation
docs:
	@echo "📚 Generating documentation..."
	cd docs && mkdocs serve

docs-api:
	@echo "📚 Generating API documentation..."
	cd backend && python -m app.scripts.generate_openapi_spec
	@echo "API documentation available at: http://localhost:8000/docs"

# Cleanup
clean: clean-python clean-node clean-cache
	@echo "🧹 Cleanup complete!"

clean-python:
	@echo "🧹 Cleaning Python cache files..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf backend/.coverage backend/htmlcov backend/.pytest_cache

clean-node:
	@echo "🧹 Cleaning Node.js cache files..."
	rm -rf frontend/node_modules/.cache
	rm -rf frontend/build frontend/dist
	rm -rf frontend/coverage

clean-cache:
	@echo "🧹 Cleaning cache files..."
	rm -rf .mypy_cache .pytest_cache
	docker system prune -f

clean-docker:
	@echo "🧹 Cleaning Docker resources..."
	docker-compose down -v
	docker system prune -af
	docker volume prune -f

# Deployment helpers
build-prod:
	@echo "🏗️  Building production images..."
	docker-compose -f docker-compose.prod.yml build

deploy-staging:
	@echo "🚀 Deploying to staging..."
	# Add staging deployment commands here

deploy-prod:
	@echo "🚀 Deploying to production..."
	# Add production deployment commands here

# Development utilities
logs-backend:
	docker-compose logs -f backend

logs-frontend:
	docker-compose logs -f frontend

logs-db:
	docker-compose logs -f postgres

shell-backend:
	docker-compose exec backend bash

shell-db:
	docker-compose exec postgres psql -U pamuser -d pamdb

# Quick checks
check: lint type-check security test
	@echo "✅ All checks passed! Ready to commit."

# CI/CD simulation
ci: install lint type-check security test docker-build
	@echo "✅ CI pipeline simulation complete!"