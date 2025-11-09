"""
Gunicorn configuration file for production deployment
ملف تكوين Gunicorn للنشر الإنتاجي
"""
import multiprocessing
import os

# Server socket
bind = "0.0.0.0:" + str(os.environ.get("PORT", "8000"))
backlog = 2048

# Worker processes
# Default to 1 worker for free tier (512MB RAM) to stay within memory limits
# Can be overridden by setting WEB_CONCURRENCY environment variable
# For production with more memory, consider: workers = (2 * cpu_count) + 1
workers = int(os.environ.get("WEB_CONCURRENCY", 1))
worker_class = "sync"
worker_connections = 1000
timeout = 120
keepalive = 5

# Logging
accesslog = "-"  # stdout
errorlog = "-"   # stderr
loglevel = os.environ.get("LOG_LEVEL", "info")
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Process naming
proc_name = "housing_system"

# Server mechanics
daemon = False
tmp_upload_dir = None

# Security
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190

# Preload app for better performance
preload_app = True

# Worker lifecycle hooks
def on_starting(server):
    """Called just before the master process is initialized."""
    print("🚀 Starting Housing Management System...")

def on_reload(server):
    """Called to recycle workers during a reload via SIGHUP."""
    print("♻️  Reloading Housing Management System...")

def when_ready(server):
    """Called just after the server is started."""
    print("✅ Housing Management System is ready!")
    print(f"   Workers: {workers}")
    print(f"   Binding: {bind}")

def on_exit(server):
    """Called just before exiting Gunicorn."""
    print("👋 Shutting down Housing Management System...")
