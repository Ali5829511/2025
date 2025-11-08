# Dockerfile for Housing Management System
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir gunicorn psycopg2-binary

# Copy application files
COPY . .

# Make start script executable
RUN chmod +x start.sh

# Create logs directory
RUN mkdir -p logs

# Create non-root user
RUN useradd -m -u 1000 housing && \
    chown -R housing:housing /app

USER housing

# Expose port
EXPOSE 8000

# Health check - using curl instead of python requests for reliability
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/api/health || exit 1

# Initialize database and start server
CMD ["./start.sh"]
