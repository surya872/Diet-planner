#!/bin/bash

echo "🍎 Starting Diet Planner Application (Local Mode)..."
echo "=================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if .env file exists
if [ ! -f .env ]; then
    echo -e "${YELLOW}⚠️  .env file not found. Creating from example...${NC}"
    cp env.example .env
    echo -e "${RED}❌ Please edit .env file with your actual values before running again.${NC}"
    echo "   - Add your Gemini API key"
    echo "   - Set secure database passwords"
    exit 1
fi

# Check if PostgreSQL is running
echo -e "${BLUE}🔍 Checking PostgreSQL connection...${NC}"
if ! pg_isready -h localhost -p 5432 -U diet_user -d diet_planner > /dev/null 2>&1; then
    echo -e "${RED}❌ Cannot connect to PostgreSQL database${NC}"
    echo "Please make sure:"
    echo "1. PostgreSQL is running"
    echo "2. Database 'diet_planner' exists"
    echo "3. User 'diet_user' has proper permissions"
    echo ""
    echo "Run: ./setup_database.sh to set up the database"
    exit 1
fi
echo -e "${GREEN}✅ PostgreSQL connection successful${NC}"

# Function to start backend
start_backend() {
    echo -e "${BLUE}🚀 Starting Python Backend...${NC}"
    cd backend
    
    # Check if virtual environment exists
    if [ ! -d "venv" ]; then
        echo -e "${YELLOW}⚠️  Virtual environment not found. Creating...${NC}"
        python -m venv venv
    fi
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Install dependencies if needed
    if [ ! -f "venv/lib/python*/site-packages/flask" ]; then
        echo -e "${YELLOW}📦 Installing Python dependencies...${NC}"
        pip install -r requirements.txt
    fi
    
    # Start Flask backend
    echo -e "${GREEN}✅ Backend starting on http://localhost:5001${NC}"
    python app.py &
    BACKEND_PID=$!
    cd ..
}

# Function to start frontend
start_frontend() {
    echo -e "${BLUE}🚀 Starting React Frontend...${NC}"
    cd frontend
    
    # Check if node_modules exists
    if [ ! -d "node_modules" ]; then
        echo -e "${YELLOW}📦 Installing Node.js dependencies...${NC}"
        npm install
    fi
    
    # Start React development server
    echo -e "${GREEN}✅ Frontend starting on http://localhost:3000${NC}"
    npm start &
    FRONTEND_PID=$!
    cd ..
}

# Function to cleanup on exit
cleanup() {
    echo ""
    echo -e "${YELLOW}🛑 Stopping services...${NC}"
    if [ ! -z "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null
        echo "Backend stopped"
    fi
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null
        echo "Frontend stopped"
    fi
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Start services
start_backend
sleep 3  # Give backend time to start

start_frontend
sleep 3  # Give frontend time to start

echo ""
echo -e "${GREEN}🎉 Diet Planner Application is running!${NC}"
echo ""
echo "📱 Frontend: http://localhost:3001"
echo "🔧 Backend API: http://localhost:5001"
echo "🗄️  Database: localhost:5432"
echo ""
echo -e "${YELLOW}Press Ctrl+C to stop all services${NC}"
echo ""

# Wait for user to stop
wait
