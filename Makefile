# SlotSwapper Docker Management Makefile

.PHONY: help build up down logs shell clean backup restore

# Default target
help: ## Show this help message
	@echo "SlotSwapper Docker Management Commands:"
	@echo ""
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

# Development commands
dev: ## Start development environment
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d

dev-build: ## Build and start development environment
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d --build

dev-logs: ## Show development logs
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml logs -f

dev-down: ## Stop development environment
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml down

# Production commands
prod: ## Start production environment
	docker-compose --profile production up -d

prod-build: ## Build and start production environment
	docker-compose --profile production up -d --build

prod-logs: ## Show production logs
	docker-compose --profile production logs -f

prod-down: ## Stop production environment
	docker-compose --profile production down

# General commands
build: ## Build all services
	docker-compose build

up: ## Start all services (default profile)
	docker-compose up -d

down: ## Stop all services
	docker-compose down

restart: ## Restart all services
	docker-compose restart

logs: ## Show logs for all services
	docker-compose logs -f

status: ## Show status of all services
	docker-compose ps

# Service-specific commands
backend-shell: ## Access backend container shell
	docker-compose exec backend bash

frontend-shell: ## Access frontend container shell
	docker-compose exec frontend sh

db-shell: ## Access database shell
	docker-compose exec database psql -U postgres -d slotswapper

redis-shell: ## Access Redis CLI
	docker-compose exec redis redis-cli

# Database commands
db-backup: ## Create database backup
	docker-compose exec database pg_dump -U postgres slotswapper > backup_$(shell date +%Y%m%d_%H%M%S).sql
	@echo "Database backup created: backup_$(shell date +%Y%m%d_%H%M%S).sql"

db-restore: ## Restore database from backup (usage: make db-restore FILE=backup.sql)
	@if [ -z "$(FILE)" ]; then echo "Usage: make db-restore FILE=backup.sql"; exit 1; fi
	docker-compose exec -T database psql -U postgres slotswapper < $(FILE)
	@echo "Database restored from: $(FILE)"

db-reset: ## Reset database (WARNING: This will delete all data)
	@echo "WARNING: This will delete all database data. Continue? [y/N]" && read ans && [ $${ans:-N} = y ]
	docker-compose down -v
	docker-compose up -d database
	@echo "Database reset complete"

# Migration commands
migrate: ## Run database migrations
	docker-compose exec backend alembic upgrade head

migrate-create: ## Create new migration (usage: make migrate-create MSG="description")
	@if [ -z "$(MSG)" ]; then echo "Usage: make migrate-create MSG='migration description'"; exit 1; fi
	docker-compose exec backend alembic revision --autogenerate -m "$(MSG)"

# Maintenance commands
clean: ## Clean up Docker resources
	docker system prune -f
	docker volume prune -f
	docker network prune -f

clean-all: ## Clean up all Docker resources (WARNING: removes all unused containers, images, networks)
	@echo "WARNING: This will remove all unused Docker resources. Continue? [y/N]" && read ans && [ $${ans:-N} = y ]
	docker system prune -a -f
	docker volume prune -f

update: ## Pull latest images and rebuild
	docker-compose pull
	docker-compose build --pull

# Health checks
health: ## Check health of all services
	@echo "Checking service health..."
	@docker-compose ps
	@echo ""
	@echo "Frontend health:"
	@curl -f http://localhost:3000/health 2>/dev/null && echo "✓ Frontend healthy" || echo "✗ Frontend unhealthy"
	@echo "Backend health:"
	@curl -f http://localhost:8000/health 2>/dev/null && echo "✓ Backend healthy" || echo "✗ Backend unhealthy"

# Monitoring
stats: ## Show resource usage statistics
	docker stats --no-stream

top: ## Show running processes in containers
	docker-compose top

# Setup commands
setup: ## Initial setup for development
	@echo "Setting up SlotSwapper development environment..."
	cp .env.example .env
	@echo "✓ Environment file created"
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml build
	@echo "✓ Services built"
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d
	@echo "✓ Services started"
	@echo ""
	@echo "Setup complete! Access the application at:"
	@echo "  Frontend: http://localhost:3000"
	@echo "  Backend:  http://localhost:8000"

setup-prod: ## Initial setup for production
	@echo "Setting up SlotSwapper production environment..."
	@if [ ! -f .env ]; then \
		echo "Creating production environment file..."; \
		cp .env.production .env; \
		echo "⚠️  Please edit .env with your production values before continuing"; \
		exit 1; \
	fi
	docker-compose --profile production build
	@echo "✓ Production services built"
	@echo "Ready for production deployment with: make prod"

# Testing
test-backend: ## Run backend tests
	docker-compose exec backend python -m pytest

test-frontend: ## Run frontend tests
	docker-compose exec frontend npm test

# SSL setup (for production)
ssl-setup: ## Setup SSL certificates (requires certbot)
	@echo "Setting up SSL certificates..."
	mkdir -p nginx/ssl
	# Add your SSL certificate setup commands here
	@echo "Please place your SSL certificates in nginx/ssl/"
	@echo "Required files: fullchain.pem, privkey.pem"
