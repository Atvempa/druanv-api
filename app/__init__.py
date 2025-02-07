from flask import Flask
from flask_pymongo import PyMongo
from flask_cors import CORS
from app.config import Config

app = Flask(__name__)
CORS(app)  # Add CORS support

# Skip auth for API routes
@app.before_request
def skip_auth():
    if request.path.startswith('/api/'):
        return None

app.config.from_object(Config)

# Initialize MongoDB
mongo = PyMongo(app)

from app import routes
