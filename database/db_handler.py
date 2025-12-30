from tinydb import TinyDB, Query
import os
from datetime import datetime

# Creates 'database.json' in your project folder
db = TinyDB('database.json')
verified_table = db.table('verified_datasets')

def save_verified_data(data_dict):
    """Inserts a verified document into the local JSON database."""
    try:
        data_dict['stored_at'] = datetime.now().isoformat()
        inserted_id = verified_table.insert(data_dict)
        print(f"✨ Data saved locally! Document ID: {inserted_id}")
        return inserted_id
    except Exception as e:
        print(f"❌ Storage Error: {e}")
        return None

def get_all_verified():
    """Returns all records from the local DB."""
    return verified_table.all()