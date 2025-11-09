#!/bin/sh
# Startup script for Fly.io deployment

# Initialize database
echo "🔄 Initializing database..."
python3 database.py

# Start gunicorn with explicit configuration
echo "🚀 Starting application server..."
exec gunicorn \
    --bind 0.0.0.0:${PORT:-8000} \
    --workers 1 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    --log-level info \
    server:app
