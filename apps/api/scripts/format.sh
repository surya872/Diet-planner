#!/bin/bash

# Code formatting script for backend
set -e

echo "🎨 Formatting Backend Code..."

# Activate virtual environment
source venv/bin/activate

# Install dependencies if not already installed
pip install -r requirements.txt

# Sort imports
echo "📚 Sorting imports..."
isort app.py tests/

# Format code with black
echo "🖤 Formatting code with black..."
black app.py tests/

# Run flake8 to check for any remaining issues
echo "📝 Running flake8 linting..."
flake8 app.py tests/

echo "✅ Code formatting completed!"
