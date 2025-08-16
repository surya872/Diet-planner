#!/bin/bash

# Render startup script for Diet Planner API
echo "🚀 Starting Diet Planner API on Render..."

# Debug environment variables
echo "🔍 Environment Debug:"
echo "APP_ENV: ${APP_ENV:-NOT_SET}"
echo "FLASK_ENV: ${FLASK_ENV:-NOT_SET}" 
echo "DATABASE_URL: ${DATABASE_URL:0:50}..." # Show first 50 chars only
echo "PORT: ${PORT:-NOT_SET}"

# Set environment variables
export PYTHONPATH=/app:$PYTHONPATH
export FLASK_APP=app.py

# Database migration (if needed)
echo "📊 Running database migrations..."
python -c "
import os
os.environ['FLASK_APP'] = 'app.py'
from app import app, db
with app.app_context():
    try:
        db.create_all()
        print('✅ Database tables created/updated')
    except Exception as e:
        print(f'⚠️ Database migration error (might be normal): {e}')
"

# Start the application with gunicorn
echo "🔥 Starting Gunicorn server on port ${PORT:-5000}..."
exec gunicorn \
    --bind 0.0.0.0:${PORT:-5000} \
    --workers 2 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    --log-level info \
    --preload \
    app:app
