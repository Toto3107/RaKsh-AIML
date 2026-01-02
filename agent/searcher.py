import os
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()

# Get your key from https://tavily.com/
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def find_new_sources(user_query: str):
    """
    Translates a human question into a list of high-quality URLs.
    """
    print(f"🔎 Agent is searching the web for: {user_query}")
    
    # We target specifically government, educational, and environmental sites
    refined_query = f"{user_query} reports filetype:html site:.gov OR site:.org"
    
    response = tavily.search(query=refined_query, search_depth="advanced", max_results=3)
    
    # Return a list of just the URLs
    return [result['url'] for result in response['results']]