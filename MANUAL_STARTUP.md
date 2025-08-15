# Manual Startup Guide (Without Docker)

This guide shows you how to run the Diet Planner application locally without Docker.

## Prerequisites

- ✅ PostgreSQL database set up (run `./setup_database.sh` first)
- ✅ Python 3.8+ installed
- ✅ Node.js 16+ installed
- ✅ Gemini API key

## Step 1: Get Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Create a new API key
4. Copy the key

## Step 2: Configure Environment

Edit the `.env` file in the root directory:

```env
# Database Configuration
POSTGRES_DB=diet_planner
POSTGRES_USER=diet_user
POSTGRES_PASSWORD=diet_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# Gemini AI Configuration (REQUIRED)
GEMINI_API_KEY=your_actual_gemini_api_key_here

# Flask Configuration
FLASK_SECRET_KEY=your_secret_key_here
FLASK_ENV=development

# Frontend Configuration (optional)
REACT_APP_API_URL=http://localhost:5000/api
```

## Step 3: Quick Start (Recommended)

```bash
# Run the automated startup script
./start_local.sh
```

This script will:
- ✅ Check database connection
- ✅ Start Python backend
- ✅ Start React frontend
- ✅ Open both services in your browser

## Step 4: Manual Start (Alternative)

If you prefer to start services manually:

### Start Backend (Terminal 1)
```bash
cd backend
source venv/bin/activate
python app.py
```

### Start Frontend (Terminal 2)
```bash
cd frontend
npm start
```

## Access the Application

- **Frontend**: http://localhost:3001
- **Backend API**: http://localhost:5001
- **Health Check**: http://localhost:5001/api/health

## Troubleshooting

### Backend Issues
```bash
# Check if virtual environment is activated
which python
# Should show: /path/to/diet-planner/backend/venv/bin/python

# Reinstall dependencies if needed
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

### Frontend Issues
```bash
# Clear npm cache
cd frontend
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

### Database Issues
```bash
# Check database connection
psql -U diet_user -d diet_planner -c "SELECT 1;"

# Reset database if needed
./setup_database.sh
```

### Port Conflicts
If ports 3001 or 5001 are in use:
```bash
# Find processes using the ports
lsof -i :3001
lsof -i :5001

# Kill the processes
kill -9 <PID>
```

## Stopping the Application

### If using start_local.sh
Press `Ctrl+C` in the terminal

### If started manually
Press `Ctrl+C` in each terminal window

## Development Tips

### Backend Development
- Backend auto-reloads on file changes
- Check logs in the terminal for errors
- API endpoints: http://localhost:5001/api/health

### Frontend Development
- Frontend auto-reloads on file changes
- Check browser console for errors
- Hot reload enabled

### Database Management
```bash
# Use the database management tool
./manage_database.sh

# Or connect directly
psql -U diet_user -d diet_planner
```

## Environment Variables

Key environment variables you might need to modify:

- `GEMINI_API_KEY`: Your Google Gemini API key
- `POSTGRES_PASSWORD`: Database password
- `FLASK_SECRET_KEY`: Secret key for Flask sessions
- `FLASK_ENV`: Set to 'development' for debug mode

## Next Steps

1. Open http://localhost:3000 in your browser
2. Fill out the user registration form
3. Generate your first AI-powered diet plan!
4. Explore the application features

Happy diet planning! 🍎
