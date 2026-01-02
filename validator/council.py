from langchain_google_genai import ChatGoogleGenerativeAI
from .schema import VerifiedDataset
from database.db_handler import save_verified_data

llm = ChatGoogleGenerativeAI(model="models/gemini-1.5-flash") # Use 1.5-flash for high-speed extraction
structured_llm = llm.with_structured_output(VerifiedDataset)

def process_raw_to_structured(raw_entry):
    """
    Takes raw scraped text and turns it into a perfectly structured dataset row.
    """
    prompt = f"""
    You are a Data Architect. Extract specific environmental data points from the text below.
    If no numeric data is found, set is_relevant to False.
    Raw Text: {raw_entry['text']}
    URL: {raw_entry['url']}
    """
    
    try:
        extraction = structured_llm.invoke(prompt)
        
        if extraction.is_relevant and extraction.confidence_score > 0.8:
            for entry in extraction.extracted_data:
                final_row = {
                    "source_url": raw_entry['url'],
                    **entry.dict()
                }
                save_verified_data(final_row) # Saves to TinyDB or Mongo
                print(f"✅ Extracted: {entry.parameter} at {entry.location}")
    except Exception as e:
        print(f"❌ Extraction Error: {e}")