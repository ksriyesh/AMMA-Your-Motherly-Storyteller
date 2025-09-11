# 🌙 AMMA 2.0 - Bedtime Story Agent

**AMMA** (Adaptive Multi-agent Motherly Assistant) is an intelligent conversational AI system that creates personalized bedtime stories for children. Built with a hybrid architecture combining **ReAct (Reasoning and Acting)** and **Reflection** patterns, AMMA provides natural conversation while generating high-quality, safe bedtime stories.

![AMMA Architecture](<img width="693" height="425" alt="image" src="https://github.com/user-attachments/assets/21c95737-c7f0-48ae-90c5-bf2cf0044db0" />
)
*Multi-agent architecture combining ReAct for interaction and Reflection for story creation*

## 🏗️ Architecture Overview

AMMA combines two powerful AI patterns:

### **ReAct Pattern (Interaction Layer)**
- **Purpose**: Natural conversation and preference collection
- **Agent**: AMMA conversational agent
- **Tools**: `update_story_preferences`, `request_new_story`
- **Flow**: Reason about user input → Act with appropriate tools → Respond naturally

### **Reflection Pattern (Story Creation Layer)**
- **Purpose**: High-quality story generation through iterative improvement
- **Agents**: Story Creator → Story Evaluator → Story Presenter
- **Flow**: Create story → Evaluate quality → Approve/Revise → Present final story

This hybrid approach ensures both **natural interaction** and **high-quality story output**.

## 🎯 Agent Flow

```
__start__ → amma → tools → amma → story_creator → story_evaluator
                   ↓                                    ↓
                __end__                            story_presenter
                   ↑                                    ↓
                   ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← __end__
                   ↑
            revision_handler ← ← ← (if needs revision)
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

## 🚀 Installation & Setup

### **Prerequisites**
- Python 3.11+
- Node.js 18+ (for frontend)
- OpenAI API key

### **Quick Setup**

**Option 1: One-Command Install (Recommended)**
```bash
# Install everything automatically
python install.py

# Or use platform-specific scripts:
# Windows: install.bat
# Linux/macOS: ./install.sh
```

**Option 2: Manual Setup**
```bash
# 1. Clone repository
git clone <repository-url>
cd Amma2.0

# 2. Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 3. Install Python dependencies
pip install -e .

# 4. Set up environment variables
echo "OPENAI_API_KEY=your_openai_api_key_here" > .env

# 5. Install frontend dependencies
cd AMMA-UI && npm install && cd ..
```

## 🎮 Usage Options

### **Option 1: Full Application (Recommended)**
Start both backend and frontend together:
```bash
python start_app.py
```
- **Frontend**: http://localhost:3000 (React chat interface)
- **Backend**: http://localhost:8001 (API + WebSocket)
- **API Docs**: http://localhost:8001/docs

### **Option 2: AMMA CLI**
Pure conversation interface:
```bash
python main.py
```
Simple command-line chat with AMMA - perfect for testing and development.

### **Option 3: Docker (Production Ready)**
```bash
# Quick start with Docker Compose
docker-compose up --build

# Or build manually
docker build -t amma-bedtime-stories .
docker run -p 3000:3000 -p 8001:8001 -e OPENAI_API_KEY=your_key amma-bedtime-stories
```

### **Option 4: Separate Services**

**Backend only:**
```bash
python -m uvicorn app:app --host 0.0.0.0 --port 8001 --reload
```

**Frontend only:**
```bash
cd AMMA-UI && npm run dev
```

## 🐳 Docker Deployment

Complete containerized setup with all dependencies:

```bash
# 1. Set up environment
echo "OPENAI_API_KEY=your_key_here" > .env

# 2. Run with Docker Compose
docker-compose up --build

# 3. Access application
# Frontend: http://localhost:3000
# Backend: http://localhost:8001
```

See [DOCKER_README.md](DOCKER_README.md) for detailed Docker documentation.

## 📁 Project Structure

```
Amma2.0/
├── src/amma/                 # 🧠 Core agent system
│   ├── graph.py             # Multi-agent orchestration & routing
│   ├── prompts.py           # Agent-specific prompts (AMMA, Creator, Evaluator)
│   ├── state.py             # Pydantic state management
│   ├── tools.py             # ReAct tools for preference updates
│   ├── context.py           # Configuration and model settings
│   └── utils.py             # Helper utilities
├── AMMA-UI/                 # 🎨 React frontend
│   ├── app/page.tsx         # Main chat interface
│   ├── components/          # UI components
│   └── styles/              # Tailwind CSS styling
├── app.py                   # 🚀 FastAPI server with WebSocket
├── main.py                  # 💬 CLI interface
├── start_app.py             # 🔧 Unified launcher
├── Dockerfile               # 🐳 Container setup
├── docker-compose.yml       # 🐙 Multi-service orchestration
└── tests/                   # 🧪 Test suite
```

## 🛠️ Key Technologies

- **🕸️ LangGraph**: Multi-agent orchestration and state management
- **🔗 LangChain**: LLM integration and tool calling
- **⚡ FastAPI**: High-performance backend with WebSocket support
- **⚛️ React/Next.js**: Modern frontend with real-time streaming
- **🎨 Tailwind CSS + shadcn/ui**: Beautiful, responsive UI components
- **📊 Pydantic**: Type-safe data validation and state modeling
- **🤖 OpenAI GPT-3.5-turbo**: Conversational AI and story generation

## 🎨 Features

### **✨ Core Capabilities**
- **Motherly Conversation**: Warm, nurturing interaction style
- **Personalized Stories**: Custom tales based on child's name and interests
- **Story Revisions**: Iterative improvement based on user feedback
- **Safety First**: Multi-layer content filtering and age-appropriate language
- **Real-time Streaming**: Character-by-character typing effect
- **Session Management**: Persistent conversations with state tracking

### **📖 Story Features**
- **Age Range**: 5-10 years old
- **Reading Time**: 5-10 minutes (700-1200 words)
- **Content**: Safe, soothing, educational with gentle morals
- **Style**: Inspired by classic children's literature
- **Quality**: Multi-agent evaluation and approval process

## 🔧 Configuration

### **Model Settings**
```python
# src/amma/context.py
model: str = "openai/gpt-3.5-turbo"  # Default model
```

### **Story Parameters**
- **Target Age**: 5-10 years
- **Reading Time**: 5-10 minutes
- **Safety Level**: Maximum (no scary content)
- **Revision Limit**: 3 iterations max

## 🌐 API Endpoints

- `GET /`: Simple fallback interface
- `WebSocket /ws/{session_id}`: Real-time chat with streaming
- `POST /chat/{session_id}`: REST API for chat messages
- `GET /docs`: Interactive Swagger documentation
- `GET /health`: Service health check

## 🚧 Development

### **Running Tests**
```bash
# Run all tests
python -m pytest tests/

# Run with coverage
python -m pytest tests/ --cov=src --cov-report=html
```

### **Code Quality**
```bash
# Format code
black src/ tests/

# Type checking
mypy src/

# Linting
flake8 src/ tests/
```

## 🔮 Future Enhancements

*From main.py comment:*
> If I had 2 more hours, I would properly integrate a voice module (maybe ElevenLabs) and look around for MCPs to fetch classic stories to generate even better bedtime tales.

- **🎵 Voice Integration**: Text-to-speech with ElevenLabs for audio stories
- **📚 Classic Story Database**: MCP integration for referencing timeless tales
- **🌍 Multi-language Support**: Stories in different languages
- **🎭 Character Voices**: Different voices for story characters
- **📱 Mobile App**: Native iOS/Android applications

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **LangGraph Team**: For the excellent multi-agent framework
- **OpenAI**: For powerful language models
- **Vercel**: For Next.js and deployment platform
- **shadcn**: For beautiful UI components
- **All Parents**: Who inspired the creation of a safe, nurturing AI storyteller

---

*Built with ❤️ for bedtime stories and sweet dreams* 🌙✨
