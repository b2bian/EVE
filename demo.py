#!/usr/bin/env python3
"""
EVE Terminal Demo - Test PersonalBrain without GUI
Perfect for testing while tkinter installs
"""

import sys
import os
from pathlib import Path

# Add utils to path
sys.path.insert(0, str(Path(__file__).parent))

from utils.personal_brain import PersonalBrain, create_brain
from utils.memory import MemoryManager
from utils.ollama_handler import OllamaHandler
from utils.theme_loader import ThemeLoader

def print_header(text):
    """Print a styled header."""
    print(f"\n{'='*70}")
    print(f"  {text}")
    print(f"{'='*70}")

def print_section(text):
    """Print a section header."""
    print(f"\n📌 {text}\n")

def main():
    """Run terminal demo of EVE with PersonalBrain."""
    
    print_header("🧠 EVE PersonalBrain - Terminal Demo")
    
    # Initialize PersonalBrain
    print("\n⏳ Initializing PersonalBrain...")
    brain = create_brain()
    brain.log_session()
    
    # Display greeting
    greeting = brain.get_greeting()
    print(f"\n✨ EVE says: \"{greeting}\"")
    
    # Show profile
    print_section("Your Brain Profile")
    summary = brain.get_memory_summary()
    print(f"  Name: {summary['name']}")
    print(f"  Sessions: {summary['sessions']}")
    print(f"  Projects: {summary['projects']}")
    print(f"  Learnings: {summary['learnings']}")
    print(f"  Profile Completeness: {summary['profile_completeness']}%")
    
    # Show interests
    print_section("Your Interests")
    for interest, active in brain.interests.items():
        status = "✓" if active else "✗"
        print(f"  [{status}] {interest.replace('_', ' ').title()}")
    
    # Check Ollama
    print_section("System Status")
    theme = ThemeLoader("style_config.json")
    config = theme.get_config()
    ollama = OllamaHandler(config)
    
    if ollama.check_connection():
        models = ollama.get_available_models()
        print(f"  ✅ Ollama: ONLINE")
        print(f"  📦 Model: {ollama.model}")
        print(f"  🎯 Available models: {', '.join(models[:3])}")
    else:
        print(f"  ⚠️  Ollama: OFFLINE")
        print(f"  💡 To enable AI: run 'ollama serve' in another terminal")
    
    # Memory manager
    memory = MemoryManager("memory.json")
    print(f"  📚 Memory: Initialized ({len(memory.get_conversation_history())} messages)")
    
    # Interactive demo
    print_header("🎮 Interactive Demo")
    print("\nYou can now:")
    print("  1. Ask EVE questions (Ollama must be running)")
    print("  2. Store projects and learnings")
    print("  3. Switch personalities")
    print("\n💡 Type 'help' for available commands, 'exit' to quit\n")
    
    while True:
        try:
            command = input("EVE> ").strip().lower()
            
            if command == "exit":
                print("\n👋 Goodbye! EVE will be waiting when you launch the full GUI.\n")
                break
            
            elif command == "help":
                print_section("Available Commands")
                print("  profile      - Show your brain profile")
                print("  summary      - Quick summary of what EVE knows")
                print("  store-project - Save a project EVE helped with")
                print("  store-learning - Save a lesson you learned")
                print("  context      - See the context EVE uses for responses")
                print("  personality  - See your 6 personalities")
                print("  session      - Check session info")
                print("  exit         - Close this demo")
                print("  help         - Show this help menu")
            
            elif command == "profile":
                print_section("Your Profile")
                summary = brain.get_memory_summary()
                for key, value in summary.items():
                    print(f"  {key.replace('_', ' ').title()}: {value}")
            
            elif command == "summary":
                summary = brain.get_memory_summary()
                print(f"\n🧠 EVE knows {summary['profile_completeness']}% about you")
                print(f"   - You've had {summary['sessions']} session(s)")
                print(f"   - You've shared {summary['projects']} project(s)")
                print(f"   - EVE learned {summary['learnings']} thing(s) about you")
            
            elif command == "store-project":
                name = input("  Project name: ").strip()
                desc = input("  Description: ").strip()
                lang = input("  Language/Type (optional): ").strip() or None
                brain.store_project(name, desc, language=lang, tags=["demo"])
                print(f"  ✅ Stored: {name}")
            
            elif command == "store-learning":
                topic = input("  Topic: ").strip()
                insight = input("  What did you learn: ").strip()
                brain.store_learning(topic, insight, context="Terminal Demo")
                print(f"  ✅ Learned: {topic}")
            
            elif command == "context":
                print_section("EVE's Context for Responses")
                context = brain.build_context_prompt()
                print(context)
            
            elif command == "personality":
                print_section("Your 6 Personalities")
                from utils.system_prompts import PERSONALITY_DESCRIPTIONS
                for i, (name, desc) in enumerate(PERSONALITY_DESCRIPTIONS.items(), 1):
                    print(f"  {i}. {name.title()}: {desc}")
            
            elif command == "session":
                print_section("Session Information")
                print(f"  Current sessions: {brain.user_data.get('num_sessions', 0)}")
                print(f"  Last session: {brain.user_data.get('last_session', 'Never')}")
                print(f"  Created: {brain.user_data.get('created_date', 'Unknown')}")
            
            elif command.startswith("ask "):
                # Simple chat (requires Ollama)
                question = command[4:].strip()
                if not ollama.check_connection():
                    print("\n  ⚠️  Ollama is not running!")
                    print("  💡 In another terminal, run: ollama serve")
                else:
                    print(f"\n  💭 Thinking...")
                    system_prompt = brain.get_system_prompt_for_personality("quirky")
                    full_prompt = f"{system_prompt}\n\nUser: {question}\n\nEVE:"
                    try:
                        response = ollama.generate(full_prompt, stream=False)
                        print(f"\n  EVE: {response.strip()}\n")
                    except Exception as e:
                        print(f"  ❌ Error: {e}")
            
            elif command:
                print("  ❓ Unknown command. Type 'help' for available commands.")
        
        except KeyboardInterrupt:
            print("\n\n👋 Demo ended. Your brain is saved!")
            break
        except Exception as e:
            print(f"  ❌ Error: {e}")

if __name__ == "__main__":
    main()
