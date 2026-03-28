import json
import os
from pathlib import Path
from datetime import datetime

class MemoryManager:
    """Handles JSON-based memory storage for the AI assistant."""
    
    def __init__(self, memory_file="memory.json"):
        self.memory_file = memory_file
        self.memory = self._load_memory()
    
    def _load_memory(self):
        """Load memory from JSON file."""
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return self._create_default_memory()
        return self._create_default_memory()
    
    def _create_default_memory(self):
        """Create default memory structure."""
        return {
            "user_profile": {
                "name": "User",
                "preferences": {},
                "created_date": datetime.now().isoformat()
            },
            "conversation_history": [],
            "code_snippets": [],
            "notes": [],
            "brain_status": "offline",
            "voice_settings": {
                "enabled": True,
                "volume": 0.8,
                "speed": 1.0
            }
        }
    
    def save(self):
        """Save memory to JSON file."""
        try:
            with open(self.memory_file, 'w') as f:
                json.dump(self.memory, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving memory: {e}")
            return False
    
    def add_conversation(self, role, message):
        """Add a message to conversation history."""
        self.memory["conversation_history"].append({
            "role": role,
            "message": message,
            "timestamp": datetime.now().isoformat()
        })
        self.save()
    
    def get_conversation_history(self, limit=50):
        """Get recent conversation history."""
        return self.memory["conversation_history"][-limit:]
    
    def set_user_name(self, name):
        """Set user name."""
        self.memory["user_profile"]["name"] = name
        self.save()
    
    def get_user_name(self):
        """Get user name."""
        return self.memory["user_profile"].get("name", "User")
    
    def add_code_snippet(self, title, code, language="python"):
        """Save a code snippet."""
        self.memory["code_snippets"].append({
            "title": title,
            "code": code,
            "language": language,
            "timestamp": datetime.now().isoformat()
        })
        self.save()
    
    def add_note(self, note_text):
        """Add a note to memory."""
        self.memory["notes"].append({
            "text": note_text,
            "timestamp": datetime.now().isoformat()
        })
        self.save()
    
    def get_notes(self, limit=20):
        """Get recent notes."""
        return self.memory["notes"][-limit:]
    
    def set_brain_status(self, status):
        """Update brain status."""
        self.memory["brain_status"] = status
        self.save()
    
    def get_context_for_prompt(self):
        """Get contextual information for LLM prompts."""
        context = f"User Name: {self.get_user_name()}\n"
        context += f"Brain Status: {self.memory['brain_status']}\n"
        context += "Recent Context:\n"
        
        recent_conv = self.get_conversation_history(limit=10)
        for item in recent_conv[-5:]:
            context += f"  [{item['role']}]: {item['message'][:100]}\n"
        
        return context
