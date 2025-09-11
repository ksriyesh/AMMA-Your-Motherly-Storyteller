# Simple single-stage Dockerfile for AMMA
FROM node:18

# Install Python
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Create and activate virtual environment
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy Python backend source first
COPY src/ ./src/
COPY app.py ./
COPY main.py ./
COPY pyproject.toml ./

# Install Python dependencies
RUN pip install --no-cache-dir -e .

# Copy and install frontend dependencies
COPY AMMA-UI/package*.json ./AMMA-UI/
WORKDIR /app/AMMA-UI
RUN npm install

# Copy frontend source and build
COPY AMMA-UI/ ./

# Ensure lib directory is copied (sometimes Docker misses it)
COPY AMMA-UI/lib/ ./lib/

RUN npm run build

# Go back to app root
WORKDIR /app

# Install serve for static file serving
RUN npm install -g serve

# Create simple startup script that serves everything on one port
RUN echo '#!/bin/bash\n\
PORT=${PORT:-3000}\n\
echo "🚀 Starting AMMA Backend on port 8001"\n\
/opt/venv/bin/python -m uvicorn app:app --host 0.0.0.0 --port 8001 &\n\
echo "🎨 Starting AMMA Frontend on port $PORT"\n\
cd AMMA-UI && serve -s out -l $PORT --single\n\
' > start.sh && chmod +x start.sh

# Expose ports
EXPOSE 3000 8001

# Start command
CMD ["./start.sh"]