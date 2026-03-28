# EVE - Quick Reference Card

## 🚀 Launch Application

```bash
cd /Users/admin/Documents/AIAIAI/EVE
source venv/bin/activate  # Activate virtual environment
python3 main.py           # Launch app
```

Or use the convenience script:
```bash
./run.sh
```

## 🧠 Enable AI Features

Start Ollama in a **separate terminal**:
```bash
ollama serve
```

Then launch EVE in another terminal - it will auto-detect Ollama!

## 🎤 Enable Voice Input

```bash
source venv/bin/activate
pip install faster-whisper
# Then restart EVE
python3 main.py
```

## 📝 User Interface Guide

```
┌──────────────────────────────────────────────────────┐
│ ◇ EVE ◇                      [Brain Status] [Sys]    │
├────────┬────────────────────────────┬────────────────┤
│ ⚙ CPU  │                            │ 📝 / 🎙        │
│ 📊 RAM │   Terminal Chat Area       │                │
│ ⚡ Brain│   Messages appear here     │ Notes/Voice    │
│ 👤 User│   Real-time responses      │ Settings       │
├────────┴────────────────────────────┴────────────────┤
│ 🎤 Voice │ Name: [____] SET │ [Type message...] SEND│
└─────────────────────────────────────────────────────┘
```

## ⌨️ Keyboard Shortcuts

| Action | Shortcut |
|--------|----------|
| Send message | `Enter` |
| Toggle voice | Click 🎤 button |
| Cancel operation | `Ctrl+C` (in terminal) |
| Quit app | Close window |

## 🎨 Customize Colors

Edit `style_config.json`:

```json
"colors": {
  "background": "#1a1a1a",      // Dark background
  "accent_cyan": "#00f2ff",     // Main UI color
  "accent_orange": "#ff9d00",   // Headers
  "warning": "#ff3333",         // Errors
  "success": "#00ff00"          // Positive feedback
}
```

Then restart the app!

## 🔧 Common Tasks

### Change Default AI Model
Edit `style_config.json`:
```json
"ollama": {
  "model": "mistral"  // or llama2, neural-chat, etc.
}
```

### Adjust Voice Settings
Settings Tab → Select Model, Personality, Speed

### Clear Conversation History
```bash
rm memory.json
# Restart app - new user data created
```

### Check System Requirements
```bash
python3 quick_test.py
```

## 📊 Performance Tips

- Use "tiny" Whisper model for faster voice recognition
- Use "mistral" for fastest AI responses
- Close other apps to free RAM
- Monitor CPU/RAM usage in left sidebar

## 🆘 Troubleshooting

**App won't start**
```bash
python3 quick_test.py        # Check what's missing
brew install python-tk@3.14  # Install tkinter if needed
```

**No AI responses**
```bash
ollama serve                 # Start Ollama in separate terminal
ollama pull neural-chat      # Pull a model
```

**Voice not working**
```bash
pip install faster-whisper   # Install voice support
pip install pyaudio          # Install audio handling
ffmpeg -version              # Check FFmpeg installed
```

**App crashes**
Check `memory.json` isn't corrupted:
```bash
rm memory.json               # Delete corrupted file
python3 main.py              # Restart - will recreate
```

## 📚 File Locations

```
/Users/admin/Documents/AIAIAI/EVE/
├── main.py           ← Main application
├── style_config.json ← Theme settings (edit this!)
├── memory.json       ← User data (auto-saved)
└── utils/            ← Helper modules
```

## 🔗 Important URLs

- **Ollama**: https://ollama.ai (download & models)
- **Python**: https://www.python.org (download)
- **CustomTkinter**: GitHub repo with examples

## 📞 Support

1. Check `DEPLOYMENT_GUIDE.txt` for detailed setup
2. Check `README.md` for full features list
3. Check inline code comments for implementation details
4. Review `style_config.json` for all customizable options

## ✅ Preflight Checklist

Before launching:
- [ ] Python 3.8+ installed
- [ ] Tkinter installed (`brew install python-tk@3.14`)
- [ ] Virtual environment created (`source venv/bin/activate`)
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] (Optional) Ollama installed and running (`ollama serve`)
- [ ] (Optional) Faster-Whisper installed (`pip install faster-whisper`)

## 🎯 First Time Setup

1. **Activate environment**: `source venv/bin/activate`
2. **Start Ollama** (optional): `ollama serve` in new terminal
3. **Launch app**: `python3 main.py`
4. **Set your name**: Type in bottom left, click SET
5. **Test AI**: Type a message and press Enter (if Ollama running)
6. **Test voice** (optional): Click 🎤 and speak (if Faster-Whisper installed)

## 💡 Pro Tips

- Conversations auto-save to `memory.json`
- Notes are always editable in right sidebar
- System stats update every 2 seconds
- Voice auto-sends after transcription
- Colors update instantly if you edit config
- All processing is local (no cloud!)

## 🎨 Example Custom Color Scheme

For a more "classic cyberpunk" feel:

```json
"colors": {
  "background": "#000000",
  "secondary_bg": "#0a0a0a", 
  "accent_cyan": "#00ffff",
  "accent_orange": "#ff6600",
  "warning": "#ff0000",
  "success": "#00ff00"
}
```

Edit `style_config.json` and restart!

---

**Version**: 1.0  
**Status**: Production Ready ✓  
**Last Updated**: March 21, 2026  
**Quick ref**: CTRL+K, type "EVE" for instant help!
