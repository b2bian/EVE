#!/usr/bin/env python3
"""
Simple local test of EVE application modules
Tests imports and basic functionality without GUI
"""

import os
import sys
import json

# Add utils to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=" * 60)
print("EVE - Application Module Test")
print("=" * 60)

# Test 1: Theme Loader
print("\n[1/5] Testing ThemeLoader...")
try:
    from utils.theme_loader import ThemeLoader
    theme = ThemeLoader("style_config.json")
    print(f"  ✓ Config loaded")
    print(f"  ✓ Background color: {theme.get_color('background')}")
    print(f"  ✓ Accent cyan: {theme.get_color('accent_cyan')}")
    print(f"  ✓ Appearance mode: {theme.get_appearance_mode()}")
except Exception as e:
    print(f"  ✗ Error: {e}")
    sys.exit(1)

# Test 2: Memory Manager
print("\n[2/5] Testing MemoryManager...")
try:
    from utils.memory import MemoryManager
    memory = MemoryManager("test_memory.json")
    print(f"  ✓ Memory initialized")
    print(f"  ✓ User name: {memory.get_user_name()}")
    
    # Test adding conversation
    memory.add_conversation("user", "Test message")
    print(f"  ✓ Conversation saved")
    
    # Clean up
    memory.set_user_name("Guest")
    memory.save()
    print(f"  ✓ Settings updated")
except Exception as e:
    print(f"  ✗ Error: {e}")
    sys.exit(1)

# Test 3: System Monitor
print("\n[3/5] Testing SystemMonitor...")
try:
    from utils.system_monitor import SystemMonitor
    monitor = SystemMonitor(update_interval=100)
    print(f"  ✓ Monitor initialized")
    print(f"  ✓ Current CPU: {monitor.get_cpu_percent():.1f}%")
    print(f"  ✓ Current RAM: {monitor.get_memory_percent():.1f}%")
    print(f"  ✓ Status: {monitor.get_status_string()}")
except Exception as e:
    print(f"  ✗ Error: {e}")
    sys.exit(1)

# Test 4: Ollama Handler
print("\n[4/5] Testing OllamaHandler...")
try:
    from utils.ollama_handler import OllamaHandler
    config = json.load(open("style_config.json"))
    ollama = OllamaHandler(config)
    
    if ollama.is_connected:
        print(f"  ✓ Connected to Ollama")
        models = ollama.get_available_models()
        print(f"  ✓ Available models: {models}")
    else:
        print(f"  ⚠ Ollama not running (this is optional)")
        print(f"    Start with: ollama serve")
    
    print(f"  ✓ Default model: {ollama.model}")
except Exception as e:
    print(f"  ✗ Error: {e}")
    sys.exit(1)

# Test 5: Voice Handler
print("\n[5/5] Testing VoiceHandler...")
try:
    from utils.voice import VoiceHandler
    config = json.load(open("style_config.json"))
    voice = VoiceHandler(config)
    
    if voice.is_model_loaded():
        print(f"  ✓ Voice model loaded")
    else:
        print(f"  ⚠ Voice model not loaded (optional feature)")
        print(f"    To enable: pip install faster-whisper")
    
    print(f"  ✓ Voice handler initialized")
except Exception as e:
    print(f"  ✗ Error: {e}")
    sys.exit(1)

# Summary
print("\n" + "=" * 60)
print("✓ All modules tested successfully!")
print("=" * 60)

print("\nNext steps:")
print("  1. Install tkinter if needed:")
print("     macOS: brew install python-tk@3.14")
print("     Linux: sudo apt-get install python3-tk")
print("")
print("  2. Start Ollama for AI features (optional):")
print("     ollama serve")
print("")
print("  3. Launch the application:")
print("     python3 main.py")
print("     Or use: ./run.sh")
print ("=" * 60)

# Clean up test file
if os.path.exists("test_memory.json"):
    os.remove("test_memory.json")
