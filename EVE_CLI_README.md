# EVE CLI - Quick Start Guide

## 🚀 Getting Started

Since the GUI has a macOS Tcl/Tk version conflict, EVE is running in **terminal mode** with full functionality.

### Quick Start (1 command)

```bash
cd /Users/admin/Documents/AIAIAI/EVE && . .venv_system/bin/activate && python3 eve_cli_interface.py
```

Or use the launcher script:
```bash
bash /Users/admin/Documents/AIAIAI/EVE/launch_eve.sh
```

## 💬 Using EVE

Once EVE starts, you'll see:
```
============================================================
  EVE - Cyberpunk AI Assistant (CLI Mode)
============================================================

ℹ️  GUI unavailable due to tkinter version conflict on macOS
📝 Using terminal interface instead

User> 
```

### Commands

| Command | Description |
|---------|-------------|
| `/status` | Show CPU and RAM usage |
| `/name [name]` | Set your name (e.g., `/name John`) |
| `/help` | Show available commands |
| `/exit` | Exit EVE |
| Any text | Chat with EVE (requires Ollama) |

### Example Conversation

```
User> Hello EVE
🤖 EVE: Hi! I'm EVE, your cyberpunk AI assistant...

User> /status
📊 System Status:
   CPU: 15.3%
   RAM: 42.1%

User> /exit
👋 Goodbye!
```

## 🧠 Enable AI Responses (Optional)

To chat with an AI:

1. **Open a new terminal tab** and run:
```bash
ollama serve
```

2. **Pull a model** (first time only):
```bash
ollama pull neural-chat
```

3. **Start chatting** with EVE - responses will now include AI-generated replies!

## 🔧 Available Models

Popular models to try:
- `neural-chat` (recommended - fast & good)
- `mistral` (powerful)
- `llama2` (accurate)

Pull any with: `ollama pull [model-name]`

## 📝 Features

✅ **Memory System** - Conversations are saved automatically
✅ **System Monitoring** - Real-time CPU/RAM stats
✅ **User Profiles** - Save your name and preferences
✅ **Theme System** - Cyberpunk color scheme configured
✅ **AI Integration** - Works with Ollama or Gemini API

## ⚠️ GUI Not Available (Why?)

The GUI version uses Tkinter, which requires macOS 12.1207+. Your system reports 12.1206, causing a version mismatch. 

**Solution:** Use the CLI interface (fully functional) or wait for:
- macOS update
- Python version change
- Tkinter patch

## 🐛 Troubleshooting

**"No module named '_tkinter'"**
- This is expected - use CLI instead
- GUI would require system-level Tcl/Tk rebuild

**"Ollama not running"**
- Run: `ollama serve` in another terminal
- This is optional - EVE CLI works without it

**"Module not found" errors**
- Ensure virtual environment is activated: `. .venv_system/bin/activate`
- Reinstall deps: `pip install -r requirements.txt`

## 📊 Project Status

- ✅ Core AI functionality: WORKING
- ✅ Memory system: WORKING
- ✅ System monitoring: WORKING
- ✅ CLI interface: WORKING & TESTED
- ⚠️ GUI interface: Blocked by macOS tkinter version
- ✅ Ollama integration: Ready
- ✅ Gemini API: Fixed & Ready (with API key)

## 🎯 Next Steps

1. Start EVE CLI: `python3 eve_cli_interface.py`
2. Set your name: `/name Your Name`
3. Check status: `/status`
4. (Optional) Start Ollama for AI: `ollama serve`
5. Chat with EVE!

---

**Eve is ready to assist you. Type `/help` to see commands!**
