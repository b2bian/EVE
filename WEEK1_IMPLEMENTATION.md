# EVE Cross-Platform: Getting Started (Week 1)

**Status:** Ready to implement  
**Time to first working chat:** ~2 hours  
**Target Completion:** End of Week 1

---

## Phase 1: Groundwork (Hours 1-2)

### 1.1 Install Dependencies

```bash
# Install Flutter (if not already installed)
# macOS only (we'll build for Android later)
brew tap livekit/tap
brew install flutter
flutter doctor
# Should show: Android toolchain ✓, Flutter ✓, Xcode ✓

# Verify Flutter
flutter --version
```

### 1.2 Create Flutter Project

```bash
# Create new Flutter app for both Android + macOS
flutter create eve_app
cd eve_app

# Enable both platforms
flutter config --enable-android
flutter config --enable-macos

# Add dependencies to pubspec.yaml
flutter pub add http sqflite provider intl
flutter pub get

# Verify structure
ls -la lib/
# Should show main.dart, test/
```

### 1.3 Create Backend Python Service

```bash
# Back in EVE root directory
cd /Users/admin/Documents/AIAIAI/EVE

# Create backend service directory
mkdir -p backend

# Create Python virtual environment
python3 -m venv backend/venv
source backend/venv/bin/activate

# Install dependencies
pip install fastapi uvicorn sqlalchemy python-dotenv psutil requests

# Create requirements.txt for reproducibility
pip freeze > backend/requirements.txt
```

---

## Phase 2: Backend Service (Hours 2-4)

### 2.1 Create SQLite Database Module

**File:** `backend/database.py`

```python
import sqlite3
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional

class Database:
    def __init__(self, db_path: str = "memory/eve.db"):
        self.db_path = db_path
        Path(db_path).parent.mkdir(exist_ok=True)
        self.init_schema()
    
    def init_schema(self):
        """Initialize database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Messages table
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
        
        # Memories table
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
        
        # Settings table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT,
                type TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create indices for performance
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_messages_timestamp ON messages(timestamp)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_messages_role ON messages(role)')
        
        conn.commit()
        conn.close()
    
    def add_message(self, content: str, role: str, model: str = "ollama") -> str:
        """Add message to database"""
        import uuid
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
        
        return list(reversed(messages))  # Oldest first
    
    def save_memory(self, key: str, value: str, category: str = "general"):
        """Save user memory"""
        import uuid
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
```

### 2.2 Create Ollama Manager

**File:** `backend/ollama_manager.py`

```python
import subprocess
import requests
import time
import psutil
from typing import Optional

class OllamaManager:
    def __init__(self, host: str = "localhost", port: int = 11434):
        self.host = host
        self.port = port
        self.base_url = f"http://{host}:{port}"
        self.process: Optional[subprocess.Popen] = None
    
    def is_running(self) -> bool:
        """Check if Ollama server is responding"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=1)
            return response.status_code == 200
        except:
            return False
    
    def ensure_running(self):
        """Start Ollama if not already running"""
        if self.is_running():
            return True
        
        print("Starting Ollama...")
        try:
            self.process = subprocess.Popen(
                ["ollama", "serve"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            # Wait for startup
            for i in range(30):
                time.sleep(0.5)
                if self.is_running():
                    print("✓ Ollama started")
                    return True
            
            print("✗ Ollama failed to start")
            return False
        except Exception as e:
            print(f"✗ Error starting Ollama: {e}")
            return False
    
    def get_available_models(self) -> list:
        """List available Ollama models"""
        if not self.is_running():
            return []
        
        try:
            response = requests.get(f"{self.base_url}/api/tags")
            models = response.json().get("models", [])
            return [m["name"] for m in models]
        except:
            return []
    
    def generate(self, prompt: str, model: str = "mistral") -> str:
        """Generate response from Ollama"""
        if not self.is_running():
            return "Error: Ollama not running"
        
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": model,
                    "prompt": prompt,
                    "stream": False,
                    "temperature": 0.7
                },
                timeout=60
            )
            
            if response.status_code == 200:
                return response.json().get("response", "")
            else:
                return f"Error: {response.status_code}"
        except Exception as e:
            return f"Error: {str(e)}"
    
    def get_status(self) -> dict:
        """Get Ollama health status"""
        return {
            "running": self.is_running(),
            "models": self.get_available_models(),
            "host": self.host,
            "port": self.port,
            "url": self.base_url
        }
```

### 2.3 Create REST API Server

**File:** `backend/api.py`

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import os
from datetime import datetime
import uuid

# Import our modules
from database import Database
from ollama_manager import OllamaManager

# Initialize FastAPI
app = FastAPI(title="EVE API", version="0.1.0")

# Enable CORS for Flutter frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
db = Database("memory/eve.db")
ollama = OllamaManager()

# Request/Response models
class Message(BaseModel):
    content: str
    model: str = "mistral"

class MessageResponse(BaseModel):
    id: str
    response: str
    timestamp: str
    latency_ms: float

# ============= Chat Endpoints =============

@app.post("/api/chat", response_model=MessageResponse)
async def chat(msg: Message):
    """Send message and get AI response"""
    import time
    
    start = time.time()
    
    # Ensure Ollama is running
    ollama.ensure_running()
    
    # Generate response
    response = ollama.generate(msg.content, model=msg.model)
    
    # Save to database
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

# ============= Model Endpoints =============

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

# ============= Memory Endpoints =============

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

# ============= Health Check =============

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "ok",
        "timestamp": datetime.now().isoformat(),
        "ollama": ollama.get_status()
    }

# ============= Root Endpoint =============

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
    
    # Ensure Ollama is running
    print("Initializing...")
    ollama.ensure_running()
    
    # Start server
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        log_level="info"
    )
```

### 2.4 Create run script

**File:** `backend/run.sh`

```bash
#!/bin/bash

# Activate Python virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip > /dev/null 2>&1

# Install requirements
pip install -q -r requirements.txt

echo "🚀 Starting EVE Backend API..."
echo "📍 Server will run on http://127.0.0.1:8000"
echo "🎮 Swagger UI: http://127.0.0.1:8000/docs"
echo ""
echo "Press Ctrl+C to stop"
echo ""

# Start the API server
python3 api.py
```

### 2.5 Test Backend

```bash
# Navigate to backend directory
cd /Users/admin/Documents/AIAIAI/EVE/backend

# Make script executable
chmod +x run.sh

# Run backend
./run.sh

# In another terminal, test the API:
curl http://127.0.0.1:8000/health

# Test chat endpoint
curl -X POST http://127.0.0.1:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"content": "Hello, what is 2+2?", "model": "mistral"}'
```

---

## Phase 3: Flutter Frontend (Hours 4-8)

### 3.1 Create Chat Service

**File:** `eve_app/lib/services/api_service.dart`

```dart
import 'package:http/http.dart' as http;
import 'dart:convert';

class ApiService {
  static const String baseURL = 'http://127.0.0.1:8000/api';
  
  // Send chat message
  static Future<String> sendMessage(String content, {String model = 'mistral'}) async {
    try {
      final response = await http.post(
        Uri.parse('$baseURL/chat'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode({
          'content': content,
          'model': model,
        }),
      ).timeout(Duration(seconds: 60));

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        return data['response'];
      } else {
        return 'Error: ${response.statusCode}';
      }
    } catch (e) {
      return 'Error: $e';
    }
  }

  // Get message history
  static Future<List<Map>> getHistory({int limit = 50}) async {
    try {
      final response = await http.get(
        Uri.parse('$baseURL/history?limit=$limit'),
      );

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        return List<Map>.from(data['messages']);
      }
      return [];
    } catch (e) {
      print('Error: $e');
      return [];
    }
  }

  // Check Ollama status
  static Future<bool> checkModelStatus() async {
    try {
      final response = await http.get(
        Uri.parse('$baseURL/model/status'),
      ).timeout(Duration(seconds: 2));

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        return data['running'] == true;
      }
      return false;
    } catch (e) {
      return false;
    }
  }

  // Ensure model is running
  static Future<bool> ensureModelRunning() async {
    try {
      final response = await http.post(
        Uri.parse('$baseURL/model/ensure-running'),
      ).timeout(Duration(seconds: 30));

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        return data['success'] == true;
      }
      return false;
    } catch (e) {
      print('Error: $e');
      return false;
    }
  }
}
```

### 3.2 Create Chat Screen

**File:** `eve_app/lib/screens/chat_screen.dart`

```dart
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../services/api_service.dart';
import '../widgets/message_bubble.dart';

class ChatScreen extends StatefulWidget {
  @override
  _ChatScreenState createState() => _ChatScreenState();
}

class _ChatScreenState extends State<ChatScreen> {
  final TextEditingController _controller = TextEditingController();
  final List<Map<String, String>> messages = [];
  bool isLoading = false;
  bool modelRunning = false;
  ScrollController _scrollController = ScrollController();

  @override
  void initState() {
    super.initState();
    _initializeApp();
    _loadHistory();
  }

  void _initializeApp() async {
    // Check if Ollama is running
    bool running = await ApiService.checkModelStatus();
    if (!running) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Starting Ollama...'), duration: Duration(seconds: 2)),
      );
      await ApiService.ensureModelRunning();
    }
    setState(() => modelRunning = true);
  }

  void _loadHistory() async {
    final history = await ApiService.getHistory();
    setState(() {
      messages.clear();
      for (var msg in history) {
        messages.add({
          'role': msg['role'],
          'content': msg['content'],
          'timestamp': msg['timestamp'] ?? ''
        });
      }
    });
    _scrollToBottom();
  }

  void _scrollToBottom() {
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (_scrollController.hasClients) {
        _scrollController.animateTo(
          _scrollController.position.maxScrollExtent,
          duration: Duration(milliseconds: 300),
          curve: Curves.easeOut,
        );
      }
    });
  }

  void _sendMessage() async {
    if (_controller.text.isEmpty) return;

    String userMessage = _controller.text;
    _controller.clear();

    // Add user message to UI
    setState(() {
      messages.add({'role': 'user', 'content': userMessage});
      isLoading = true;
    });
    _scrollToBottom();

    // Send to backend
    String response = await ApiService.sendMessage(userMessage);

    // Add AI response
    setState(() {
      messages.add({'role': 'assistant', 'content': response});
      isLoading = false;
    });
    _scrollToBottom();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('EVE'),
        backgroundColor: Color(0xFF1a1a2e),
        elevation: 0,
        actions: [
          Padding(
            padding: EdgeInsets.all(16),
            child: Center(
              child: Text(
                modelRunning ? '🟢 Online' : '🔴 Offline',
                style: TextStyle(color: Colors.white),
              ),
            ),
          )
        ],
      ),
      backgroundColor: Color(0xFF16213e),
      body: Column(
        children: [
          Expanded(
            child: ListView.builder(
              controller: _scrollController,
              padding: EdgeInsets.all(12),
              itemCount: messages.length + (isLoading ? 1 : 0),
              itemBuilder: (context, index) {
                if (index == messages.length) {
                  return Padding(
                    padding: EdgeInsets.all(8),
                    child: Center(
                      child: SizedBox(
                        width: 24,
                        height: 24,
                        child: CircularProgressIndicator(
                          strokeWidth: 2,
                          valueColor: AlwaysStoppedAnimation<Color>(Color(0xFF00d4ff)),
                        ),
                      ),
                    ),
                  );
                }

                var msg = messages[index];
                return MessageBubble(
                  message: msg['content']!,
                  isUser: msg['role'] == 'user',
                );
              },
            ),
          ),
          Container(
            padding: EdgeInsets.all(12),
            color: Color(0xFF0f3460),
            child: Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: _controller,
                    style: TextStyle(color: Colors.white),
                    decoration: InputDecoration(
                      hintText: 'Type a message...',
                      hintStyle: TextStyle(color: Colors.grey),
                      border: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(8),
                        borderSide: BorderSide(color: Color(0xFF00d4ff)),
                      ),
                      filled: true,
                      fillColor: Color(0xFF1a1a2e),
                      contentPadding: EdgeInsets.symmetric(horizontal: 12, vertical: 10),
                    ),
                    onSubmitted: (_) => _sendMessage(),
                  ),
                ),
                SizedBox(width: 8),
                FloatingActionButton(
                  onPressed: isLoading ? null : _sendMessage,
                  backgroundColor: Color(0xFF00d4ff),
                  child: Icon(Icons.send, color: Color(0xFF1a1a2e)),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
```

### 3.3 Create Message Bubble Widget

**File:** `eve_app/lib/widgets/message_bubble.dart`

```dart
import 'package:flutter/material.dart';

class MessageBubble extends StatelessWidget {
  final String message;
  final bool isUser;

  MessageBubble({
    required this.message,
    required this.isUser,
  });

  @override
  Widget build(BuildContext context) {
    return Align(
      alignment: isUser ? Alignment.centerRight : Alignment.centerLeft,
      child: Container(
        margin: EdgeInsets.symmetric(vertical: 4),
        padding: EdgeInsets.symmetric(horizontal: 12, vertical: 8),
        constraints: BoxConstraints(maxWidth: MediaQuery.of(context).size.width * 0.8),
        decoration: BoxDecoration(
          color: isUser ? Color(0xFF00d4ff) : Color(0xFF0f3460),
          borderRadius: BorderRadius.only(
            topLeft: Radius.circular(12),
            topRight: Radius.circular(12),
            bottomLeft: Radius.circular(isUser ? 12 : 0),
            bottomRight: Radius.circular(isUser ? 0 : 12),
          ),
        ),
        child: Text(
          message,
          style: TextStyle(
            color: isUser ? Color(0xFF1a1a2e) : Colors.white,
            fontSize: 14,
          ),
        ),
      ),
    );
  }
}
```

### 3.4 Update main.dart

**File:** `eve_app/lib/main.dart`

```dart
import 'package:flutter/material.dart';
import 'screens/chat_screen.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'EVE',
      theme: ThemeData(
        primaryColor: Color(0xFF1a1a2e),
        scaffoldBackgroundColor: Color(0xFF16213e),
      ),
      home: ChatScreen(),
      debugShowCheckedModeBanner: false,
    );
  }
}
```

### 3.5 Run Flutter App

```bash
# Navigate to Flutter app
cd /Users/admin/Documents/AIAIAI/EVE/eve_app

# Get dependencies
flutter pub get

# Run on Mac (simulator or physical device)
flutter run -d macos

# Or build release
flutter build macos --release
```

---

## Phase 4: Testing & Verification (Hours 8-10)

### 4.1 Test Backend

```bash
# Terminal 1: Start backend
cd /Users/admin/Documents/AIAIAI/EVE/backend
./run.sh

# Terminal 2: Test endpoints
# Test health
curl http://127.0.0.1:8000/health | python3 -m json.tool

# Test chat
curl -X POST http://127.0.0.1:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"content": "What is the capital of France?"}' | python3 -m json.tool

# Test history
curl http://127.0.0.1:8000/api/history | python3 -m json.tool
```

### 4.2 Test Flutter App

```bash
# Make sure backend is running in Terminal 1
# In Terminal 2, run Flutter app
cd eve_app
flutter run -d macos

# Test:
# 1. Type a message
# 2. Wait for response
# 3. Check message appears in UI
# 4. Verify response time (should be <500ms)
```

### 4.3 Performance Check

```python
# Create test script
# File: backend/test_performance.py

import requests
import time
import json

base_url = "http://127.0.0.1:8000"

# Test 1: Response time
print("Testing response latency...")
for i in range(5):
    start = time.time()
    response = requests.post(
        f"{base_url}/api/chat",
        json={"content": f"Test message {i+1}"}
    )
    latency = (time.time() - start) * 1000
    data = response.json()
    actual_latency = data.get("latency_ms", 0)
    print(f"  Message {i+1}: {actual_latency:.0f}ms")

# Test 2: Message history
print("\nTesting history retrieval...")
start = time.time()
response = requests.get(f"{base_url}/api/history?limit=100")
latency = (time.time() - start) * 1000
print(f"  Load 100 messages: {latency:.0f}ms")

# Test 3: Model health
print("\nTesting model health...")
start = time.time()
response = requests.get(f"{base_url}/api/model/status")
latency = (time.time() - start) * 1000
print(f"  Model status check: {latency:.0f}ms")
```

---

## Week 1 Checklist

- [ ] **Day 1-2:** Flutter project created, backend service running
- [ ] **Day 3-4:** FastAPI endpoints working, SQLite database initialized
- [ ] **Day 5-6:** Chat screen UI complete, message history loads
- [ ] **Day 7:** End-to-end testing, performance meets targets

**Success Criteria for Week 1:**
- ✅ Flutter app starts and connects to backend
- ✅ Messages are sent and responses received
- ✅ Response latency <500ms
- ✅ Message history persists
- ✅ Zero crashes for 10+ message session
- ✅ Works on both Mac simulator and physical device

---

## If You Get Stuck

### Backend won't start?
```bash
# Check if Ollama is running
curl http://127.0.0.1:11434/api/tags

# If not, start it
ollama serve
```

### Flutter can't connect to backend?
```bash
# Make sure backend is accessible
curl http://127.0.0.1:8000/health

# Check firewall/network
netstat -an | grep 8000
```

### Database errors?
```bash
# Reset database
rm memory/eve.db
# Restart backend - will recreate schema

# Or inspect database
sqlite3 memory/eve.db ".tables"
sqlite3 memory/eve.db "SELECT COUNT(*) FROM messages;"
```

### Ollama not responding?
```bash
# Restart Ollama
pkill -f "ollama serve"
ollama serve

# Or download specific model first
ollama pull mistral
```

---

## Next: Week 2 Plan

After Week 1 MVP is working:
1. **Polish & Optimization** - Reduce latency further
2. **Android Support** - Build APK with Ollama
3. **Mac App** - Create .app bundle
4. **Distribution** - Prepare for release

---

**Ready to start?** Begin with `cd /Users/admin/Documents/AIAIAI/EVE && mkdir -p backend eve_app`

Run the commands from Phase 1 in order. You should have a working backend within 1 hour.
