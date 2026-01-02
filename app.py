import streamlit as st
import pandas as pd
from agent.searcher import find_new_sources
from database.db_handler import verified_table
from api.exporter import export_to_csv
import subprocess

# --- UI CONFIG ---
st.set_page_config(page_title="Raksh-Engine | Command Center", layout="wide")

st.title("🛡️ Raksh-Engine: Autonomous Environmental Intelligence")
st.markdown("---")

# --- SIDEBAR (Stats) ---
with st.sidebar:
    st.header("📊 Engine Status")
    total_records = len(verified_table.all())
    st.metric("Verified Records", total_records)
    
    if st.button("🗑️ Clear Database"):
        verified_table.truncate()
        st.rerun()

# --- MAIN INTERFACE ---
query = st.text_input("What dataset do you need today?", placeholder="e.g. Nitrate levels in Punjab groundwater 2025")

if st.button("🚀 Start Autonomous Extraction"):
    if not query:
        st.error("Please enter a query first!")
    else:
        with st.status("🔍 Agent is working...", expanded=True) as status:
            # Step 1: Search
            st.write("Searching the web for high-authority sources...")
            urls = find_new_sources(query)
            st.write(f"Found {len(urls)} sources.")
            
            # Step 2: Scrape & Process
            for url in urls:
                st.write(f"🕸️ Scraping: {url}")
                # We trigger the spider via subprocess
                subprocess.run(["scrapy", "crawl", "raksh_spider", "-a", f"start_url={url}"])
                
                # Step 3: Validation (Call your Council logic here)
                st.write(f"⚖️ Council is validating data from {url}...")
                # Note: Assuming your council processes the last entry in raw_data.json
            
            status.update(label="✅ Extraction Complete!", state="complete", expanded=False)

# --- DATA DISPLAY ---
st.subheader("📋 Extracted Dataset")
data = verified_table.all()
if data:
    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True)
    
    # Download Button
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Structured CSV",
        data=csv,
        file_name="raksh_environmental_data.csv",
        mime="text/csv",
    )
else:
    st.info("No data extracted yet. Start a run above!")