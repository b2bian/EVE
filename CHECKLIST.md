# ✅ EVE Quick Action Checklist

**Goal:** Get EVE running from backend → installers → deployed on devices

---

## RIGHT NOW (5 minutes)

- [ ] Open terminal
- [ ] Run:
  ```bash
  cd /Users/admin/Documents/AIAIAI/EVE
  source backend/venv/bin/activate
  python3 backend/api.py
  ```
- [ ] See output: `INFO:     Uvicorn running on http://0.0.0.0:8000`
- [ ] In another terminal, run:
  ```bash
  curl http://localhost:8000/health
  ```
- [ ] See response: `{"status":"healthy",...}`

✅ **Backend is working!**

---

## TODAY (1 hour)

### Option A: GitHub Actions (Easiest ⭐)

- [ ] Create GitHub account (if needed)
- [ ] Create new repository: github.com/new
  - Name: `EVE`
  - Private: Your choice
  - Click "Create"
- [ ] In terminal:
  ```bash
  cd /Users/admin/Documents/AIAIAI/EVE
  git init
  git add .
  git commit -m "EVE App - Initial release"
  git branch -M main
  git remote add origin https://github.com/YOUR_USERNAME/EVE.git
  git push -u origin main
  ```
- [ ] Wait 10-15 minutes
- [ ] Go to Releases tab on GitHub
- [ ] Download `EVE-Android.apk` and `EVE-macOS.dmg`

✅ **Installers are ready!**

---

### Option B: macOS 14.0+ Machine

- [ ] Transfer entire `/Users/admin/Documents/AIAIAI/EVE` folder to Mac with 14.0+
- [ ] On that Mac, run:
  ```bash
  cd EVE
  bash build_with_flutter.sh
  ```
- [ ] Wait 20-30 minutes
- [ ] Find installers in `installers/` folder

✅ **Installers are ready!**

---

### Option C: Linux Machine

- [ ] Transfer `/Users/admin/Documents/AIAIAI/EVE` to Linux
- [ ] On Linux, run:
  ```bash
  cd EVE
  bash build_with_flutter.sh
  ```
- [ ] Wait 15-25 minutes
- [ ] Find APK in `eve_app/build/app/outputs/`
- [ ] For DMG: You need a Mac for that

✅ **APK is ready!**

---

## FOR ANDROID INSTALLATION

- [ ] Have Android phone/emulator ready
- [ ] Download `EVE-Android.apk` from GitHub Releases
- [ ] On Android phone:
  - [ ] Go to Settings → Security
  - [ ] Enable "Unknown Sources"
  - [ ] Copy APK to phone
  - [ ] Tap to install EVE
  - [ ] Open EVE app
  - [ ] When app asks for backend URL, enter:
    - Local network: `http://YOUR_MAC_IP:8000`
    - OR: `http://localhost:8000` if on same network

✅ **Android app is running!**

---

## FOR MACOS INSTALLATION

- [ ] Download `EVE-macOS.dmg` from GitHub Releases
- [ ] Double-click to mount DMG
- [ ] Drag `EVE.app` to Applications folder
- [ ] Eject the DMG
- [ ] Open Applications folder
- [ ] Double-click `EVE.app` to launch
- [ ] App auto-connects to backend on localhost:8000

✅ **macOS app is running!**

---

## TESTING BOTH APPS

- [ ] Backend running on your Mac:
  ```bash
  python3 backend/api.py
  ```
- [ ] On Android: Type a message → See response
- [ ] On macOS: Type a message → See response
- [ ] Test different models (optional):
  ```bash
  # First, install more models on your Mac:
  ollama pull neural-chat
  ```

✅ **Full system is working!**

---

## OPTIONAL CUSTOMIZATIONS

- [ ] Change model in backend (edit `backend/api.py`)
- [ ] Customize UI colors (edit Flutter code)
- [ ] Add more memory features (edit `backend/database.py`)
- [ ] Deploy backend to cloud (see BUILD_AND_DEPLOYMENT_GUIDE.md)

---

## TROUBLESHOOTING CHECKLIST

### Backend won't start
- [ ] Port 8000 available?
  ```bash
  lsof -i :8000
  ```
- [ ] Try different port:
  ```bash
  API_PORT=8001 python3 backend/api.py
  ```

### Ollama not found
- [ ] Install from https://ollama.sh
- [ ] Start manually:
  ```bash
  ollama serve
  ```

### API connection fails
- [ ] Backend running?
  ```bash
  curl http://localhost:8000/health
  ```
- [ ] Check firewall permissions

### APK won't install
- [ ] Android 7.0+?
- [ ] "Unknown Sources" enabled?
- [ ] File not corrupted?

### macOS app won't launch
- [ ] Eject DMG first
- [ ] Try dragging app again
- [ ] Check if backend running

---

## SUCCESS CRITERIA

You've succeeded when:

- [x] Backend starts without errors
- [x] `curl http://localhost:8000/health` works
- [x] GitHub has your code
- [x] APK downloaded from Releases
- [x] DMG downloaded from Releases
- [x] APK installed on Android (or can be)
- [x] DMG installed on macOS
- [x] Both apps connect to backend
- [x] Both apps receive responses
- [x] Database has messages: `memory/eve.db`

---

## QUICK REFERENCE

| Command | Purpose |
|---------|---------|
| `python3 backend/api.py` | Start backend |
| `curl http://localhost:8000/health` | Test backend |
| `git push origin main` | Trigger GitHub Actions |
| `bash build_with_flutter.sh` | Build on compatible machine |

---

## ESTIMATED TIMELINE

```
Right now:    Start backend (5 min)
Today:        Build installers (15-30 min)
Today:        Install APK (5 min)
Today:        Install DMG (5 min)
Today:        Enjoy EVE! (all day)
```

---

## FINAL CHECKLIST

- [ ] Backend running
- [ ] Health check passes
- [ ] Code pushed to GitHub (or building locally)
- [ ] Installers downloaded
- [ ] APK installed on Android
- [ ] DMG installed on macOS
- [ ] Both apps connect to backend
- [ ] Sent test messages
- [ ] Database has messages stored
- [ ] Ready to grow! 🚀

---

**Status:** green

**Next action:** Run `python3 backend/api.py` NOW!

**Questions?** See documentation in `/Users/admin/Documents/AIAIAI/EVE/`
