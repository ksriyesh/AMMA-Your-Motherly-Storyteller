# Backend-only Dockerfile for AMMA
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    && rm -rf /var/lib/apt/lists/*

# Copy Python backend source
COPY src/ ./src/
COPY app.py ./
COPY main.py ./
COPY pyproject.toml ./

# Install Python dependencies
RUN pip install --no-cache-dir -e .

# Expose backend port (Railway will set PORT env var)
EXPOSE 8001

# Start backend on Railway's PORT (8080) or fallback to 8001
CMD ["sh", "-c", "python -m uvicorn app:app --host 0.0.0.0 --port ${PORT:-8001}"]
