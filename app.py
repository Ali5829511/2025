from flask import Flask, render_template, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__, static_folder='src/static', template_folder='src/static')
CORS(app)

@app.route('/')
def index():
    return send_from_directory('src/static', 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('src/static', filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

