# Project Title: Raksh-Engine (Dynamic AIML Centralized Data Provider)
**Status:** In-Development (Active Sprint: 0)  
**Author:** Mayank Gehlot
**Target GSoC Orgs:** NumFOCUS, OWASP, PSF, C2SI  

---

## 1. Abstract
The **Raksh-Engine** is an intelligent, agent-driven data ingestion pipeline designed to solve the problem of "Static Dataset Decay" in AI/ML projects. Unlike traditional scrapers that fetch data from hardcoded lists, this engine acts as a **Dynamic Data-on-Demand** service. It takes natural language input from a user (e.g., "I need real-time groundwater salinity levels in Punjab"), discovers relevant sources, orchestrates distributed scrapers, and validates the output through a **Multi-Agent LLM Council** before feeding it into the "Raksh" ML model or a chatbot interface.

## 2. Problem Statement
- **Dynamic Data Gap:** Real-time ML models (like groundwater predictors) fail when relying on outdated Kaggle datasets.
- **Data Poisoning:** Automated scrapers often ingest "noise" or false data, which degrades ML model accuracy.
- **High Entry Barrier:** Researchers often spend 80% of their time on data collection rather than model optimization.

## 3. Proposed Solution
A centralized engine that bridges the gap between raw web data and ML-ready features.
- **On-Demand Discovery:** Uses an LLM to identify the best URLs/APIs for a user's request.
- **Agentic Validation:** A "Council" of 3 LLM agents (The Extractor, The Skeptic, and The Chairman) reaches consensus on data validity.
- **Automated ML Feed:** Verified data is automatically transformed into a schema-ready format for the Raksh ML pipeline.

## 4. Technical Architecture (HLD)



### A. Ingestion Tier (Scrapy & Docker)
- Distributed, containerized Scrapy spiders.
- Triggered by CLI arguments passed from the "Chatbot" or "Orchestrator."

### B. Validation Tier (The LLM Council - LangChain/LangGraph)
- **Agent 1 (Extractor):** Pulls raw entities from the scraped HTML.
- **Agent 2 (The Skeptic):** Cross-references values against physical limits (e.g., pH levels cannot be 40).
- **Agent 3 (The Chairman):** Merges the findings and assigns a "Confidence Score."

### C. Observability Tier (Prometheus & ELK)
- **Monitoring:** Scraping success rates and LLM token costs via Prometheus/Grafana.
- **Logging:** Centralized logs via Filebeat/ELK to track data lineage and audit the "Council's" decisions.

## 5. Technology Stack
- **Languages:** Python (Core), Bash (Automation).
- **Orchestration:** LangGraph, Docker Compose, Kubernetes.
- **Primary Scraper:** Scrapy (for high-concurrency background ingestion).
- **Dynamic Handler:** Playwright (integrated via `scrapy-playwright` for JS-rendered government portals).
- **Extraction Logic:** LLM-based semantic extraction (ScrapeGraphAI) to handle varying site structures without manual CSS maintenance.
- **Data Storage:** MongoDB (Unstructured), ChromaDB (Vector Search).
- **DevOps:** GitHub Actions (CI/CD), Prometheus, Grafana, ELK Stack.

## 6. GSoC 2026 Milestones (Draft)
- **Weeks 1-3:** Core Ingestion Engine (Multi-topic Scrapy Spiders + Dockerization).
- **Weeks 4-6:** LLM Council Integration (LangChain Consensus Logic).
- **Weeks 7-9:** API Development & Chatbot Interface (FastAPI + React).
- **Weeks 10-12:** Observability & Scaling (K8s deployment + Grafana Dashboards).

7. Data Ingestion & ML Loop:

Validation Logic (Day 4): Implemented a Multi-Agent "Council" using LangChain and Pydantic. This ensures semantic integrity and prevents "Data Poisoning" of the Raksh ML models.