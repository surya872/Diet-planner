# Diet Planner Application Makefile
# Enterprise-level SDLC automation

.PHONY: help install test test-backend test-frontend lint lint-backend lint-frontend format format-backend format-frontend setup-db migrate clean build deploy dev

# Default target
help:
	@echo "🍎 Diet Planner Application Commands"
	@echo ""
	@echo "📦 Setup Commands:"
	@echo "  install          Install all dependencies (backend + frontend)"
	@echo "  setup-db         Set up the database"
	@echo "  migrate          Run database migrations"
	@echo ""
	@echo "🧪 Testing Commands:"
	@echo "  test             Run all tests (backend + frontend)"
	@echo "  test-backend     Run backend tests only"
	@echo "  test-frontend    Run frontend tests only"
	@echo "  test-integration Run integration tests"
	@echo "  test-e2e         Run end-to-end tests"
	@echo ""
	@echo "📝 Code Quality Commands:"
	@echo "  lint             Run linting for all code"
	@echo "  lint-backend     Run backend linting"
	@echo "  lint-frontend    Run frontend linting"
	@echo "  format           Format all code"
	@echo "  format-backend   Format backend code"
	@echo "  format-frontend  Format frontend code"
	@echo ""
	@echo "🏗️  Build Commands:"
	@echo "  build            Build all applications"
	@echo "  build-backend    Build backend application"
	@echo "  build-frontend   Build frontend application"
	@echo ""
	@echo "🚀 Development Commands:"
	@echo "  dev              Start development servers"
	@echo "  dev-backend      Start backend development server"
	@echo "  dev-frontend     Start frontend development server"
	@echo ""
	@echo "🧹 Maintenance Commands:"
	@echo "  clean            Clean all build artifacts"
	@echo "  clean-backend    Clean backend artifacts"
	@echo "  clean-frontend   Clean frontend artifacts"

# Installation Commands
install: install-backend install-frontend
	@echo "✅ All dependencies installed successfully!"

install-backend:
	@echo "📦 Installing backend dependencies..."
	cd backend && python -m venv venv
	cd backend && source venv/bin/activate && pip install --upgrade pip
	cd backend && source venv/bin/activate && pip install -r requirements.txt

install-frontend:
	@echo "📦 Installing frontend dependencies..."
	cd frontend && npm ci

# Database Commands
setup-db:
	@echo "🗄️ Setting up database..."
	chmod +x setup_database.sh
	./setup_database.sh

migrate:
	@echo "🔄 Running database migrations..."
	psql -U diet_user -d diet_planner -f database/add_password_migration.sql

# Testing Commands
test: test-backend test-frontend
	@echo "✅ All tests completed!"

test-backend:
	@echo "🧪 Running backend tests..."
	chmod +x backend/scripts/test.sh
	cd backend && ./scripts/test.sh

test-frontend:
	@echo "🧪 Running frontend tests..."
	chmod +x frontend/scripts/test.sh
	cd frontend && ./scripts/test.sh

test-integration:
	@echo "🔧 Running integration tests..."
	cd backend && source venv/bin/activate && pytest tests/integration/ -v

test-e2e:
	@echo "🎭 Running end-to-end tests..."
	cd backend && source venv/bin/activate && pytest tests/e2e/ -v

# Code Quality Commands
lint: lint-backend lint-frontend
	@echo "✅ All linting completed!"

lint-backend:
	@echo "📝 Running backend linting..."
	cd backend && source venv/bin/activate && flake8 app.py tests/
	cd backend && source venv/bin/activate && mypy app.py --ignore-missing-imports

lint-frontend:
	@echo "📝 Running frontend linting..."
	cd frontend && npm run lint || true
	cd frontend && npx tsc --noEmit

format: format-backend format-frontend
	@echo "✅ All code formatted!"

format-backend:
	@echo "🎨 Formatting backend code..."
	chmod +x backend/scripts/format.sh
	cd backend && ./scripts/format.sh

format-frontend:
	@echo "🎨 Formatting frontend code..."
	cd frontend && npx prettier --write "src/**/*.{ts,tsx,js,jsx,css,scss,json}"

# Build Commands
build: build-backend build-frontend
	@echo "✅ All applications built!"

build-backend:
	@echo "🏗️ Building backend application..."
	cd backend && docker build -t diet-planner-backend:latest .

build-frontend:
	@echo "🏗️ Building frontend application..."
	cd frontend && npm run build
	cd frontend && docker build -t diet-planner-frontend:latest .

# Development Commands
dev:
	@echo "🚀 Starting development servers..."
	@echo "Run 'make dev-backend' and 'make dev-frontend' in separate terminals"

dev-backend:
	@echo "🚀 Starting backend development server..."
	cd backend && source venv/bin/activate && python app.py

dev-frontend:
	@echo "🚀 Starting frontend development server..."
	cd frontend && npm start

# Maintenance Commands
clean: clean-backend clean-frontend
	@echo "✅ All artifacts cleaned!"

clean-backend:
	@echo "🧹 Cleaning backend artifacts..."
	cd backend && rm -rf __pycache__ .pytest_cache .coverage htmlcov *.egg-info
	cd backend && find . -type d -name __pycache__ -exec rm -rf {} +
	cd backend && find . -name "*.pyc" -delete

clean-frontend:
	@echo "🧹 Cleaning frontend artifacts..."
	cd frontend && rm -rf build coverage

# Security Commands
security-scan:
	@echo "🔒 Running security scans..."
	cd backend && source venv/bin/activate && safety check
	cd backend && source venv/bin/activate && bandit -r app.py
	cd frontend && npm audit

# Coverage Commands
coverage:
	@echo "📊 Generating coverage reports..."
	cd backend && source venv/bin/activate && pytest --cov=app --cov-report=html --cov-report=term-missing
	cd frontend && npm test -- --coverage --watchAll=false

# Docker Commands
docker-build:
	@echo "🐳 Building Docker images..."
	docker-compose build

docker-up:
	@echo "🐳 Starting Docker containers..."
	docker-compose up -d

docker-down:
	@echo "🐳 Stopping Docker containers..."
	docker-compose down

docker-logs:
	@echo "🐳 Showing Docker logs..."
	docker-compose logs -f

# Pre-commit Commands
pre-commit: format lint test
	@echo "✅ Pre-commit checks completed!"

# CI/CD Commands
ci: install lint test security-scan coverage
	@echo "✅ CI pipeline completed!"

# Health Check
health:
	@echo "🏥 Checking application health..."
	curl -f http://localhost:5001/api/health || echo "❌ Backend not running"
	curl -f http://localhost:3001 || echo "❌ Frontend not running"
