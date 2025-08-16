#!/bin/bash

# Render startup script for Diet Planner API
echo "🚀 Starting Diet Planner API on Render..."

# Set Python path
export PYTHONPATH=/opt/render/project/src/backend:$PYTHONPATH

# Database migration (if needed)
echo "📊 Running database migrations..."
python -c "
from app import app, db
with app.app_context():
    db.create_all()
    print('✅ Database tables created/updated')
"

# Start the application with gunicorn
echo "🔥 Starting Gunicorn server..."
exec gunicorn \
    --bind 0.0.0.0:$PORT \
    --workers 2 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    --log-level info \
    app:app
