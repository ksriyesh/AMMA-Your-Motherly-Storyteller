"""FastAPI server for AMMA bedtime story agent with streaming support."""

import asyncio
import json
import uuid
from typing import Dict, Optional

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

# Load environment variables from .env file
load_dotenv()

from src.amma.context import Context
from src.amma.graph import graph
from src.amma.state import State


# Pydantic models for API
class ChatMessage(BaseModel):
    message: str
    session_id: Optional[str] = None


class ChatResponse(BaseModel):
    response: str
    session_id: str
    status: str = "success"


# FastAPI app
app = FastAPI(
    title="AMMA - Bedtime Story Agent",
    description="A conversational AI that creates personalized bedtime stories for children",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for sessions (in production, use Redis or similar)
sessions: Dict[str, Dict] = {}


class ConnectionManager:
    """Manages WebSocket connections for streaming."""
    
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
    
    async def connect(self, websocket: WebSocket, session_id: str):
        await websocket.accept()
        self.active_connections[session_id] = websocket
    
    def disconnect(self, session_id: str):
        if session_id in self.active_connections:
            del self.active_connections[session_id]
    
    async def send_message(self, session_id: str, message: dict):
        if session_id in self.active_connections:
            websocket = self.active_connections[session_id]
            try:
                await websocket.send_text(json.dumps(message))
            except Exception:
                self.disconnect(session_id)


manager = ConnectionManager()


async def stream_response(session_id: str, response: str, base_delay: float = 0.03):
    """Stream response character by character to create typing effect."""
    try:
        # Send start streaming signal
        await manager.send_message(session_id, {
            "type": "stream_start",
            "content": ""
        })
        
        # Stream each character with variable delay for natural feel
        for i, char in enumerate(response):
            await manager.send_message(session_id, {
                "type": "stream_chunk",
                "content": char
            })
            
            # Variable delay: longer after punctuation, shorter for regular chars
            if char in '.!?':
                delay = base_delay * 8  # Longer pause after sentences
            elif char in ',;:':
                delay = base_delay * 4  # Medium pause after clauses
            elif char == ' ':
                delay = base_delay * 1.5  # Slightly longer for spaces
            else:
                delay = base_delay  # Normal speed for regular characters
            
            await asyncio.sleep(delay)
        
        # Send end streaming signal
        await manager.send_message(session_id, {
            "type": "stream_end",
            "content": ""
        })
        
    except Exception:
        # Fallback to regular response
        await manager.send_message(session_id, {
            "type": "response",
            "content": response
        })


async def run_amma_agent(message: str, session_id: str) -> str:
    """Run the AMMA agent and return the response."""
    try:
        # Get or create session state
        if session_id not in sessions:
            sessions[session_id] = {
                "state": State(messages=[]),
                "context": Context()
            }
        
        session_data = sessions[session_id]
        current_state = session_data["state"]
        context = session_data["context"]
        
        # Add user message to state
        from langchain_core.messages import HumanMessage
        user_message = HumanMessage(content=message)
        current_state.messages.append(user_message)
        
        # Run the agent
        result = await graph.ainvoke(
            current_state.model_dump(),
            config={"configurable": {"context": context}}
        )
        
        # Update session state
        updated_state = State(**result)
        sessions[session_id]["state"] = updated_state
        
        # Get the last AI message
        if updated_state.messages:
            last_message = updated_state.messages[-1]
            if hasattr(last_message, 'content'):
                return last_message.content
        
        return "I'm sorry, I couldn't generate a response. Please try again."
        
    except Exception as e:
        return f"I encountered an error: {str(e)}. Please try again."


@app.get("/", response_class=HTMLResponse)
async def get_chat_interface():
    """Serve a simple fallback chat interface."""
    return HTMLResponse(content="""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>AMMA - Bedtime Story Agent</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 600px; margin: 50px auto; padding: 20px; }
            .header { text-align: center; margin-bottom: 30px; }
            .info { background: #f5f5f5; padding: 20px; border-radius: 8px; }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🌙 AMMA</h1>
            <p>Bedtime Story Agent</p>
        </div>
        <div class="info">
            <h3>Welcome to AMMA!</h3>
            <p>For the best experience, please use the React frontend at:</p>
            <p><strong><a href="http://localhost:3000">http://localhost:3000</a></strong></p>
            <br>
            <p>API Status: <span style="color: green;">✓ Running</span></p>
            <p>WebSocket: <span style="color: green;">✓ Available</span></p>
            <p><a href="/docs">View API Documentation</a></p>
        </div>
    </body>
    </html>
    """)


@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(chat_message: ChatMessage):
    """Handle chat messages via REST API."""
    session_id = chat_message.session_id or str(uuid.uuid4())
    
    try:
        response = await run_amma_agent(chat_message.message, session_id)
        return ChatResponse(
            response=response,
            session_id=session_id,
            status="success"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    """WebSocket endpoint for streaming responses."""
    await manager.connect(websocket, session_id)
    
    # Send automatic greeting when client connects (only for new sessions)
    try:
        # Check if this is a new session (no messages yet)
        is_new_session = session_id not in sessions or len(sessions[session_id]["state"].messages) == 0
        
        if is_new_session:
            # Send typing indicator
            await manager.send_message(session_id, {
                "type": "typing",
                "content": "AMMA is preparing to greet you..."
            })
            
            # Get AMMA's greeting
            greeting_response = await run_amma_agent("hey", session_id)
            
            # Stream greeting response
            await stream_response(session_id, greeting_response)
        else:
            pass
        
    except Exception as e:
        await manager.send_message(session_id, {
            "type": "error",
            "content": f"Error: {str(e)}"
        })
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message_data = json.loads(data)
            message = message_data.get("message", "")
            
            if message:
                try:
                    # Send typing indicator
                    await manager.send_message(session_id, {
                        "type": "typing",
                        "content": "AMMA is thinking..."
                    })
                    
                    # Get response from AMMA
                    response = await run_amma_agent(message, session_id)
                    
                    # Send streaming response character by character
                    await stream_response(session_id, response)
                    
                except Exception as e:
                    await manager.send_message(session_id, {
                        "type": "error",
                        "content": f"Error: {str(e)}"
                    })
                    
    except WebSocketDisconnect:
        manager.disconnect(session_id)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "AMMA Bedtime Story Agent"}


@app.get("/sessions")
async def get_active_sessions():
    """Get information about active sessions (for debugging)."""
    return {
        "active_sessions": len(sessions),
        "websocket_connections": len(manager.active_connections),
        "session_ids": list(sessions.keys())
    }


@app.delete("/sessions/{session_id}")
async def clear_session(session_id: str):
    """Clear a specific session."""
    if session_id in sessions:
        del sessions[session_id]
        return {"message": f"Session {session_id} cleared"}
    else:
        raise HTTPException(status_code=404, detail="Session not found")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
        log_level="info"
    )
