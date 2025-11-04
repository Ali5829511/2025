from flask import Flask, render_template, send_from_directory
from flask_cors import CORS
import os

# Configure Flask to serve files from current directory
app = Flask(__name__, static_folder='.', template_folder='.')
CORS(app)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('.', filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

