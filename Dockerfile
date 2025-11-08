# Dockerfile for Housing Management System - Fly.io Optimized
# ملف Docker لنظام إدارة الإسكان - محسّن لـ Fly.io
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir gunicorn psycopg2-binary

# Copy application files
COPY . .

# Create logs directory
RUN mkdir -p logs

# Create non-root user
RUN useradd -m -u 1000 housing && \
    chown -R housing:housing /app

USER housing

# Expose port 8000 (required by Fly.io configuration)
# كشف المنفذ 8000 (مطلوب من تكوين Fly.io)
EXPOSE 8000

# Set environment variables for Fly.io
# تعيين متغيرات البيئة لـ Fly.io
ENV PORT=8000
ENV HOST=0.0.0.0
ENV FLASK_ENV=production
ENV FLASK_DEBUG=False

# Health check on port 8000
# فحص الصحة على المنفذ 8000
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python3 -c "import requests; requests.get('http://localhost:8000/api/health', timeout=5)" || exit 1

# Initialize database and start server with Gunicorn on port 8000
# تهيئة قاعدة البيانات وبدء الخادم مع Gunicorn على المنفذ 8000
CMD python3 database.py && gunicorn --config gunicorn_config.py server:app
