# app.py
from flask import Flask, request, jsonify
from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv

# Load .env if present (helpful for local dev)
load_dotenv()

app = Flask(__name__)

# Environment variables
MONGODB_URI = os.environ.get("MONGODB_URI")
MONGO_USER = os.environ.get("MONGO_USER")
MONGO_PASSWORD = os.environ.get("MONGO_PASSWORD")
MONGO_AUTH_DB = os.environ.get("MONGO_AUTH_DB", "admin")  # default admin

# Build connection string:
# If MONGODB_URI provided directly, prefer it; otherwise build from parts
if not MONGODB_URI:
    if MONGO_USER and MONGO_PASSWORD:
        # connect using credentials
        MONGODB_URI = f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@mongodb:27017/?authSource={MONGO_AUTH_DB}"
    else:
        MONGODB_URI = "mongodb://mongodb:27017/"

# Create Mongo client
client = MongoClient(MONGODB_URI)
db = client.flask_db
collection = db.data

@app.route('/')
def index():
    return f"Welcome to the Flask app! The current time is: {datetime.now()}"

@app.route('/data', methods=['GET', 'POST'])
def data():
    if request.method == 'POST':
        payload = request.get_json()
        if not payload:
            return jsonify({"error": "Invalid JSON or empty body"}), 400
        # insert document
        collection.insert_one(payload)
        return jsonify({"status": "Data inserted"}), 201
    else:  # GET
        docs = list(collection.find({}, {"_id": 0}))
        return jsonify(docs), 200

if __name__ == "__main__":
    # For local development only. In production in k8s we'll use gunicorn (or flask run via docker)
    app.run(host='0.0.0.0', port=5000)
