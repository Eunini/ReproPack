# ReproPack Backend - Dockerfile for Render
FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    # Add Rust's cargo bin to the PATH
    PATH="/root/.cargo/bin:${PATH}"

WORKDIR /app

# Install system dependencies: build-essential for C extensions, curl for rustup
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates build-essential && rm -rf /var/lib/apt/lists/*

# Install Rust toolchain
RUN curl https://sh.rustup.rs -sSf | sh -s -- -y

# Install Python dependencies
COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy application source
COPY . .

# Expose internal port
EXPOSE 8080

# Create runtime directory
RUN mkdir -p /data/packages

# Start server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]