'''import streamlit as st
import pandas as pd
import json
import os
import subprocess

from agent.searcher import find_new_sources
from validator.council import process_extracted_text
from database.db_handler import verified_table

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="Raksh Engine v1.0",
    page_icon="🛡️",
    layout="wide"
)

# ------------------ HEADER ------------------
st.markdown(
    """
    <div style="padding:15px 0;">
        <h1>🛡️ Raksh Engine</h1>
        <p style="font-size:16px; color: #9aa0a6;">
        Autonomous Data Extraction • Validation • Structuring Engine
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# ------------------ SIDEBAR ------------------
with st.sidebar:
    st.header("⚙️ Engine Controls")
    st.markdown(
        """
        **Raksh Pipeline**
        1. 🔍 Source Discovery  
        2. 🕸️ Web Scraping  
        3. ⚖️ AI Council Validation  
        4. 📊 Structured Storage  
        """
    )
    st.divider()
    st.caption("Version: v1.0 | Mode: Local Execution")

# ------------------ DATA REFRESH ------------------
def get_current_data():
    return pd.DataFrame(verified_table.all())

# ------------------ MAIN INPUT ------------------
st.subheader("🔎 Research Query")

query = st.text_input(
    label="What data should Raksh extract?",
    placeholder="e.g. PH levels in Yamuna River 2024",
)

run_pipeline = st.button("🚀 Run Autonomous Extraction", use_container_width=True)

# ------------------ PIPELINE EXECUTION ------------------
if run_pipeline:
    if not query:
        st.error("⚠️ Please enter a research query to proceed.")
    else:
        with st.status("Raksh Engine is running...", expanded=True) as status:

            # STEP 1: SEARCH
            st.markdown("### 🔍 Discovering Sources")
            urls = find_new_sources(query)
            st.success(f"Found {len(urls)} potential sources")

            # STEP 2: SCRAPE + VALIDATE
            st.markdown("### 🕸️ Scraping & ⚖️ Validating")

            for idx, url in enumerate(urls, start=1):
                st.write(f"**{idx}. Processing:** {url}")

                temp_file = "current_scrape.json"
                if os.path.exists(temp_file):
                    os.remove(temp_file)

                subprocess.run(
                    ["scrapy", "crawl", "raksh_spider", "-a", f"start_url={url}", "-o", temp_file],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )

                if os.path.exists(temp_file):
                    with open(temp_file, "r") as f:
                        raw_results = json.load(f)

                    for entry in raw_results:
                        process_extracted_text(entry)

                    os.remove(temp_file)

            status.update(
                label="✅ Raksh Pipeline Completed Successfully",
                state="complete",
                expanded=False
            )

# ------------------ VERIFIED DATA ------------------
st.divider()
st.subheader("📊 Verified Knowledge Base")

df = get_current_data()

if not df.empty:
    st.dataframe(df, use_container_width=True, height=420)

    col1, col2 = st.columns([3, 1])

    with col1:
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download Structured Dataset (CSV)",
            data=csv,
            file_name="verified_raksh_data.csv",
            mime="text/csv",
            use_container_width=True
        )

    with col2:
        if st.button("🗑️ Reset Database", type="secondary", use_container_width=True):
            verified_table.truncate()
            st.warning("Database cleared.")
            st.rerun()

else:
    st.info("📭 No verified data yet. Run the pipeline to populate the database.")
'''
import streamlit as st
import json
import subprocess
from processor.refiner import extract_structured_data

st.set_page_config(page_title="Universal DaaS", layout="wide")
st.title("🚀 Universal Dataset Provider")

url = st.text_input("Target URL", "https://news.ycombinator.com")
topic = st.text_input("Target Topic", "Trending AI News")
fields = ["title", "link", "score"]

if st.button("Generate Dataset"):
    with st.spinner("Bypassing anti-bots and extracting..."):
        # Run Scrapy via Subprocess (Stateless & Fast)
        # Note: We save to 'temp_output.json'
        subprocess.run([
            "scrapy", "crawl", "universal_spider", 
            "-a", f"url={url}", 
            "-o", "temp_output.json"
        ])
        
        with open("temp_output.json") as f:
            raw_data = json.load(f)[0]
            
        # Refine with AI
        final_json = extract_structured_data(raw_data['html'], topic, fields)
        st.write("### ✅ Extraction Complete")
        st.json(final_json)