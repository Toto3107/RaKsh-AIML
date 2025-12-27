import os
from pymongo import MongoClient
import certifi

# Use the same environment variable strategy from Day 4
MONGO_URI = os.getenv("MONGO_CONNECTION_STRING")

client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())
db = client['raksh_engine']
collection = db['verified_datasets']

def save_to_db(data_dict):
    try:
        result = collection.insert_one(data_dict)
        return result.inserted_id
    except Exception as e:
        print(f"Database Error: {e}")
        return None