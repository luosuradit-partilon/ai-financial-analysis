FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency files first for better caching
COPY requirements.txt ./

# Install Python dependencies with optimizations
RUN pip install --upgrade pip && \
    pip install --no-cache-dir --timeout=1000 -r requirements.txt

# Copy application files
COPY *.py ./

# Create directory for generated analysis files
RUN mkdir -p /app/output

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Run the MCP server
CMD ["python", "app/server.py"]