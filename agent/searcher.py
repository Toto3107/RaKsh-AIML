import os
from tavily import TavilyClient

def find_new_sources(query):
    # Initialize Tavily (Get key from tavily.com)
    tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
    
    # Search for the query + "data" to get specific results
    search_result = tavily.search(query=f"{query} data 2024", search_depth="advanced")
    
    # Return just the URLs
    return [res['url'] for res in search_result['results']]