#!/bin/bash

echo "🍎 Starting Diet Planner Application..."
echo "======================================"

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating from example..."
    cp env.example .env
    echo "❌ Please edit .env file with your Gemini API key before running again."
    exit 1
fi

# Check database connection
echo "🔍 Checking database connection..."
if ! pg_isready -h localhost -p 5432 -U diet_user -d diet_planner > /dev/null 2>&1; then
    echo "❌ Cannot connect to database. Run ./setup_database.sh first."
    exit 1
fi
echo "✅ Database connection successful"

echo ""
echo "🚀 Starting services..."
echo ""

# Start backend in a new terminal window
echo "📡 Starting Backend (Terminal 1)..."
osascript -e 'tell app "Terminal" to do script "cd \"'$(pwd)'/backend\" && source venv/bin/activate && python app.py"'

# Wait a moment for backend to start
sleep 3

# Start frontend in a new terminal window
echo "🌐 Starting Frontend (Terminal 2)..."
osascript -e 'tell app "Terminal" to do script "cd \"'$(pwd)'/frontend\" && npm start"'

echo ""
echo "✅ Services started!"
echo ""
echo "📱 Frontend: http://localhost:3001"
echo "🔧 Backend: http://localhost:5001"
echo "🗄️  Database: localhost:5432"
echo ""
echo "💡 The application will open in your browser automatically."
echo "   Press Ctrl+C in each terminal to stop the services."
