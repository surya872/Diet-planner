# Diet Planner Setup Guide

This guide will help you set up and run the Diet Planner application on your local machine.

## Prerequisites

Before you begin, make sure you have the following installed:

- **Docker** and **Docker Compose** (recommended)
- **Node.js** (v16 or higher) - for local frontend development
- **Python** (3.8 or higher) - for local backend development
- **PostgreSQL** - for local database development

## Quick Start (Docker)

### 1. Clone and Setup

```bash
# Clone the repository (if not already done)
git clone <repository-url>
cd diet-planner

# Copy environment file
cp env.example .env
```

### 2. Configure Environment Variables

Edit the `.env` file with your actual values:

```env
# Database Configuration
POSTGRES_DB=diet_planner
POSTGRES_USER=diet_user
POSTGRES_PASSWORD=your_secure_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# Gemini AI Configuration (REQUIRED)
GEMINI_API_KEY=your_actual_gemini_api_key

# Flask Configuration
FLASK_SECRET_KEY=your_secret_key_here
FLASK_ENV=development

# Frontend Configuration (optional)
REACT_APP_API_URL=http://localhost:5000/api
```

### 3. Get Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Create a new API key
4. Copy the key and paste it in your `.env` file

### 4. Run the Application

```bash
# Make the startup script executable (if not already done)
chmod +x start.sh

# Run the application
./start.sh
```

Or manually:

```bash
docker-compose up --build -d
```

### 5. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000
- **Database**: localhost:5432

## Local Development Setup

If you prefer to run the application locally without Docker:

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export GEMINI_API_KEY=your_api_key
export POSTGRES_DB=diet_planner
export POSTGRES_USER=diet_user
export POSTGRES_PASSWORD=your_password
export POSTGRES_HOST=localhost
export POSTGRES_PORT=5432

# Run the backend
python app.py
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

### Database Setup

1. Install PostgreSQL
2. Create a database named `diet_planner`
3. Run the initialization script:

```bash
psql -d diet_planner -f database/init.sql
```

## API Endpoints

### Health Check
- `GET /api/health` - Check if the API is running

### Users
- `POST /api/users` - Create a new user
- `GET /api/users/<user_id>` - Get user by ID

### Diet Plans
- `POST /api/diet-plan` - Generate a new diet plan
- `GET /api/diet-plan/<user_id>` - Get all diet plans for a user
- `GET /api/diet-plan/<plan_id>` - Get a specific diet plan

## Troubleshooting

### Common Issues

1. **Docker not running**
   - Make sure Docker Desktop is started
   - Check if Docker daemon is running

2. **Port conflicts**
   - Make sure ports 3000, 5000, and 5432 are available
   - Stop any existing services using these ports

3. **Gemini API errors**
   - Verify your API key is correct
   - Check if you have sufficient API quota
   - Ensure the API key has the necessary permissions

4. **Database connection issues**
   - Check if PostgreSQL is running
   - Verify database credentials in `.env`
   - Ensure the database exists

### Logs

View application logs:

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f postgres
```

### Reset Database

To reset the database and start fresh:

```bash
# Stop containers
docker-compose down

# Remove volumes
docker-compose down -v

# Start again
docker-compose up --build -d
```

## Features

- **User Registration**: Collect user information (age, gender, weight, diet preferences)
- **AI-Powered Diet Plans**: Generate personalized 1-week meal plans using Gemini AI
- **Nutritional Information**: Detailed breakdown of calories, protein, carbs, and fat
- **Multiple Diet Types**: Support for various dietary preferences
- **Responsive Design**: Works on desktop and mobile devices
- **Modern UI**: Beautiful, intuitive interface

## Technology Stack

- **Frontend**: React.js with TypeScript, Tailwind CSS
- **Backend**: Python Flask with SQLAlchemy
- **Database**: PostgreSQL
- **AI**: Google Gemini LLM
- **Deployment**: Docker and Docker Compose

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License.
