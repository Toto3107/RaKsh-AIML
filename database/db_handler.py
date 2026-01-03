from tinydb import TinyDB, Query
import os

# Ensure the database directory exists
os.makedirs('database', exist_ok=True)

db = TinyDB('database/database.json')
verified_table = db.table('verified_data')

def save_verified_data(data):
    """Simple wrapper to insert into table."""
    verified_table.insert(data)