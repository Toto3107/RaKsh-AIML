import streamlit as st
import pandas as pd
import json
import os
import subprocess
from agent.searcher import find_new_sources
from validator.council import process_raw_to_structured
from database.db_handler import verified_table

st.set_page_config(page_title="Raksh Engine v1.0", layout="wide")

st.title("🛡️ Raksh-Engine: Autonomous Refinery")

# --- DATA REFRESH LOGIC ---
# This ensures the UI updates whenever the database changes
def get_current_data():
    return pd.DataFrame(verified_table.all())

# --- USER INPUT ---
query = st.text_input("What data should I extract?", placeholder="e.g. PH levels in Yamuna River 2024")

if st.button("🚀 Start Extraction Pipeline"):
    if not query:
        st.error("Please enter a query.")
    else:
        with st.status("Pipeline Running...", expanded=True) as status:
            # 1. SEARCH
            st.write("🔎 Searching for sources...")
            urls = find_new_sources(query)
            
            # 2. SCRAPE & VALIDATE
            for url in urls:
                st.write(f"🕸️ Scraping: {url}")
                # We save to a specific temp file for THIS run
                temp_file = "current_scrape.json"
                if os.path.exists(temp_file): os.remove(temp_file)
                
                subprocess.run(["scrapy", "crawl", "raksh_spider", "-a", f"start_url={url}", "-o", temp_file])
                
                # 3. VERIFICATION (The Missing Link)
                if os.path.exists(temp_file):
                    st.write(f"⚖️ Council verifying data from {url}...")
                    with open(temp_file, "r") as f:
                        raw_results = json.load(f)
                        for entry in raw_results:
                            process_raw_to_structured(entry) # This writes to database.json
                    os.remove(temp_file)
            
            status.update(label="✅ Extraction Complete!", state="complete")

# --- THE DOWNLOAD & DISPLAY SECTION (Bug Fix) ---
st.header("📊 Verified Database")
df = get_current_data()

if not df.empty:
    # Display the data
    st.dataframe(df, use_container_width=True)
    
    # DOWNLOAD OPTION
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Structured Dataset (CSV)",
        data=csv,
        file_name="verified_raksh_data.csv",
        mime="text/csv",
        key='download-csv'
    )
    
    if st.button("🗑️ Reset Database"):
        verified_table.truncate()
        st.rerun()
else:
    st.info("Database is empty. Run a search to populate it.")