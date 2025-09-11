# Multi-stage Docker build for AMMA - Bedtime Story Agent
# Stage 1: Build Next.js frontend
FROM node:18-alpine AS frontend-builder

WORKDIR /app/frontend

# Copy frontend package files
COPY AMMA-UI/package*.json ./
COPY AMMA-UI/yarn.lock* ./

# Install frontend dependencies
RUN npm install

# Copy frontend source code
COPY AMMA-UI/ ./

# Build the frontend
# Cache bust: 2025-09-11-v2
RUN npm run build

# Stage 2: Setup Python backend and serve everything
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js for serving frontend
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs

# Set working directory
WORKDIR /app

# Copy Python requirements and install dependencies
COPY pyproject.toml ./
RUN pip install --no-cache-dir -e .

# Copy Python backend source
COPY src/ ./src/
COPY app.py ./
COPY main.py ./
COPY start_app.py ./

# Copy built frontend from previous stage
COPY --from=frontend-builder /app/frontend/.next ./AMMA-UI/.next
COPY --from=frontend-builder /app/frontend/public ./AMMA-UI/public
COPY --from=frontend-builder /app/frontend/package*.json ./AMMA-UI/
COPY --from=frontend-builder /app/frontend/node_modules ./AMMA-UI/node_modules
COPY AMMA-UI/next.config.mjs ./AMMA-UI/
COPY AMMA-UI/tsconfig.json ./AMMA-UI/
COPY AMMA-UI/postcss.config.mjs ./AMMA-UI/
COPY AMMA-UI/tailwind.config.js ./AMMA-UI/

# Create startup script
RUN echo '#!/bin/bash\n\
set -e\n\
\n\
echo "🚀 Starting AMMA - Bedtime Story Agent"\n\
echo "✅ Backend: http://localhost:8001"\n\
echo "✅ Frontend: http://localhost:3000"\n\
echo ""\n\
\n\
# Start backend in background\n\
echo "🔧 Starting FastAPI backend..."\n\
python -m uvicorn app:app --host 0.0.0.0 --port 8001 &\n\
BACKEND_PID=$!\n\
\n\
# Wait a moment for backend to start\n\
sleep 5\n\
\n\
# Start frontend\n\
echo "🎨 Starting Next.js frontend..."\n\
cd AMMA-UI\n\
npm start &\n\
FRONTEND_PID=$!\n\
\n\
# Function to cleanup processes\n\
cleanup() {\n\
    echo "🛑 Shutting down services..."\n\
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null || true\n\
    exit 0\n\
}\n\
\n\
# Trap signals for graceful shutdown\n\
trap cleanup SIGTERM SIGINT\n\
\n\
echo "✅ AMMA is running!"\n\
echo "📖 Visit http://localhost:3000 to start creating bedtime stories"\n\
echo "🔧 API docs available at http://localhost:8001/docs"\n\
echo ""\n\
echo "Press Ctrl+C to stop"\n\
\n\
# Wait for processes\n\
wait\n\
' > /app/start.sh && chmod +x /app/start.sh

# Expose ports
EXPOSE 3000 8001

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8001/docs || exit 1

# Set environment variables
ENV NODE_ENV=production
ENV PYTHONPATH=/app

# Default command
CMD ["/app/start.sh"]
