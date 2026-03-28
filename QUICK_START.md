# 🚀 EVE App - Quick Start Guide

## Status Summary

| Component | Status | Action |
|-----------|--------|--------|
| **Backend API** | ✅ Ready | Start now: `python3 backend/api.py` |
| **Database** | ✅ Ready | Auto-created on first run |
| **Ollama Integration** | ✅ Ready | Requires Ollama installed |
| **Flutter Source Code** | ✅ Complete | Ready for building |
| **APK Installer** | ⏳ Pending | Build on macOS 14.0+ or Linux |
| **DMG Installer** | ⏳ Pending | Build on macOS 14.0+ |

---

## 🎯 Quick Start (5 minutes)

### 1. Start the Backend (Your Mac)
```bash
cd /Users/admin/Documents/AIAIAI/EVE
source backend/venv/bin/activate
python3 backend/api.py
```

**Expected Output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

### 2. Test in Another Terminal
```bash
curl http://localhost:8000/health
```

**Expected Response:**
```json
{"status":"healthy","timestamp":"2024-01-15T10:30:00Z"}
```

### 3. Try Chat
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"Hello EVE","model":"mistral"}'
```

✅ **Backend is working!**

---

## 📱 Building APK & DMG

### Why Can't We Build Here?
macOS 12.0 doesn't meet Flutter's 14.0+ requirement. But the source code is ready!

### Option 1: GitHub Actions (Easiest ⭐)
```bash
# 1. Push code to GitHub
git push origin main

# 2. Workflows automatically build APK + DMG
# 3. Get files from GitHub Releases in ~10 minutes
```

**Pros:** Free, automatic, no setup
**Cons:** Need GitHub account

### Option 2: Build on macOS 14.0+
If you have another Mac with newer OS:
```bash
cd EVE
bash build_with_flutter.sh
# Creates APK + DMG in ~/installers/
```

### Option 3: Build on Linux
Any modern Linux (Ubuntu 20.04+):
```bash
cd EVE
flutter create eve_app
cd eve_app
flutter build apk --release
# Creates APK in build/app/outputs/flutter-app.apk
```

---

## 📁 Project Structure

```
EVE/
├── backend/               ← START HERE (Production-ready)
│   ├── api.py            ← REST server (starts on :8000)
│   ├── database.py       ← SQLite persistence
│   ├── ollama_manager.py ← Ollama control
│   ├── venv/             ← Python environment
│   └── requirements.txt   ← Dependencies
│
├── flutter_src/          ← Source code for building APK/DMG
│   ├── main.dart
│   ├── chat_screen.dart
│   ├── api_service.dart
│   └── message_bubble.dart
│
├── build_with_flutter.sh ← Use on macOS 14.0+ / Linux
├── BUILD_AND_DEPLOYMENT_GUIDE.md
├── ALTERNATIVE_BUILD_GUIDE.md
└── memory/               ← Database files created at runtime
    └── eve.db
```

---

## 🔌 API Quick Reference

### Health Check
```bash
curl http://localhost:8000/health
```

### Chat (Main Endpoint)
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is AI?",
    "model": "mistral"
  }'
```

### Get History
```bash
curl "http://localhost:8000/api/history?limit=10"
```

### Check Model Status
```bash
curl http://localhost:8000/api/model/status
```

### Save Data
```bash
curl -X POST http://localhost:8000/api/memory/save \
  -H "Content-Type: application/json" \
  -d '{
    "key": "user_name",
    "value": "Alice"
  }'
```

### Get Data
```bash
curl "http://localhost:8000/api/memory/get?key=user_name"
```

---

## 🛠️ Troubleshooting

### Backend Won't Start
```bash
# Check if port 8000 is in use
lsof -i :8000

# If yes, kill it:
kill -9 <PID>

# Or use different port:
API_PORT=8001 python3 backend/api.py
```

### Missing Ollama
```bash
# Install from: https://ollama.sh
# Then make sure it's running:
ollama serve

# Or let backend auto-start it (if installed):
# Just restart the backend
```

### Module Import Errors
```bash
# Make sure venv is activated:
source backend/venv/bin/activate

# Install missing dependencies:
pip install fastapi uvicorn sqlalchemy python-dotenv
```

### Cannot Build APK/DMG
```bash
# Your Mac: macOS 12.0
# Required: macOS 14.0+ / Linux / Windows 10+
# Solution: Use GitHub Actions (Option 1 above)
```

---

## 🚀 Deployment Checklist

- [ ] Backend running locally on your Mac
- [ ] Can connect to http://localhost:8000
- [ ] Can send chat messages to API
- [ ] Ollama installed and running
- [ ] Database created at `memory/eve.db`
- [ ] Build scripts ready (for other machine)
- [ ] Source code committed to GitHub
- [ ] GitHub Actions building APK/DMG
- [ ] APK downloaded from workflows
- [ ] DMG downloaded from workflows
- [ ] APK installed on Android device
- [ ] macOS DMG shows in Applications

---

## 📊 Performance Expectations

| Operation | Latency | Notes |
|-----------|---------|-------|
| Health check | <10ms | Direct response |
| Chat (first) | 1-5s | Model loading |
| Chat (after) | 500ms-2s | Token generation |
| Database query | <10ms | SQLite local |
| History retrieval | <50ms | Depends on size |

---

## 🔒 Security & Privacy

✅ **100% Local & Private:**
- No cloud APIs
- No data leaves your device
- All processing on local Ollama
- SQLite database on your Mac
- No telemetry or tracking

---

## 📞 Support

### Documentation
- `BUILD_AND_DEPLOYMENT_GUIDE.md` - Full build guide
- `ALTERNATIVE_BUILD_GUIDE.md` - For macOS 12.0 systems
- `API_DOCUMENTATION.md` - API reference
- `README.md` - Project overview

### Quick Links
- Backend source: `backend/api.py`
- Flutter source: `flutter_src/*.dart`
- Build script: `build_with_flutter.sh`
- Config: `backend/.env` (optional)

### Debug Mode
```bash
# Enable debug logging:
DEBUG=true python3 backend/api.py

# See SQL queries:
SQL_DEBUG=true python3 backend/api.py
```

---

## ✨ Next Steps

1. **Right now:**
   - Start backend: `python3 backend/api.py`
   - Test API: `curl http://localhost:8000/health`

2. **Within an hour:**
   - Build APK on compatible machine OR use GitHub Actions
   - Get both installers (APK + DMG)

3. **Today:**
   - Install APK on Android device
   - Install DMG on another macOS machine
   - Connect both to your backend

4. **Tomorrow:**
   - Customize with more models
   - Add personal data/memory
   - Deploy to other devices

---

**Backend Status:** ✅ Production-Ready  
**Build Status:** ⏳ Waiting for compatible machine  
**Overall:** 🟢 System operational, ready for deployment

Last Updated: 2024-01-15  
Version: EVE 1.0.0
