#!/bin/bash

# Test script for backend
set -e

echo "🧪 Running Backend Tests..."

# Activate virtual environment
source venv/bin/activate

# Install dependencies if not already installed
pip install -r requirements.txt

# Run code quality checks
echo "📝 Running code quality checks..."
flake8 app.py tests/
black --check app.py tests/
isort --check-only app.py tests/

# Run type checking
echo "🔍 Running type checking..."
mypy app.py --ignore-missing-imports

# Run unit tests
echo "🔬 Running unit tests..."
pytest tests/unit/ -v --cov=app --cov-report=html --cov-report=term-missing --cov-fail-under=80

# Run integration tests
echo "🔧 Running integration tests..."
pytest tests/integration/ -v

# Run all tests with coverage
echo "📊 Running all tests with coverage..."
pytest tests/ -v --cov=app --cov-report=html --cov-report=term-missing

echo "✅ All backend tests passed!"
