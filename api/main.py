from fastapi import FastAPI, HTTPException
from database.db_handler import verified_table # Import from our new handler
from typing import List

app = FastAPI(title="Raksh-Engine API")

@app.get("/")
def home():
    return {"message": "Raksh Local Data Provider is Live"}

@app.get("/data")
def get_verified_data():
    """Fetch all verified records from TinyDB."""
    return verified_table.all()

@app.get("/data/{category}")
def get_by_category(category: str):
    """Filter records by category."""
    # TinyDB search logic
    from tinydb import Query
    Data = Query()
    results = verified_table.search(Data.metadata.category == category)
    
    if not results:
        raise HTTPException(status_code=404, detail="Category not found")
    return results