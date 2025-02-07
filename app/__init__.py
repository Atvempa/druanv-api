from flask import Flask
from pymongo import MongoClient
import os
from dotenv import load_dotenv
import certifi
import ssl

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize MongoDB with SSL configuration
MONGO_URI = os.getenv('MONGO_URI')
client = MongoClient(
    MONGO_URI,
    tlsCAFile=certifi.where(),
    tls=True,
    tlsAllowInvalidCertificates=True
)
db = client.profiles_db
profiles = db.profiles

from app import routes 