#!/bin/bash

# Netlify Frontend Deployment Script
echo "🚀 Deploying Diet Planner Frontend to Netlify"

# Navigate to frontend directory
cd frontend

# Install dependencies
echo "📦 Installing dependencies..."
npm ci

# Run tests
echo "🧪 Running tests..."
npm test -- --coverage --watchAll=false

# Build the application
echo "🔨 Building production bundle..."
npm run build

# Check build size
echo "📊 Build size analysis:"
du -sh build/

echo "✅ Frontend ready for Netlify deployment!"
echo ""
echo "Next steps:"
echo "1. Push to GitHub"
echo "2. Connect repository to Netlify"
echo "3. Set build command: npm run build"
echo "4. Set publish directory: build"
echo "5. Set environment variable: REACT_APP_API_URL"
echo ""
echo "🌐 Deploy backend to Render/Railway first, then update REACT_APP_API_URL"
