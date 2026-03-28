import sqlite3
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
import uuid

class Database:
    def __init__(self, db_path: str = "../memory/eve.db"):
        self.db_path = db_path
        Path(db_path).parent.mkdir(exist_ok=True)
        self.init_schema()
    
    def init_schema(self):
        """Initialize database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id TEXT PRIMARY KEY,
                user_id TEXT,
                content TEXT NOT NULL,
                role TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                model TEXT,
                tokens_used INTEGER,
                device_uuid TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS memories (
                id TEXT PRIMARY KEY,
                key TEXT UNIQUE,
                value TEXT,
                category TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                device_uuid TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT,
                type TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_messages_timestamp ON messages(timestamp)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_messages_role ON messages(role)')
        
        conn.commit()
        conn.close()
    
    def add_message(self, content: str, role: str, model: str = "ollama") -> str:
        """Add message to database"""
        msg_id = str(uuid.uuid4())
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO messages (id, content, role, model)
            VALUES (?, ?, ?, ?)
        ''', (msg_id, content, role, model))
        conn.commit()
        conn.close()
        
        return msg_id
    
    def get_message_history(self, limit: int = 100, offset: int = 0) -> List[Dict]:
        """Get message history"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM messages 
            ORDER BY timestamp DESC 
            LIMIT ? OFFSET ?
        ''', (limit, offset))
        
        messages = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return list(reversed(messages))
    
    def save_memory(self, key: str, value: str, category: str = "general"):
        """Save user memory"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT OR REPLACE INTO memories (id, key, value, category)
                VALUES (?, ?, ?, ?)
            ''', (str(uuid.uuid4()), key, value, category))
        except:
            pass
        
        conn.commit()
        conn.close()
    
    def get_memory(self, key: str) -> Optional[str]:
        """Retrieve user memory"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT value FROM memories WHERE key = ?', (key,))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else None
