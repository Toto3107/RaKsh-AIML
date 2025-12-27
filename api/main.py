from fastapi import FastAPI, HTTPException
from database.mongo_client import collection
from typing import List
import uvicorn

app = FastAPI(title="Raksh-Engine API", description="Verified Environmental Data Provider")

@app.get("/")
def read_root():
    return {"status": "Raksh-Engine Online", "version": "1.0.0"}

@app.get("/data", response_model=List[dict])
def get_all_data(limit: int = 10):
    """Fetch the latest verified records from the database."""
    try:
        # Fetch data from MongoDB, excluding the internal _id for JSON compatibility
        cursor = collection.find({}, {"_id": 0}).sort("metadata.timestamp", -1).limit(limit)
        return list(cursor)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/data/{category}")
def get_data_by_category(category: str):
    """Filter verified data by category (e.g., groundwater, environment)."""
    cursor = collection.find({"metadata.category": category}, {"_id": 0})
    results = list(cursor)
    if not results:
        raise HTTPException(status_code=404, detail="No data found for this category")
    return results

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)