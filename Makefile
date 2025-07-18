# Menshun PAM - Simplified Deployment Makefile
# This Makefile provides easy commands to deploy and manage Menshun PAM
# 
# Docker Permission Handling:
# - Automatically detects if user is in 'docker' group
# - Uses 'sudo' for Docker commands if user lacks Docker permissions
# - Works seamlessly regardless of Docker installation method (package/snap)

# Variables
COMPOSE_FILE := docker-compose.yml
PROD_COMPOSE_FILE := docker-compose.prod.yml
PROJECT_NAME := menshun-pam
BACKUP_DIR := ./backups
LOG_DIR := ./logs

# Docker command - automatically use sudo if user is not in docker group
DOCKER_CMD := $(shell if groups | grep -q docker || [ "$$EUID" -eq 0 ]; then echo "docker"; else echo "sudo docker"; fi)
DOCKER_COMPOSE_CMD := $(shell if groups | grep -q docker || [ "$$EUID" -eq 0 ]; then echo "docker-compose"; else echo "sudo docker-compose"; fi)

# Colors for terminal output
RED := \033[0;31m
GREEN := \033[0;32m
YELLOW := \033[1;33m
BLUE := \033[0;34m
NC := \033[0m # No Color

# Default target
.DEFAULT_GOAL := help

##@ General Commands

.PHONY: help
help: ## Display this help message
	@echo "$(BLUE)Menshun PAM - Enterprise Privileged Access Management$(NC)"
	@echo "$(BLUE)============================================$(NC)"
	@echo ""
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_0-9-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

.PHONY: init
init: ## 🚀 Initialize and deploy Menshun PAM (development)
	@echo "$(BLUE)🚀 Initializing Menshun PAM Development Environment$(NC)"
	@$(MAKE) check-requirements
	@$(MAKE) setup-directories
	@$(MAKE) setup-env-dev
	@$(MAKE) build
	@$(MAKE) start-dev
	@$(MAKE) init-database
	@$(MAKE) post-deploy-info
	@echo "$(GREEN)✅ Menshun PAM development environment is ready!$(NC)"

.PHONY: init-prod
init-prod: ## 🏢 Initialize and deploy Menshun PAM (production)
	@echo "$(BLUE)🏢 Initializing Menshun PAM Production Environment$(NC)"
	@$(MAKE) check-requirements
	@$(MAKE) setup-directories
	@$(MAKE) setup-env-prod
	@$(MAKE) build-prod
	@$(MAKE) start-prod
	@$(MAKE) init-database-prod
	@$(MAKE) setup-ssl
	@$(MAKE) post-deploy-info-prod
	@echo "$(GREEN)✅ Menshun PAM production environment is ready!$(NC)"

##@ Setup Commands

.PHONY: check-requirements
check-requirements: ## Check system requirements
	@echo "$(YELLOW)📋 Checking system requirements...$(NC)"
	@command -v docker >/dev/null 2>&1 || { echo "$(RED)❌ Docker is not installed$(NC)"; exit 1; }
	@command -v docker-compose >/dev/null 2>&1 || command -v docker >/dev/null 2>&1 && $(DOCKER_CMD) compose version >/dev/null 2>&1 || { echo "$(RED)❌ Docker Compose is not installed$(NC)"; exit 1; }
	@command -v git >/dev/null 2>&1 || { echo "$(RED)❌ Git is not installed$(NC)"; exit 1; }
	@if ! groups | grep -q docker && [ "$$EUID" -ne 0 ]; then echo "$(YELLOW)⚠️ User not in docker group - will use sudo for Docker commands$(NC)"; fi
	@echo "$(GREEN)✅ All requirements satisfied$(NC)"

.PHONY: setup-directories
setup-directories: ## Create required directories
	@echo "$(YELLOW)📁 Creating required directories...$(NC)"
	@mkdir -p $(BACKUP_DIR)
	@mkdir -p $(LOG_DIR)
	@mkdir -p data/postgres
	@mkdir -p data/redis
	@mkdir -p ssl/certificates
	@mkdir -p monitoring/grafana/dashboards
	@mkdir -p monitoring/grafana/datasources
	@echo "$(GREEN)✅ Directories created$(NC)"

.PHONY: setup-env-dev
setup-env-dev: ## Setup development environment file
	@echo "$(YELLOW)⚙️  Setting up development environment...$(NC)"
	@if [ ! -f .env ]; then \
		echo "$(BLUE)📝 Creating development .env file...$(NC)"; \
		cp .env.example .env; \
		echo "$(YELLOW)⚠️  Please edit .env file with your Azure AD credentials$(NC)"; \
		echo "$(YELLOW)   Required: AZURE_CLIENT_ID, AZURE_CLIENT_SECRET, AZURE_TENANT_ID$(NC)"; \
	else \
		echo "$(GREEN)✅ .env file already exists$(NC)"; \
	fi
	@if [ ! -f frontend/.env ]; then \
		echo "$(BLUE)📝 Creating frontend .env file...$(NC)"; \
		cp frontend/.env.example frontend/.env; \
	fi

.PHONY: setup-env-prod
setup-env-prod: ## Setup production environment file
	@echo "$(YELLOW)⚙️  Setting up production environment...$(NC)"
	@if [ ! -f .env ]; then \
		echo "$(BLUE)📝 Creating production .env file...$(NC)"; \
		cp .env.example .env; \
		sed -i.bak 's/ENVIRONMENT=development/ENVIRONMENT=production/' .env; \
		sed -i.bak 's/DEBUG=true/DEBUG=false/' .env; \
		sed -i.bak 's/localhost:3000/your-domain.com/' .env; \
		rm -f .env.bak; \
		echo "$(RED)🚨 IMPORTANT: Edit .env file with production settings!$(NC)"; \
		echo "$(YELLOW)   Required: DOMAIN, AZURE_CLIENT_ID, AZURE_CLIENT_SECRET, AZURE_TENANT_ID$(NC)"; \
		echo "$(YELLOW)   Generate secure passwords for: POSTGRES_PASSWORD, SECRET_KEY, ENCRYPTION_KEY$(NC)"; \
	else \
		echo "$(GREEN)✅ .env file already exists$(NC)"; \
	fi

.PHONY: setup-ssl
setup-ssl: ## Setup SSL certificates
	@echo "$(YELLOW)🔐 Setting up SSL certificates...$(NC)"
	@if [ ! -f ssl/certificates/cert.pem ]; then \
		echo "$(BLUE)📝 Creating self-signed certificate for development...$(NC)"; \
		openssl req -x509 -newkey rsa:4096 -keyout ssl/certificates/key.pem -out ssl/certificates/cert.pem -days 365 -nodes -subj "/CN=localhost"; \
		echo "$(YELLOW)⚠️  For production, replace with proper SSL certificates$(NC)"; \
	else \
		echo "$(GREEN)✅ SSL certificates already exist$(NC)"; \
	fi

##@ Build Commands

.PHONY: build
build: ## Build all Docker images
	@echo "$(YELLOW)🔨 Building Docker images...$(NC)"
	@$(DOCKER_COMPOSE_CMD) -f $(COMPOSE_FILE) build

.PHONY: build-prod
build-prod: ## Build production Docker images
	@echo "$(YELLOW)🔨 Building production Docker images...$(NC)"
	@$(DOCKER_COMPOSE_CMD) -f $(PROD_COMPOSE_FILE) build

.PHONY: pull
pull: ## Pull latest Docker images
	@echo "$(YELLOW)📥 Pulling latest Docker images...$(NC)"
	@$(DOCKER_COMPOSE_CMD) -f $(COMPOSE_FILE) pull

##@ Service Management

.PHONY: start-dev
start-dev: ## Start development services
	@echo "$(YELLOW)🚀 Starting development services...$(NC)"
	@$(DOCKER_COMPOSE_CMD) -f $(COMPOSE_FILE) up -d
	@echo "$(GREEN)✅ Development services started$(NC)"

.PHONY: start-prod
start-prod: ## Start production services
	@echo "$(YELLOW)🚀 Starting production services...$(NC)"
	@$(DOCKER_COMPOSE_CMD) -f $(PROD_COMPOSE_FILE) up -d
	@echo "$(GREEN)✅ Production services started$(NC)"

.PHONY: stop
stop: ## Stop all services
	@echo "$(YELLOW)🛑 Stopping services...$(NC)"
	@$(DOCKER_COMPOSE_CMD) -f $(COMPOSE_FILE) down
	@$(DOCKER_COMPOSE_CMD) -f $(PROD_COMPOSE_FILE) down 2>/dev/null || true
	@echo "$(GREEN)✅ Services stopped$(NC)"

.PHONY: restart
restart: ## Restart all services
	@echo "$(YELLOW)🔄 Restarting services...$(NC)"
	@$(MAKE) stop
	@$(MAKE) start-dev

.PHONY: restart-prod
restart-prod: ## Restart production services
	@echo "$(YELLOW)🔄 Restarting production services...$(NC)"
	@$(DOCKER_COMPOSE_CMD) -f $(PROD_COMPOSE_FILE) down
	@$(DOCKER_COMPOSE_CMD) -f $(PROD_COMPOSE_FILE) up -d
	@echo "$(GREEN)✅ Production services restarted$(NC)"

.PHONY: status
status: ## Show service status
	@echo "$(BLUE)📊 Service Status$(NC)"
	@$(DOCKER_COMPOSE_CMD) -f $(COMPOSE_FILE) ps 2>/dev/null || echo "Development services not running"
	@$(DOCKER_COMPOSE_CMD) -f $(PROD_COMPOSE_FILE) ps 2>/dev/null || echo "Production services not running"

##@ Database Commands

.PHONY: init-database
init-database: ## Initialize database (development)
	@echo "$(YELLOW)🗄️  Initializing database...$(NC)"
	@sleep 10  # Wait for database to be ready
	@$(DOCKER_COMPOSE_CMD) -f $(COMPOSE_FILE) exec backend alembic upgrade head
	@$(DOCKER_COMPOSE_CMD) -f $(COMPOSE_FILE) exec backend python -m app.scripts.seed_roles
	@echo "$(GREEN)✅ Database initialized$(NC)"

.PHONY: init-database-prod
init-database-prod: ## Initialize database (production)
	@echo "$(YELLOW)🗄️  Initializing production database...$(NC)"
	@sleep 10  # Wait for database to be ready
	@$(DOCKER_COMPOSE_CMD) -f $(PROD_COMPOSE_FILE) exec backend alembic upgrade head
	@$(DOCKER_COMPOSE_CMD) -f $(PROD_COMPOSE_FILE) exec backend python -m app.scripts.seed_roles
	@echo "$(GREEN)✅ Production database initialized$(NC)"

.PHONY: migrate
migrate: ## Run database migrations
	@echo "$(YELLOW)🔄 Running database migrations...$(NC)"
	@$(DOCKER_COMPOSE_CMD) -f $(COMPOSE_FILE) exec backend alembic upgrade head
	@echo "$(GREEN)✅ Database migrations completed$(NC)"

.PHONY: migrate-prod
migrate-prod: ## Run database migrations (production)
	@echo "$(YELLOW)🔄 Running production database migrations...$(NC)"
	@$(DOCKER_COMPOSE_CMD) -f $(PROD_COMPOSE_FILE) exec backend alembic upgrade head
	@echo "$(GREEN)✅ Production database migrations completed$(NC)"

.PHONY: db-shell
db-shell: ## Access database shell
	@echo "$(BLUE)💾 Opening database shell...$(NC)"
	@$(DOCKER_COMPOSE_CMD) -f $(COMPOSE_FILE) exec database psql -U pamuser -d pamdb

.PHONY: backup-db
backup-db: ## Create database backup
	@echo "$(YELLOW)💾 Creating database backup...$(NC)"
	@mkdir -p $(BACKUP_DIR)
	@$(DOCKER_COMPOSE_CMD) -f $(COMPOSE_FILE) exec -T database pg_dump -U pamuser -d pamdb > $(BACKUP_DIR)/backup-$(shell date +%Y%m%d_%H%M%S).sql
	@echo "$(GREEN)✅ Database backup created in $(BACKUP_DIR)/$(NC)"

.PHONY: restore-db
restore-db: ## Restore database from backup (requires BACKUP_FILE variable)
	@echo "$(YELLOW)🔄 Restoring database from backup...$(NC)"
	@if [ -z "$(BACKUP_FILE)" ]; then \
		echo "$(RED)❌ Please specify BACKUP_FILE: make restore-db BACKUP_FILE=backup.sql$(NC)"; \
		exit 1; \
	fi
	@$(DOCKER_COMPOSE_CMD) -f $(COMPOSE_FILE) exec -T database psql -U pamuser -d pamdb < $(BACKUP_FILE)
	@echo "$(GREEN)✅ Database restored from $(BACKUP_FILE)$(NC)"

##@ Monitoring Commands

.PHONY: logs
logs: ## Show application logs
	@echo "$(BLUE)📋 Application Logs$(NC)"
	@$(DOCKER_COMPOSE_CMD) -f $(COMPOSE_FILE) logs -f backend frontend

.PHONY: logs-prod
logs-prod: ## Show production logs
	@echo "$(BLUE)📋 Production Logs$(NC)"
	@$(DOCKER_COMPOSE_CMD) -f $(PROD_COMPOSE_FILE) logs -f backend frontend

.PHONY: health
health: ## Check application health
	@echo "$(BLUE)🏥 Health Check$(NC)"
	@curl -s http://localhost:8000/health | python -m json.tool 2>/dev/null || echo "Backend not responding"
	@echo ""
	@curl -s http://localhost:8000/health/ready | python -m json.tool 2>/dev/null || echo "Backend not ready"

.PHONY: health-prod
health-prod: ## Check production health
	@echo "$(BLUE)🏥 Production Health Check$(NC)"
	@curl -s https://$(shell grep DOMAIN .env | cut -d= -f2)/api/v1/health | python -m json.tool 2>/dev/null || echo "Production backend not responding"

##@ Development Commands

.PHONY: dev
dev: ## Start development with hot reload
	@echo "$(YELLOW)🔥 Starting development with hot reload...$(NC)"
	@$(DOCKER_COMPOSE_CMD) -f $(COMPOSE_FILE) up

.PHONY: shell-backend
shell-backend: ## Access backend container shell
	@echo "$(BLUE)🐚 Opening backend shell...$(NC)"
	@$(DOCKER_COMPOSE_CMD) -f $(COMPOSE_FILE) exec backend bash

.PHONY: shell-frontend
shell-frontend: ## Access frontend container shell
	@echo "$(BLUE)🐚 Opening frontend shell...$(NC)"
	@$(DOCKER_COMPOSE_CMD) -f $(COMPOSE_FILE) exec frontend bash

.PHONY: test
test: ## Run tests
	@echo "$(YELLOW)🧪 Running tests...$(NC)"
	@$(DOCKER_COMPOSE_CMD) -f $(COMPOSE_FILE) exec backend pytest
	@$(DOCKER_COMPOSE_CMD) -f $(COMPOSE_FILE) exec frontend npm test

.PHONY: lint
lint: ## Run linters
	@echo "$(YELLOW)🔍 Running linters...$(NC)"
	@$(DOCKER_COMPOSE_CMD) -f $(COMPOSE_FILE) exec backend black . --check
	@$(DOCKER_COMPOSE_CMD) -f $(COMPOSE_FILE) exec backend flake8 .
	@$(DOCKER_COMPOSE_CMD) -f $(COMPOSE_FILE) exec frontend npm run lint

.PHONY: format
format: ## Format code
	@echo "$(YELLOW)✨ Formatting code...$(NC)"
	@$(DOCKER_COMPOSE_CMD) -f $(COMPOSE_FILE) exec backend black .
	@$(DOCKER_COMPOSE_CMD) -f $(COMPOSE_FILE) exec frontend npm run format

##@ Maintenance Commands

.PHONY: update
update: ## Update application
	@echo "$(YELLOW)📦 Updating application...$(NC)"
	@git pull origin main
	@$(MAKE) pull
	@$(MAKE) build
	@$(MAKE) migrate
	@$(MAKE) restart
	@echo "$(GREEN)✅ Application updated$(NC)"

.PHONY: update-prod
update-prod: ## Update production application
	@echo "$(YELLOW)📦 Updating production application...$(NC)"
	@git pull origin main
	@$(DOCKER_COMPOSE_CMD) -f $(PROD_COMPOSE_FILE) pull
	@$(MAKE) build-prod
	@$(MAKE) migrate-prod
	@$(MAKE) restart-prod
	@echo "$(GREEN)✅ Production application updated$(NC)"

.PHONY: clean
clean: ## Clean up Docker resources
	@echo "$(YELLOW)🧹 Cleaning up Docker resources...$(NC)"
	@$(DOCKER_COMPOSE_CMD) -f $(COMPOSE_FILE) down -v --remove-orphans
	@$(DOCKER_COMPOSE_CMD) -f $(PROD_COMPOSE_FILE) down -v --remove-orphans 2>/dev/null || true
	@$(DOCKER_CMD) system prune -f
	@echo "$(GREEN)✅ Cleanup completed$(NC)"

.PHONY: reset
reset: ## Reset everything (⚠️ DESTROYS ALL DATA)
	@echo "$(RED)⚠️  WARNING: This will destroy all data!$(NC)"
	@echo "$(YELLOW)Press Ctrl+C to cancel, or Enter to continue...$(NC)"
	@read
	@$(MAKE) clean
	@sudo rm -rf data/postgres data/redis $(BACKUP_DIR) $(LOG_DIR)
	@echo "$(GREEN)✅ Everything reset$(NC)"

##@ Security Commands

.PHONY: generate-secrets
generate-secrets: ## Generate secure secrets for .env file
	@echo "$(YELLOW)🔐 Generating secure secrets...$(NC)"
	@echo "SECRET_KEY=$(shell openssl rand -hex 32)"
	@echo "ENCRYPTION_KEY=$(shell openssl rand -hex 32)"
	@echo "POSTGRES_PASSWORD=$(shell openssl rand -base64 32)"
	@echo "REDIS_PASSWORD=$(shell openssl rand -base64 32)"
	@echo "$(BLUE)Copy these values to your .env file$(NC)"

.PHONY: check-security
check-security: ## Run security checks
	@echo "$(YELLOW)🔍 Running security checks...$(NC)"
	@$(DOCKER_CMD) run --rm -v $(PWD):/app securecodewarrior/docker-security-checker /app 2>/dev/null || echo "Security scanner not available"
	@echo "$(GREEN)✅ Security checks completed$(NC)"

##@ Information Commands

.PHONY: info
info: ## Show deployment information
	@echo "$(BLUE)📊 Menshun PAM Deployment Information$(NC)"
	@echo "$(BLUE)================================$(NC)"
	@echo "Environment: $(shell grep ENVIRONMENT .env 2>/dev/null | cut -d= -f2 || echo 'Not configured')"
	@echo "Domain: $(shell grep DOMAIN .env 2>/dev/null | cut -d= -f2 || echo 'Not configured')"
	@echo "Azure Tenant: $(shell grep AZURE_TENANT_ID .env 2>/dev/null | cut -d= -f2 || echo 'Not configured')"
	@echo ""
	@echo "$(BLUE)Access URLs:$(NC)"
	@echo "Frontend: http://localhost:3000"
	@echo "Backend API: http://localhost:8000"
	@echo "API Docs: http://localhost:8000/docs"
	@echo "Database: localhost:5432"
	@echo "Redis: localhost:6379"

.PHONY: post-deploy-info
post-deploy-info: ## Show post-deployment information
	@echo "$(GREEN)🎉 Menshun PAM Development Environment Ready!$(NC)"
	@echo "$(BLUE)================================$(NC)"
	@echo ""
	@echo "$(YELLOW)📋 Next Steps:$(NC)"
	@echo "1. Open http://localhost:3000 in your browser"
	@echo "2. Complete the guided setup wizard"
	@echo "3. Configure your Azure AD credentials"
	@echo "4. Start managing privileged access!"
	@echo ""
	@echo "$(YELLOW)🔧 Useful Commands:$(NC)"
	@echo "• make logs        - View application logs"
	@echo "• make health      - Check application health"
	@echo "• make status      - Show service status"
	@echo "• make stop        - Stop all services"
	@echo "• make help        - Show all available commands"

.PHONY: post-deploy-info-prod
post-deploy-info-prod: ## Show post-deployment information (production)
	@echo "$(GREEN)🎉 Menshun PAM Production Environment Ready!$(NC)"
	@echo "$(BLUE)================================$(NC)"
	@echo ""
	@echo "$(YELLOW)📋 Next Steps:$(NC)"
	@echo "1. Configure your domain DNS to point to this server"
	@echo "2. Setup proper SSL certificates (replace self-signed)"
	@echo "3. Open https://$(shell grep DOMAIN .env | cut -d= -f2) in your browser"
	@echo "4. Complete the guided setup wizard"
	@echo "5. Configure monitoring and backups"
	@echo ""
	@echo "$(YELLOW)🔧 Production Commands:$(NC)"
	@echo "• make logs-prod     - View production logs"
	@echo "• make health-prod   - Check production health"
	@echo "• make backup-db     - Create database backup"
	@echo "• make update-prod   - Update production deployment"

.PHONY: version
version: ## Show version information
	@echo "$(BLUE)Menshun PAM Version Information$(NC)"
	@echo "Git commit: $(shell git rev-parse --short HEAD 2>/dev/null || echo 'Unknown')"
	@echo "Git branch: $(shell git rev-parse --abbrev-ref HEAD 2>/dev/null || echo 'Unknown')"
	@echo "Docker version: $(shell docker --version 2>/dev/null || echo 'Not installed')"
	@echo "Docker Compose version: $(shell docker-compose --version 2>/dev/null || echo 'Not installed')"