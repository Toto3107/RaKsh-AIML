import json
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from .schema import VerifiedData
from database.db_handler import save_verified_data
# 1. Initialize Gemini
# We use 'gemini-1.5-flash' because it's fast and free
llm = ChatGoogleGenerativeAI(
    model="models/gemini-2.5-flash",
    temperature=0.3,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

# 2. Bind the Schema (Structured Output)
structured_llm = llm.with_structured_output(VerifiedData)

def run_council(raw_entry):
    # Prompting the Council
    system_message = (
        "You are the Chairman of the Data Council. "
        "Evaluate the following scraped data for environmental monitoring relevance. "
        "If it's just quotes or random text, mark is_valid=False."
    )
    user_content = f"Raw Scraped Entry: {raw_entry}"
    
    # Combine and Invoke
    response = structured_llm.invoke([
        ("system", system_message),
        ("user", user_content)
    ])
    return response


with open("raw_data.json") as f:
    data = json.load(f)
for entry in data:
    decision = run_council(entry)
    
    if decision.is_valid and decision.confidence_score > 0.7:
        # Prepare the final document for the database
        final_doc = {
            "metadata": entry,
            "validation": decision.dict(), # Convert Pydantic to Dict
            "status": "ready_for_ml"
        }
        db_id = save_verified_data(final_doc)
        print(f"✅ Data Persistence Success: ID {db_id}")
    else:
        print("❌ Data Rejected by Council.")
        
# 3. Main Execution
if __name__ == "__main__":
    if not os.path.exists("raw_data.json"):
        print("Error: raw_data.json not found! Run your Scrapy spider first.")
    else:
        with open("raw_data.json", "r") as f:
            data = json.load(f)

        print(f"🚀 Council is reviewing {len(data[:3])} entries...")
        
        for i, entry in enumerate(data[:3]):
            decision = run_council(entry)
            print(f"\n--- Entry {i+1} Result ---")
            print(f"Valid: {decision.is_valid}")
            print(f"Confidence: {decision.confidence_score}")
            print(f"Notes: {decision.skeptic_notes}")