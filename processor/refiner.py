import os
import json
from google import genai
from pydantic import BaseModel, ValidationError
from typing import List, Dict, Any
from dotenv import load_dotenv
load_dotenv()
# Set up the Client
# 2026-spec: Gemini 3 Flash is the sweet spot for speed vs. reasoning
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def extract_structured_data(html_content: str, target_topic: str, schema_fields: List[str]):
    """
    Takes raw HTML and returns a structured JSON dataset.
    """
    
    # Construct a prompt that forces "Correctness"
    prompt = f"""
    You are a Senior Data Engineer. Your task is to extract high-fidelity data from the provided HTML.
    
    TOPIC: {target_topic}
    REQUIRED FIELDS: {', '.join(schema_fields)}
    
    INSTRUCTIONS:
    1. Extract ALL available records.
    2. Ensure data types are consistent (numbers as floats/ints, dates in ISO format).
    3. If a field is missing for a record, use null.
    4. Return ONLY a valid JSON array of objects.
    
    HTML BODY:
    {html_content[:30000]}  # Gemini 3 handles large contexts, but we trim to save tokens/cost
    """

    try:
        response = client.models.generate_content(
            model="gemini-3-flash",
            contents=prompt,
            config={
                "response_mime_type": "application/json"
            }
        )
        
        # Clean and parse the response
        dataset = json.loads(response.text)
        return dataset

    except Exception as e:
        return {"error": f"Refinement failed: {str(e)}"}