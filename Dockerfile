# Use a Python 3.12 slim image for 2026 performance
FROM python:3.12-slim

# Install system dependencies for curl_cffi and Scrapy
RUN apt-get update && apt-get install -y \
    build-essential \
    libnss3 \
    libnss3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Streamlit default port
EXPOSE 8501

CMD ["streamlit", "run", "app.py"]