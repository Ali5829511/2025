from flask import Flask, render_template, send_from_directory, abort
from flask_cors import CORS
import os

# Configure Flask to serve files from current directory
app = Flask(__name__, static_folder='.', template_folder='.')
CORS(app)

# Define allowed file extensions for security
ALLOWED_EXTENSIONS = {'.html', '.css', '.js', '.png', '.jpg', '.jpeg', '.gif', '.svg', '.pdf', '.md'}

def is_safe_path(filename):
    """Check if the requested file is safe to serve"""
    # Prevent directory traversal
    if '..' in filename or filename.startswith('/'):
        return False
    
    # Block sensitive files
    blocked_files = {'.env', '.git', '__pycache__', 'requirements.txt', '.gitignore'}
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
    
    if not os.path.isfile(filename):
        abort(404)
        
    return send_from_directory('.', filename)

if __name__ == '__main__':
    # Disable debug mode in production
    app.run(host='0.0.0.0', port=5000, debug=True)

