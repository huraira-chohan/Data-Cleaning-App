# Use official Python image
FROM python:3.10-slim

# Set workdir
WORKDIR /app

# Install system deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY . /app

# Expose Streamlit default port
EXPOSE 8501

# Streamlit config envs (can be overridden)
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_HEADLESS=true
ENV PYTHONUNBUFFERED=1

# Run
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
