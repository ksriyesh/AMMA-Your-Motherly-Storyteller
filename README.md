# 🌙 AMMA 2.0 - Bedtime Story Agent

**AMMA** (Adaptive Multi-agent Motherly Assistant) is an intelligent conversational AI system that creates personalized bedtime stories for children. Built with a hybrid architecture combining **ReAct (Reasoning and Acting)** and **Reflection** patterns, AMMA provides natural conversation while generating high-quality, safe bedtime stories.

![AMMA Architecture](https://github.com/user-attachments/assets/21c95737-c7f0-48ae-90c5-bf2cf0044db0)

*Multi-agent architecture combining ReAct for interaction and Reflection for story creation*

## 🏗️ Architecture Overview

AMMA combines two powerful AI patterns to deliver both natural interaction and high-quality story generation:

### **ReAct Pattern (Interaction Layer)**
- **Purpose**: Natural conversation and preference collection
- **Agent**: AMMA conversational agent
- **Tools**: `update_story_preferences`, `request_new_story`
- **Flow**: Reason about user input → Act with appropriate tools → Respond naturally

### **Reflection Pattern (Story Creation Layer)**
- **Purpose**: High-quality story generation through iterative improvement
- **Agents**: Story Creator → Story Evaluator → Story Presenter
- **Flow**: Create story → Evaluate quality → Approve/Revise → Present final story

## 🎯 Agent Flow

```
User Input → AMMA (Conversational) → Tools → Story Creator → Story Evaluator
                ↓                                              ↓
             End Chat                                    Story Presenter
                                                              ↓
                                                         Final Story
                                                              ↓
                                                    Revision Handler (if needed)
```

### **Core Agents**
1. **🗣️ AMMA (Conversational)**: Motherly interaction, preference collection, conversation management
2. **✍️ Story Creator**: Generates bedtime stories (5-10 min reading time, age 5-10)
3. **🔍 Story Evaluator**: Reviews for safety, tone, age-appropriateness, and bedtime suitability
4. **📖 Story Presenter**: Delivers clean, final story to user
5. **🔄 Revision Handler**: Manages story improvement iterations

### **State Management**
- Child information (name, preferences)
- Story content and revisions
- Conversation history
- Evaluation results and feedback
- Revision tracking (max 3 iterations)

## 📦 Installation & Setup

### **Prerequisites**
- Python 3.11+ (for backend)
- Node.js 18+ (for frontend)  
- OpenAI API key
- Docker (optional, for containerized backend)

### **🚀 Quick Setup**

**Option 1: One-Command Install (Recommended)**
```bash
# Install everything automatically
python install.py
```

**Option 2: Manual Setup**
```bash
# 1. Clone repository
git clone https://github.com/ksriyesh/AMMA-Your-Motherly-Storyteller.git
cd AMMA-Your-Motherly-Storyteller

# 2. Backend Setup
pip install -e .

# 3. Frontend Setup
cd AMMA-UI
npm install
cd ..

# 4. Environment Variables
echo "OPENAI_API_KEY=your_openai_key_here" > .env
```

### **📋 Package Installation Details**

**Backend Dependencies (Python):**
```bash
# Core packages installed via pyproject.toml:
pip install -e .

# Key dependencies:
# - langchain-core, langchain-openai (LLM integration)
# - langgraph (multi-agent orchestration) 
# - fastapi, uvicorn (web server)
# - websockets (real-time communication)
# - pydantic (data validation)
# - python-dotenv (environment management)
```

**Frontend Dependencies (Node.js):**
```bash
cd AMMA-UI
npm install

# Key dependencies:
# - next.js (React framework)
# - tailwindcss (styling)
# - shadcn/ui (UI components)
# - lucide-react (icons)
```

## 🖥️ Local Development

### **Option 1: Full Stack Development**
```bash
# Start both backend and frontend
python start_app.py

# Access:
# Frontend: http://localhost:3000
# Backend: http://localhost:8001
# API Docs: http://localhost:8001/docs
```

### **Option 2: Separate Development**
```bash
# Terminal 1: Backend only
python -m uvicorn app:app --reload --port 8001

# Terminal 2: Frontend only
cd AMMA-UI
npm run dev

# Access:
# Frontend: http://localhost:3000
# Backend: http://localhost:8001
```

### **Option 3: CLI Testing**
```bash
# Simple command-line interface
python main.py

# Pure conversational interface - chat directly with AMMA
```

## 🐳 Docker Deployment

### **Backend Only (Production)**
```bash
# Build backend container
docker build -t amma-backend .

# Run with environment variables
docker run -p 8001:8080 \
  -e OPENAI_API_KEY=your_key_here \
  -e PORT=8080 \
  amma-backend

# Access:
# Backend: http://localhost:8001
# API Docs: http://localhost:8001/docs
```

### **Docker for Railway Deployment**
```bash
# The Dockerfile is optimized for Railway deployment
# Railway automatically:
# 1. Detects the Dockerfile
# 2. Sets PORT environment variable
# 3. Handles container orchestration

# For Railway:
# 1. Connect GitHub repo to Railway
# 2. Add OPENAI_API_KEY environment variable
# 3. Deploy automatically
```

## ☁️ Production Deployment

### **Backend (Railway)**
1. **Connect Repository**: Link your GitHub repo to Railway
2. **Environment Variables**: Add `OPENAI_API_KEY` in Railway dashboard
3. **Auto-Deploy**: Railway detects `Dockerfile` and deploys automatically
4. **Access**: `https://your-service.railway.app`

### **Frontend (GitHub Pages)**  
1. **Enable GitHub Pages**: Repository Settings → Pages → Source: "GitHub Actions"
2. **Environment Variables**: Add in Repository Settings → Actions → Variables:
   ```
   NEXT_PUBLIC_API_URL = https://your-backend.railway.app
   NEXT_PUBLIC_WS_URL = wss://your-backend.railway.app/ws
   ```
3. **Auto-Deploy**: Frontend deploys automatically on push to main
4. **Access**: `https://yourusername.github.io/repository-name/`

### **Complete Production Setup**
- **Backend**: Railway (handles WebSocket connections, API, story generation)
- **Frontend**: GitHub Pages (static React app, global CDN)
- **Connection**: Frontend connects to Railway backend via WebSocket
- **Cost**: GitHub Pages (free), Railway (free tier available)

## 📁 Project Structure

```
AMMA/
├── 🚀 Backend (Railway Deployment)
│   ├── src/amma/              # Core agent implementation
│   │   ├── graph.py          # Multi-agent orchestration
│   │   ├── prompts.py        # Agent system prompts
│   │   ├── state.py          # Pydantic state models
│   │   ├── tools.py          # ReAct tools
│   │   └── utils.py          # Utilities
│   ├── app.py                # FastAPI server + WebSocket
│   ├── Dockerfile            # Container configuration
│   └── pyproject.toml        # Python dependencies
├── 🎨 Frontend (GitHub Pages)
│   └── AMMA-UI/              # Next.js React application
│       ├── app/page.tsx      # Main chat interface
│       ├── components/       # UI components
│       └── lib/              # Utilities
├── 🔧 Local Development
│   ├── start_app.py          # Full-stack launcher
│   ├── main.py              # CLI interface
│   └── install.py           # Dependency installer
├── 🚀 Deployment
│   └── .github/workflows/    # GitHub Actions (frontend deployment)
└── 📖 Documentation
    └── README.md
```

## 🚀 Usage Examples

### **CLI Interface**
```bash
python main.py
# 🌙 AMMA - Bedtime Story Agent
# Press Ctrl+C to exit
# 
# You: Hi AMMA
# AMMA: Hello dear! I'm AMMA, your motherly storyteller...
```

### **Web Interface**
```bash
python start_app.py
# Visit: http://localhost:3000
# Chat with AMMA in a beautiful web interface
```

### **API Usage**
```bash
curl -X POST "http://localhost:8001/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Tell me a story about dragons", "session_id": "test123"}'
```

## 🎯 Key Features

- **🤖 Multi-Agent Architecture**: ReAct + Reflection patterns
- **🌙 Bedtime-Optimized**: Soothing tone, age-appropriate content
- **🔄 Story Revisions**: Iterative improvement based on user feedback
- **⚡ Real-Time Streaming**: WebSocket-based chat interface
- **🛡️ Safety-First**: Built-in content evaluation and filtering
- **📱 Responsive UI**: Works on desktop and mobile
- **🐳 Production-Ready**: Docker + Railway + GitHub Pages deployment
- **🔧 Developer-Friendly**: Local development tools and CLI interface

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **LangChain**: For LLM integration and agent framework
- **LangGraph**: For multi-agent orchestration
- **OpenAI**: For GPT models powering story generation
- **FastAPI**: For high-performance web API
- **Next.js**: For modern React framework
- **Railway**: For seamless backend deployment
- **GitHub Pages**: For free frontend hosting

---

*Built with ❤️ for creating magical bedtime experiences for children*
