import subprocess
from agent.searcher import find_new_sources

def start_autonomous_run(topic):
    # STEP 1: Find URLs
    target_urls = find_new_sources(topic)
    
    if not target_urls:
        print("❌ No relevant sources found.")
        return

    # STEP 2: Scrape them one by one
    for url in target_urls:
        print(f"🕸️ Deploying Spider to: {url}")
        
        # We pass the URL directly into the Scrapy spider
        # Note: 'raksh_spider' must be updated to accept the 'start_url' argument
        subprocess.run([
            "scrapy", "crawl", "raksh_spider",
            "-a", f"start_url={url}",
            "-o", "raw_data.json"
        ])

    print("\n✅ Extraction Finished. Data stored in raw_data.json")

if __name__ == "__main__":
    query = input("What environmental data should I find? ")
    start_autonomous_run(query)