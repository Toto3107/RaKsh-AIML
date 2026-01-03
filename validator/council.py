import hashlib
from langchain_google_genai import ChatGoogleGenerativeAI
from database.db_handler import verified_table, Query
from .schema import VerifiedDataset
import os 
from dotenv import load_dotenv
load_dotenv()
# 1. FIX: Updated model string for 2026 stability
llm = ChatGoogleGenerativeAI(
    model="models/gemini-1.5-flash", 
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0,
    # Adding this helps if the library is defaulting to an old API version
    version="v1" 
)
structured_llm = llm.with_structured_output(VerifiedDataset)

def generate_unique_id(record):
    """Creates a unique hash based on location, parameter, and value."""
    unique_string = f"{record['location']}-{record['parameter']}-{record['value']}".lower()
    return hashlib.md5(unique_string.encode()).hexdigest()

def process_raw_to_structured(raw_entry):
    prompt = f"Extract environmental data points from: {raw_entry['text']}"
    
    try:
        extraction = structured_llm.invoke(prompt)
        
        if extraction.is_relevant and extraction.confidence_score > 0.7:
            for item in extraction.extracted_data:
                record = {
                    "parameter": item.parameter,
                    "value": item.value,
                    "unit": item.unit,
                    "location": item.location,
                    "date": item.timestamp,
                    "source": raw_entry.get('url')
                }
                
                # 2. DEDUPLICATION: Check if this data already exists
                record_id = generate_unique_id(record)
                Entry = Query()
                if not verified_table.search(Entry.uid == record_id):
                    record['uid'] = record_id # Store the unique ID
                    verified_table.insert(record)
                    print(f"✅ Saved Unique Record: {item.location}")
                else:
                    print(f"⏭️ Skipping Duplicate: {item.location}")
            return True
        return False
    except Exception as e:
        print(f"🔥 [COUNCIL ERROR]: {e}")
        return False