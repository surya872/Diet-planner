#!/bin/bash

# Test script for frontend
set -e

echo "🧪 Running Frontend Tests..."

# Install dependencies if not already installed
npm ci

# Run TypeScript type checking
echo "🔍 Running TypeScript type checking..."
npx tsc --noEmit

# Run ESLint
echo "📝 Running ESLint..."
npm run lint || echo "⚠️ ESLint warnings found"

# Run unit tests with coverage
echo "🔬 Running unit tests with coverage..."
npm test -- --coverage --watchAll=false --verbose

# Optional: Run visual regression tests (if configured)
# echo "👀 Running visual regression tests..."
# npm run test:visual || echo "⚠️ Visual tests not configured"

echo "✅ All frontend tests completed!"
