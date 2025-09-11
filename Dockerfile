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

# Create nginx config for reverse proxy
RUN echo 'events { worker_connections 1024; }\n\
http {\n\
    upstream backend {\n\
        server localhost:8001;\n\
    }\n\
    server {\n\
        listen 3000;\n\
        location /api/ {\n\
            proxy_pass http://backend/;\n\
            proxy_http_version 1.1;\n\
            proxy_set_header Upgrade $http_upgrade;\n\
            proxy_set_header Connection "upgrade";\n\
            proxy_set_header Host $host;\n\
        }\n\
        location /ws/ {\n\
            proxy_pass http://backend/ws/;\n\
            proxy_http_version 1.1;\n\
            proxy_set_header Upgrade $http_upgrade;\n\
            proxy_set_header Connection "upgrade";\n\
            proxy_set_header Host $host;\n\
        }\n\
        location /docs {\n\
            proxy_pass http://backend/docs;\n\
        }\n\
        location / {\n\
            root /app/AMMA-UI/out;\n\
            try_files $uri $uri/ /index.html;\n\
        }\n\
    }\n\
}\n\
' > nginx.conf\n\
\n\
# Install nginx\n\
RUN apt-get update && apt-get install -y nginx && rm -rf /var/lib/apt/lists/*\n\
\n\
# Create startup script\n\
RUN echo '#!/bin/bash\n\
echo "🚀 Starting AMMA Backend on port 8001"\n\
/opt/venv/bin/python -m uvicorn app:app --host 0.0.0.0 --port 8001 &\n\
echo "🌐 Starting Nginx reverse proxy on port 3000"\n\
nginx -c /app/nginx.conf -g "daemon off;"\n\
' > start.sh && chmod +x start.sh

# Expose ports
EXPOSE 3000 8001

# Start command
CMD ["./start.sh"]