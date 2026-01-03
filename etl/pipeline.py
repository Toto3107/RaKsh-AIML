import subprocess
import json
import os
import time
from validator.council import process_raw_to_structured
from agent.searcher import find_new_sources
class RakshETL:
    def __init__(self, query):
        self.query = query
        self.raw_file = "raw_ingestion.json"

    def run(self):
        # 1. CLEANUP OLD DATA
        if os.path.exists(self.raw_file):
            os.remove(self.raw_file)

        # 2. EXTRACT
        def extract(self):
            urls = find_new_sources(self.query)
            
            if not urls:
                return False

            # Ensure we start with a fresh raw file for this query
            if os.path.exists(self.raw_file):
                os.remove(self.raw_file)

            for url in urls:
                print(f"🕸️ [EXTRACT] Scraping: {url}")
                # The '-a' flag passes the argument to the __init__ of the spider
                subprocess.run([
                    "scrapy", "crawl", "raksh_spider", 
                    "-a", f"start_url={url}", 
                    "-o", self.raw_file,
                    "--loglevel", "INFO" # Keep logs clean so we see the status
                ])
            return os.path.exists(self.raw_file)
        # 3. CHECK IF EXTRACTION WORKED
        if not os.path.exists(self.raw_file) or os.getsize(self.raw_file) == 0:
            print("⚠️ Extraction yielded no data.")
            return 0

        # 4. TRANSFORM & LOAD
        with open(self.raw_file, "r") as f:
            raw_data = json.load(f)
            new_records = 0
            for entry in raw_data:
                if process_raw_to_structured(entry):
                    new_records += 1
        
        return new_records