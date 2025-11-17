"""
Gunicorn configuration for Traffic Violations Management System
تكوين Gunicorn لنظام إدارة المخالفات المرورية
"""
import os
import multiprocessing

# Server socket
bind = f"0.0.0.0:{os.environ.get('PORT', '10000')}"
backlog = 2048

# Worker processes
workers = int(os.environ.get('GUNICORN_WORKERS', multiprocessing.cpu_count() * 2 + 1))
worker_class = 'sync'
worker_connections = 1000
timeout = 120
keepalive = 5
max_requests = 1000
max_requests_jitter = 50

# Logging
accesslog = '-'
errorlog = '-'
loglevel = 'info'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Process naming
proc_name = 'traffic-violations-system'

# Server mechanics
daemon = False
pidfile = None
user = None
group = None
tmp_upload_dir = None

# Graceful timeout for worker shutdown
graceful_timeout = 30

# Preload app for better performance
preload_app = True

def on_starting(server):
    """Called just before the master process is initialized"""
    print("\n" + "="*60)
    print("🚀 نظام إدارة المخالفات المرورية")
    print("🚀 Traffic Violations Management System")
    print("="*60)
    print(f"\n✅ Starting Gunicorn server")
    print(f"✅ Workers: {workers}")
    print(f"✅ Binding to: {bind}")
    print(f"✅ Timeout: {timeout}s")
    print("="*60 + "\n")

def on_exit(server):
    """Called just after the master process exits"""
    print("\n✅ Server stopped gracefully\n")

def worker_int(worker):
    """Called when a worker receives a SIGINT or SIGQUIT signal"""
    print(f"✅ Worker {worker.pid} shutting down gracefully")

def worker_abort(worker):
    """Called when a worker receives a SIGABRT signal"""
    print(f"⚠️ Worker {worker.pid} aborted")
