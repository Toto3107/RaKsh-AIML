import streamlit as st
import pandas as pd
import json
from agent.searcher import find_new_sources
from validator.council import process_raw_to_structured  # Import your Council logic
from database.db_handler import verified_table
import subprocess
import os

# --- APP LAYOUT ---
st.title("🛡️ Raksh-Engine: Autonomous Data Refinery")

query = st.text_input("Describe the dataset you need:", placeholder="e.g. Ground water levels in Maharashtra 2024")

if st.button("🚀 Generate Verified Dataset"):
    if not query:
        st.warning("Please enter a request.")
    else:
        # 1. SEARCH PHASE
        with st.spinner("🕵️ Agent finding sources..."):
            urls = find_new_sources(query)
            st.success(f"Found {len(urls)} relevant sources.")

        # 2. INGEST & VALIDATE PHASE
        progress_bar = st.progress(0)
        for idx, url in enumerate(urls):
            st.write(f"⏳ Processing: {url}")
            
            # Run Spider
            # Note: We use a temp file for raw data to avoid mixing old/new runs
            subprocess.run(["scrapy", "crawl", "raksh_spider", "-a", f"start_url={url}", "-o", "temp_raw.json"])
            
            # Run Council on the raw data just collected
            if os.path.exists("temp_raw.json"):
                with open("temp_raw.json", "r") as f:
                    raw_data = json.load(f)
                    for entry in raw_data:
                        # This is the "Refinery" step
                        process_raw_to_structured(entry)
                
                os.remove("temp_raw.json") # Clean up for the next URL
            
            progress_bar.progress((idx + 1) / len(urls))

        st.balloons()
        st.success("Refinery complete! Your verified dataset is ready.")

# --- THE VERIFIED FILE SECTION ---
st.markdown("---")
st.subheader("📥 Download Verified Dataset")

# Fetch data from TinyDB
verified_data = verified_table.all()

if verified_data:
    df = pd.DataFrame(verified_data)
    
    # Show the table to the user
    st.dataframe(df, use_container_width=True)
    
    # CREATE THE DOWNLOAD BUTTON
    csv_data = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="💾 Download Verified CSV",
        data=csv_data,
        file_name=f"raksh_{query.replace(' ', '_')}.csv",
        mime="text/csv"
    )
else:
    st.info("The database is currently empty. Run the extraction above to generate data.")