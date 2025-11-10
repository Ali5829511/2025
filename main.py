from flask import Flask, render_template, send_from_directory, abort
from flask_cors import CORS
from werkzeug.security import safe_join
import os

# Configure Flask to serve files from current directory
app = Flask(__name__, static_folder='.', template_folder='.')
CORS(app)

# Define the base directory for serving files
BASE_DIR = os.path.abspath('.')

# Define allowed file extensions for security
ALLOWED_EXTENSIONS = {'.html', '.css', '.js', '.png', '.jpg', '.jpeg', '.gif', '.svg', '.pdf', '.md'}

def is_safe_path(filename):
    """Check if the requested file is safe to serve"""
    # Prevent directory traversal
    if '..' in filename or filename.startswith('/'):
        return False
    
    # Block sensitive files
    blocked_files = {'.env', '.git', '__pycache__', 'requirements.txt', '.gitignore', '.py'}
    if any(blocked in filename for blocked in blocked_files):
        return False
    
    # Check file extension
    _, ext = os.path.splitext(filename)
    if ext.lower() not in ALLOWED_EXTENSIONS:
        return False
    
    return True

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    if not is_safe_path(filename):
        abort(403)
    
    # Use safe_join to prevent path traversal attacks
    safe_path = safe_join(BASE_DIR, filename)
    if safe_path is None or not os.path.isfile(safe_path):
        abort(404)
        
    return send_from_directory('.', filename)

if __name__ == '__main__':
    # Get debug mode from environment variable (default: False for security)
    # Set FLASK_DEBUG=True explicitly for development
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=5000, debug=debug_mode)

