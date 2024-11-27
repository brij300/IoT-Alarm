from pymongo import MongoClient

# MongoDB connection details
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "EdgeAlarms"

def get_db():
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    return db
