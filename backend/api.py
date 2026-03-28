import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from datetime import datetime

try:
    from .database import Database
    from .ollama_manager import OllamaManager
except ImportError:
    from database import Database
    from ollama_manager import OllamaManager

app = FastAPI(title="EVE API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db = Database()
ollama = OllamaManager()

class Message(BaseModel):
    content: str
    model: str = "mistral"

class MessageResponse(BaseModel):
    id: str
    response: str
    timestamp: str
    latency_ms: float

@app.post("/api/chat", response_model=MessageResponse)
async def chat(msg: Message):
    """Send message and get AI response"""
    import time
    
    start = time.time()
    ollama.ensure_running()
    
    response = ollama.generate(msg.content, model=msg.model)
    
    user_id = db.add_message(msg.content, role="user", model=msg.model)
    response_id = db.add_message(response, role="assistant", model=msg.model)
    
    latency = (time.time() - start) * 1000
    
    return MessageResponse(
        id=response_id,
        response=response,
        timestamp=datetime.now().isoformat(),
        latency_ms=latency
    )

@app.get("/api/history")
async def get_history(limit: int = 50, offset: int = 0):
    """Get message history"""
    messages = db.get_message_history(limit=limit, offset=offset)
    return {
        "messages": messages,
        "count": len(messages)
    }

@app.get("/api/model/status")
async def model_status():
    """Check Ollama status"""
    return ollama.get_status()

@app.post("/api/model/ensure-running")
async def ensure_model_running():
    """Ensure Ollama is running"""
    success = ollama.ensure_running()
    return {
        "success": success,
        "running": ollama.is_running()
    }

@app.post("/api/memory/save")
async def save_memory(data: dict):
    """Save memory entry"""
    key = data.get("key")
    value = data.get("value")
    category = data.get("category", "general")
    
    db.save_memory(key, value, category)
    
    return {"success": True, "key": key}

@app.get("/api/memory/get/{key}")
async def get_memory(key: str):
    """Get memory entry"""
    value = db.get_memory(key)
    return {
        "key": key,
        "value": value,
        "found": value is not None
    }

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "ok",
        "timestamp": datetime.now().isoformat(),
        "ollama": ollama.get_status()
    }

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "EVE API",
        "version": "0.1.0",
        "endpoints": {
            "chat": "POST /api/chat",
            "history": "GET /api/history",
            "model_status": "GET /api/model/status",
            "health": "GET /health"
        }
    }

if __name__ == "__main__":
    import uvicorn
    
    print("Initializing...")
    ollama.ensure_running()
    
    print("🚀 Starting EVE Backend API...")
    print("📍 Server running on http://127.0.0.1:8000")
    print("🎮 Swagger UI: http://127.0.0.1:8000/docs")
    
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        log_level="info"
    )
