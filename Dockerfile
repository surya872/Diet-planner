# Dockerfile for Render deployment - Backend only
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy backend requirements and install dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend application code
COPY backend/ .

# Create startup script
RUN chmod +x start-render.sh

# Expose port (Render sets this via $PORT)
EXPOSE $PORT

# Set environment variables
ENV PYTHONPATH=/app
ENV FLASK_APP=app.py

# Run database initialization and start server
CMD ["./start-render.sh"]
