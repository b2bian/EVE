#!/usr/bin/env python3
"""
EVE CLI Interface - Terminal-based version of EVE when GUI is unavailable
Provides full chat functionality without tkinter/Tcl dependency
"""

import sys
import os
import json
from datetime import datetime

# Add utils to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.memory import MemoryManager
from utils.ollama_handler import OllamaHandler
from utils.system_monitor import SystemMonitor
from utils.theme_loader import ThemeLoader

class EVE_CLI:
    def __init__(self):
        self.theme = ThemeLoader("style_config.json")
        self.memory = MemoryManager("memory.json")
        self.ollama = OllamaHandler(self.theme.get_config())
        self.monitor = SystemMonitor()
        self.running = True
        
        print("\n" + "="*60)
        print("  EVE - Cyberpunk AI Assistant (CLI Mode)")
        print("="*60)
        print("\nℹ️  GUI unavailable due to tkinter version conflict on macOS")
        print("📝 Using terminal interface instead\n")
        
        # Check Ollama status
        if self.ollama.check_connection():
            print("✅ Ollama connected - AI features available")
        else:
            print("⚠️  Ollama not running - start with: ollama serve")
        
        print("\n" + "-"*60)
    
    def show_status(self):
        """Display system status"""
        print(f"\n📊 System Status:")
        print(f"   CPU: {self.monitor.cpu_percent:.1f}%")
        print(f"   RAM: {self.monitor.memory_percent:.1f}%")
    
    def chat(self):
        """Main chat loop"""
        user_name = self.memory.get_user_name() or "User"
        
        while self.running:
            print(f"\n{user_name}> ", end="", flush=True)
            try:
                user_input = input().strip()
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                self.running = False
                break
            except EOFError:
                print("\n\n👋 Goodbye!")
                self.running = False
                break
            
            if not user_input:
                continue
            
            # Handle commands
            if user_input.lower() == "/status":
                self.show_status()
                continue
            elif user_input.lower() == "/exit":
                self.running = False
                break
            elif user_input.lower() == "/help":
                self.show_help()
                continue
            elif user_input.lower().startswith("/name "):
                name = user_input[6:].strip()
                self.memory.set_user_name(name)
                user_name = name
                print(f"✓ Name set to: {name}")
                continue
            
            # Send to Ollama/Gemini
            print(f"\n🤖 EVE: ", end="", flush=True)
            
            if self.ollama.check_connection():
                response = self.ollama.generate(user_input)
                print(response)
            else:
                print("(Ollama not connected - cannot generate response)")
                print("\nTo enable AI: ollama serve")
            
            # Save conversation
            self.memory.add_conversation(user_input, "EVE")
    
    def show_help(self):
        """Show available commands"""
        print("\n📋 Commands:")
        print("   /status  - Show system status")
        print("   /name    - Set your name")
        print("   /help    - Show this help")
        print("   /exit    - Exit EVE")
        print("\n   Type anything else to chat with EVE!")

if __name__ == "__main__":
    try:
        eve = EVE_CLI()
        eve.chat()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
