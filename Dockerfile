# ReproPack Backend - Fly.io Dockerfile
FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# System deps (optional: build tools if needed for future packages)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates build-essential && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy application source
COPY . .

# Expose internal port (Fly will map 443/80 externally)
EXPOSE 8080

# Default envs (override in fly secrets if needed)
ENV REPROPACK_PACKAGES_DIR=/data/packages

# Create runtime directory (will be volume mounted)
RUN mkdir -p /data/packages

# Start server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
