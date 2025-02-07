from flask import Flask
from flask_pymongo import PyMongo
from flask_cors import CORS
from app.config import Config

app = Flask(__name__)
CORS(app)  # Add CORS support
app.config.from_object(Config)

# Initialize MongoDB
mongo = PyMongo(app)

from app import routes 
