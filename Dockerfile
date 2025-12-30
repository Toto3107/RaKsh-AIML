# Use a lightweight Python image
FROM python:3.12-slim

# Set environment variables to prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Install system dependencies (needed for Scrapy/Playwright)
RUN apt-get update && apt-get install -y \
    gcc \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your project code
COPY . .

# Expose the port your FastAPI runs on
EXPOSE 8000

# Command to run the API by default
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]