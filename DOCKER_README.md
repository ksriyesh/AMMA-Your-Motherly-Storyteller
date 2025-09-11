# 🐳 AMMA Docker Setup

Run AMMA - Bedtime Story Agent with Docker for easy deployment and development.

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose installed
- OpenAI API key

### 1. Set up environment variables
Create a `.env` file in the project root:
```bash
OPENAI_API_KEY=your_openai_api_key_here
```

### 2. Build and run with Docker Compose
```bash
# Build and start both frontend and backend
docker-compose up --build

# Run in background (detached mode)
docker-compose up -d --build
```

### 3. Access the application
- **Frontend (React UI)**: http://localhost:3000
- **Backend API**: http://localhost:8001
- **API Documentation**: http://localhost:8001/docs

## 🛠️ Development Commands

```bash
# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild after code changes
docker-compose up --build

# Run with production nginx proxy
docker-compose --profile production up
```

## 📦 What's Included

The Docker setup includes:
- ✅ **Python 3.11** with all backend dependencies
- ✅ **Node.js 18** for frontend
- ✅ **FastAPI backend** on port 8001
- ✅ **Next.js frontend** on port 3000
- ✅ **WebSocket support** for real-time chat
- ✅ **Health checks** for monitoring
- ✅ **Graceful shutdown** handling
- ✅ **Optional nginx proxy** for production

## 🔧 Manual Docker Build

If you prefer to use Docker without compose:

```bash
# Build the image
docker build -t amma-bedtime-stories .

# Run the container
docker run -d \
  -p 3000:3000 \
  -p 8001:8001 \
  -e OPENAI_API_KEY=your_key_here \
  --name amma \
  amma-bedtime-stories
```

## 📝 Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | OpenAI API key for GPT models | Yes |
| `NODE_ENV` | Node environment (production/development) | No |

## 🏗️ Architecture

The Docker container runs:
1. **FastAPI backend** serving the AMMA agent API
2. **Next.js frontend** serving the React chat interface
3. **WebSocket connection** for real-time streaming
4. **Health monitoring** for service status

## 🚨 Troubleshooting

**Container won't start:**
- Check if `.env` file exists with `OPENAI_API_KEY`
- Ensure ports 3000 and 8001 are not in use

**Frontend not loading:**
- Wait 60 seconds for full startup
- Check logs: `docker-compose logs amma`

**Backend API errors:**
- Verify OpenAI API key is valid
- Check backend logs for detailed error messages

## 🌟 Production Deployment

For production, use the nginx profile:
```bash
docker-compose --profile production up -d
```

This adds a reverse proxy on port 80 for better performance and routing.
