# EVE Cross-Platform Architecture
## Local-First, Offline-First, Top-Tier Performance

**Status:** Architecture Blueprint  
**Target:** MVP in 2 weeks  
**Timeline:** Phase 1 (MVP) | Phase 2 (Polish) | Phase 3 (Growth)

---

## Executive Summary

Transform EVE from Mac-desktop app into a **production-grade cross-platform AI assistant** that works identically on both Android phone (primary) and Mac desktop, with:
- ✅ 100% offline operation (no internet required)
- ✅ Local Ollama LLM backend
- ✅ <500ms response latency (top-tier performance)
- ✅ Seamless data sync between devices
- ✅ Single source code (Flutter frontend)
- ✅ MVP launchable in 2 weeks

---

## Tech Stack: Why This Matters

### Frontend: Flutter (Both Android + Mac)

**Why Flutter:**
- Single codebase = faster 2-week MVP
- Compiles to native code = top-tier performance
- Perfect offline-first capabilities
- Excellent process management (can launch/manage Ollama)
- Hot reload during development (critical for 2-week timeline)
- Professional UI/UX out of box

**Alternatives Considered:**
- React Native: Slower for offline/process management
- Native Swift + Kotlin: 4x development time, two codebases
- Python (Kivy): Fragmented, poor mobile performance
- Web-based: Can't reliably manage local processes

**Decision:** ✅ **Flutter** - Best risk/reward for timeline

### Backend: Lightweight REST API Wrapper

**Why:**
- Keep existing Python/Ollama logic
- Flutter calls HTTP REST endpoints
- Can run as:
  - Service on Android (foreground service for Ollama)
  - CLI process on Mac (launched by Flutter)
  - Full server on Linux (future)

**Tech:** FastAPI (Python) - minimal, fast, perfect for this

### Data Storage: SQLite + JSON Sync

**Why SQLite:**
- Single-database model (no fragmentation)
- Works offline completely
- Queryable (vs JSON which isn't)
- Efficient sync (compare row checksums)
- Both Android and desktop support native SQLite

**Sync Strategy:**
- Each device has local SQLite copy
- Changes marked with timestamp + device UUID
- Sync when devices connect on same network
- Last-write-wins conflict resolution (configurable)

### Background Service: Ollama Process Manager

**Role:**
- Launches Ollama if not running
- Monitors health/resource usage
- Handles process restarts
- Exposes via local HTTP API

**Implementation:**
- Android: Foreground service + notification
- Mac: Daemon process managed by Flutter
- Both: Same interface (HTTP POST to localhost:11434)

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                   FLUTTER UI LAYER                          │
│        (Single codebase, both Android + Mac)                │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ Chat Screen  │  │ Memory View   │  │ Settings     │     │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘     │
│         │                 │                 │              │
│         └─────────────────┼─────────────────┘              │
│                           │                                │
│                    Local HTTP Calls                        │
└───────────────────────────┼────────────────────────────────┘
                            │
         ┌──────────────────╫──────────────────┐
         │                  │                  │
    ┌────▼────────┐   ┌────▼────────┐   ┌────▼──────┐
    │ BACKEND     │   │ BACKGROUND  │   │ DATA SYNC │
    │ SERVICE     │   │ SERVICE     │   │ SERVICE   │
    │ (FastAPI)   │   │ (Ollama     │   │ (P2P)     │
    │ :8000       │   │ Manager)    │   │           │
    │             │   │ :11434      │   │           │
    └────┬────────┘   └────┬────────┘   └────┬──────┘
         │                 │                  │
         │            ┌────▼────────┐        │
         │            │   OLLAMA    │        │
         │            │  LOCAL LLM  │        │
         │            │  (7B/13B)   │        │
         │            └─────────────┘        │
         │                                   │
    ┌────▼──────────────┐         ┌─────────▼──────┐
    │ SQLite Database   │         │ Local Network  │
    │ (All data local)  │         │ Sync (optional)│
    └───────────────────┘         └────────────────┘
```

---

## Component Breakdown

### 1. Flutter Frontend (Core - 2 Week MVP)

**Screens:**
- **Chat Interface** - Primary interaction (like current CLI)
- **Memory/History** - Conversation history, searchable
- **Settings** - Model selection, performance tuning
- **Profile** - User settings, appearance
- **System Status** - CPU/RAM/Ollama health

**Key Features:**
- Message history with timestamps
- Quick commands (/status, /name, etc.)
- Typing indicators
- Auto-scroll to latest message
- Offline validation (works even if backend crashes)

**Performance Optimization:**
- Lazy load history (not all at once)
- Message caching in SQLite
- JWT tokens for local auth
- Debounced auto-save

**Technology:**
```yaml
dependencies:
  flutter: latest
  http: ^0.13.0              # HTTP calls to backend
  sqflite: ^2.0.0            # Local database
  provider: ^6.0.0           # State management
  intl: ^0.17.0              # Localization/formatting
  animations: ^2.0.0         # Smooth UI
```

**Folder Structure:**
```
lib/
├── screens/
│   ├── chat_screen.dart
│   ├── memory_screen.dart
│   ├── settings_screen.dart
│   └── profile_screen.dart
├── services/
│   ├── api_service.dart       # HTTP calls
│   ├── database_service.dart  # SQLite ops
│   └── sync_service.dart      # Data sync
├── models/
│   ├── message.dart
│   ├── user.dart
│   └── settings.dart
├── widgets/
│   ├── message_bubble.dart
│   └── status_bar.dart
└── main.dart
```

---

### 2. Backend REST API (FastAPI, Python)

**Purpose:** Thin wrapper around existing EVE logic

**Endpoints:**

```
POST   /api/chat              Send message, get response
GET    /api/history           Get message history
GET    /api/model/status      Check Ollama health
POST   /api/memory/save       Save memory entry
GET    /api/memory/list       List memories
POST   /api/settings/set      Update settings
GET    /api/system/status     CPU/RAM/Ollama status
POST   /api/sync/pull         Get changes from peer
POST   /api/sync/push         Send changes to peer
```

**Implementation:**
```python
# backend/api.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import json
from datetime import datetime
from utils.ollama_handler import OllamaHandler
from utils.memory import MemoryManager
from utils.system_monitor import SystemMonitor

app = FastAPI()

# CORS for Flutter frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ollama = OllamaHandler()
memory = MemoryManager(db_path="memory/eve.db")
monitor = SystemMonitor()

@app.post("/api/chat")
async def chat(message: dict):
    """Process user message and return AI response"""
    user_msg = message.get("text", "")
    response = ollama.generate(user_msg)
    
    # Save to memory
    memory.add_message(user_msg, response)
    
    return {
        "response": response,
        "timestamp": datetime.now().isoformat(),
        "model": "ollama"
    }

@app.get("/api/model/status")
async def model_status():
    """Check if Ollama is running"""
    return {
        "running": ollama.is_running(),
        "model": ollama.current_model or "none",
        "latency_ms": ollama.get_latency()
    }

# ... more endpoints
```

**Key Files to Adapt:**
- `utils/ollama_handler.py` → Expose via REST
- `utils/memory.py` → SQLite adapter
- `utils/system_monitor.py` → API endpoint
- `utils/personal_brain.py` → Memory endpoint

---

### 3. Ollama Background Service Manager

**Android Implementation:**
```kotlin
// android/app/src/main/kotlin/com/eve/OllamaService.kt
class OllamaService : Service() {
    private val ollama = OllamaManager()
    
    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        // Keep Ollama running in foreground
        startForeground(NOTIFICATION_ID, createNotification())
        ollama.ensureRunning()
        return START_STICKY
    }
    
    // Monitor every 10 seconds
    private fun monitorOllama() {
        Timer().scheduleAtFixedRate(0, 10000) {
            if (!ollama.isRunning()) {
                ollama.start()
            }
        }
    }
}
```

**Mac Implementation:**
```python
# backend/ollama_manager.py
class OllamaManager:
    def ensure_running(self):
        """Start Ollama if not already running"""
        if not self.is_running():
            subprocess.Popen([
                "ollama", "serve"
            ], stdout=subprocess.DEVNULL)
            time.sleep(2)  # Wait for startup
    
    def is_running(self):
        """Check if Ollama HTTP server is available"""
        try:
            response = requests.get("http://localhost:11434/api/tags", timeout=1)
            return response.status_code == 200
        except:
            return False
```

---

### 4. Data Sync Layer (Optional for MVP)

**Purpose:** Keep Android and Mac data in sync

**Mechanism:**
- SQLite on both devices
- When on same network: devices discover each other
- Sync changes (only new messages, not full database)
- Conflict resolution: last-write-wins with device priority

**File:** `backend/sync.py`
```python
class SyncEngine:
    def get_changes_since(self, timestamp: datetime, device_uuid: str):
        """Get all changes since timestamp"""
        conn = sqlite3.connect('memory/eve.db')
        conn.row_factory = sqlite3.Row
        
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM messages 
            WHERE sync_timestamp > ? 
            AND device_uuid != ?
            ORDER BY sync_timestamp DESC
        """, (timestamp, device_uuid))
        
        return [dict(row) for row in cursor.fetchall()]
    
    def apply_changes(self, changes: list):
        """Merge remote changes into local DB"""
        for change in changes:
            # Last-write-wins
            existing = self.get_message(change['id'])
            if existing is None or existing['timestamp'] < change['timestamp']:
                self.insert_message(change)
```

---

## Implementation Roadmap

### Week 1: Core MVP (Android + Mac Working)

**Days 1-2: Flutter UI Foundation**
- Create new Flutter project (both Android + Mac target)
- Build chat screen with message list
- Build settings/profile screens
- Create HTTP service layer

**Days 3-4: Backend Service**
- Build FastAPI wrapper (5 simple endpoints)
- Adapt existing Python code
- SQLite database setup
- Ollama health check

**Days 5-6: Integration**
- Connect Flutter to FastAPI
- Test chat flow end-to-end
- Mac: Manual Ollama launch (user clicks button)
- Android: Foreground service for Ollama

**Days 7: Polish & Testing**
- Error handling
- Offline fallbacks
- Performance profiling
- Memory/history sync

### Week 2: Polish & Distribution

**Days 8-10: Optimization**
- Top-tier performance tuning
- Message caching
- Lazy loading history
- Reduce latency

**Days 11-12: Android Release**
- Ollama embedded/download system
- APK generation
- Testing on real device
- Play Store prep

**Days 13-14: Mac Release**
- Mac app bundle
- Ollama startup automation
- DMG installer
- TestFlight/Release prep

---

## Data Model: SQLite Schema

```sql
-- Messages table
CREATE TABLE messages (
    id TEXT PRIMARY KEY,
    user_id TEXT,
    content TEXT,
    role TEXT,  -- "user" or "assistant"
    timestamp DATETIME,
    model TEXT,
    tokens_used INTEGER,
    sync_timestamp DATETIME,
    device_uuid TEXT
);

-- Memories table
CREATE TABLE memories (
    id TEXT PRIMARY KEY,
    key TEXT UNIQUE,
    value TEXT,
    category TEXT,
    timestamp DATETIME,
    device_uuid TEXT
);

-- Settings table
CREATE TABLE settings (
    key TEXT PRIMARY KEY,
    value TEXT,
    type TEXT,  -- string, integer, boolean
    timestamp DATETIME
);

-- Sync log (for P2P sync)
CREATE TABLE sync_log (
    id TEXT PRIMARY KEY,
    table_name TEXT,
    operation TEXT,
    timestamp DATETIME,
    device_uuid TEXT,
    synced INTEGER DEFAULT 0
);
```

---

## Performance Targets (Top-Tier)

| Metric | Target | How |
|--------|--------|-----|
| **First message response** | <500ms | Cache model in RAM, optimize prompts |
| **Message display latency** | <50ms | Local rendering, no network wait |
| **History load (100 msgs)** | <200ms | SQLite indexing, lazy loading |
| **App startup** | <2s | Lazy initialize services |
| **Memory usage** | <150MB | Stream responses, don't buffer |
| **Ollama health check** | <100ms | Local TCP, no I/O overhead |

**Optimization Strategy:**
1. Measure: Use Flutter DevTools profiler
2. Cache aggressively: Messages, model, settings
3. Stream responses: Don't wait for full completion
4. Async/await: Never block UI thread
5. Index SQLite: On timestamp, device_uuid, role

---

## Deployment & Distribution

### Android
```
1. Generate release key
2. Build APK + App Bundle (Google Play)
3. Include Ollama build for ARM64
4. Auto-download if not present
5. Play Store listing with "Offline-first AI"
```

### Mac
```
1. Code sign for Gatekeeper
2. Create DMG installer
3. Include Ollama launch script
4. TestFlight for beta testing
5. App Store or direct distribution
```

---

## Growth Roadmap (Phase 2+)

### Immediate (After MVP)
- [ ] Voice input/output (whisper + TTS)
- [ ] Custom personality system
- [ ] Plugin architecture
- [ ] Scheduled reminders
- [ ] Export conversations

### Medium-term (Month 2-3)
- [ ] Multi-device sync (cloud option)
- [ ] Collaborative features (share conversations)
- [ ] Mobile app polish (Material 3 design)
- [ ] Performance: Try quantized 4-bit models
- [ ] Windows support

### Long-term (Month 4+)
- [ ] Alternative LLM engines (LLaMA, Mistral)
- [ ] Fine-tuning on user data
- [ ] Mobile agent (automation/scripts)
- [ ] Monetization (pro features)
- [ ] API for third-party apps

---

## Risk Assessment & Mitigation

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|-----------|
| Flutter learning curve | High delay | Medium | Use pre-built templates, tutorials |
| Ollama on mobile | Can't work offline | High | Pre-package quantized model APK |
| SQLite sync conflicts | Data loss | Low | Last-write-wins + tests |
| High latency > 500ms | Poor UX | Medium | Aggressive caching + model quantization |
| App crashes | Unusable | Low | Crash reporting, error boundaries |

---

## Success Criteria (MVP Definition)

✅ **MUST HAVE:**
- [ ] Chat works identically on Android + Mac
- [ ] 100% offline operation (no internet)
- [ ] Response latency <500ms
- [ ] Memory persists between sessions
- [ ] No crashes for 1-hour session
- [ ] Can send 100+ messages without degradation

✅ **SHOULD HAVE:**
- [ ] Message history search
- [ ] Settings persistence
- [ ] System status monitoring
- [ ] Beautiful UI (cyberpunk theme)

✅ **NICE TO HAVE:**
- [ ] P2P sync between Android + Mac
- [ ] Voice input
- [ ] Export conversations

---

## Getting Started Next

### Step 1: Project Setup (30 mins)
```bash
flutter create eve_app
cd eve_app

# Add targets
flutter config --enable-android
flutter config --enable-macos

# Add dependencies
flutter pub add http sqflite provider
```

### Step 2: Backend Setup (45 mins)
```bash
# Create backend service
mkdir -p backend
cd backend
python3 -m venv venv
source venv/bin/activate
pip install fastapi uvicorn sqlite3 psutil requests

# Copy existing code
cp ../utils/* ./
```

### Step 3: First Endpoint (1 hour)
- Create simple POST /api/chat endpoint
- Test with curl
- Connect Flutter UI

### Step 4: Deploy to Android (varies)
- Install Android SDK
- Configure signing
- Build APK
- Test on real device

---

## Files to Create/Modify

```
EVE/
├── frontend/                    # NEW: Flutter app
│   ├── lib/
│   │   ├── screens/
│   │   ├── services/
│   │   ├── models/
│   │   └── main.dart
│   ├── android/
│   ├── macos/
│   └── pubspec.yaml
│
├── backend_api/                 # NEW: REST API wrapper
│   ├── api.py                   # NEW: FastAPI server
│   ├── ollama_manager.py        # NEW: Process management
│   ├── sync_engine.py           # NEW: Data sync
│   └── requirements.txt
│
├── utils/                       # MODIFIED: Adapt for REST
│   ├── memory.py               # Add SQLite support
│   ├── ollama_handler.py       # Expose as API
│   └── system_monitor.py       # Add API endpoint
│
└── memory/
    └── eve.db                   # NEW: SQLite database
```

---

## Estimated Effort Breakdown

| Component | Time | Difficulty |
|-----------|------|-----------|
| Flutter UI setup | 6h | Medium |
| Backend REST API | 4h | Easy |
| SQLite data layer | 3h | Easy |
| Ollama manager | 4h | Medium |
| Testing & debugging | 8h | Medium |
| Polishing & optimization | 8h | High |
| **TOTAL (MVP)** | **~33 hours** | **Average: Medium** |

**With 2-week timeline:** ~28 hours/week = ~4 hours/day = 100% feasible

---

## Success Metrics (Post-Launch)

- ✅ App runs for 8+ hours without crash
- ✅ Response latency averages <400ms
- ✅ Message history search works instantly
- ✅ Data persists perfectly between sessions
- ✅ Works on both Android 12+ and Mac 12+
- ✅ Uses <300MB RAM on phone, <200MB on desktop
- ✅ Zero external API calls (completely offline)

---

## Go/No-Go Decision Points

### End of Week 1:
- **GO:** Chat works, backend responds, basic UI functional
- **NO-GO:** Major architectural issues, Flutter/backend can't integrate

### End of Week 2:
- **GO:** Both platforms functional, MVP ready for real usage
- **NO-GO:** Critical bugs, performance inadequate, crashing

---

**Next Step:** Start with Flutter project setup if approved. Expected timeline: 2 weeks to production MVP on both platforms.
