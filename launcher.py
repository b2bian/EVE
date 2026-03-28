#!/usr/bin/env python3
"""
EVE Launcher - PersonalBrain Edition
Handles dependencies and launches EVE with grace
"""

import sys
import subprocess
import os
from pathlib import Path

def check_tkinter():
    """Check if tkinter is available."""
    try:
        import tkinter
        return True
    except ImportError:
        return False

def check_personalbrain():
    """Check if PersonalBrain module is available."""
    try:
        from utils.personal_brain import PersonalBrain
        return True
    except ImportError:
        return False

def print_banner():
    """Display welcome banner."""
    print("\n" + "="*70)
    print("🚀 EVE - AI Desktop Assistant with PersonalBrain")
    print("="*70)

def check_dependencies():
    """Check and report on all dependencies."""
    print("\n📋 Checking dependencies...\n")
    
    checks = {
        "PersonalBrain System": check_personalbrain(),
        "Tkinter GUI Framework": check_tkinter(),
    }
    
    all_good = True
    for dep, available in checks.items():
        status = "✅" if available else "❌"
        print(f"  {status} {dep}")
        if not available:
            all_good = False
    
    return all_good

def launch_eve():
    """Launch EVE application."""
    print("\n🎮 Launching EVE...\n")
    
    try:
        # Import and run main app
        from main import EVEApplication
        import customtkinter as ctk
        
        root = ctk.CTk()
        app = EVEApplication(root)
        root.mainloop()
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("\n💡 Troubleshooting:")
        print("   1. Ensure you're in the EVE directory")
        print("   2. Run: source venv/bin/activate")
        print("   3. Try: python3 launcher.py")
        return False
    except Exception as e:
        print(f"❌ Runtime Error: {e}")
        return False
    
    return True

def install_tkinter_prompt():
    """Prompt user about tkinter installation."""
    print("\n⚠️  IMPORTANT: Tkinter is required for the GUI")
    print("\n📦 To install tkinter, run in Terminal:")
    print("   brew install python-tk@3.14")
    print("\n⏳ This may take 5-15 minutes depending on your system.")
    print("\n🔄 After installation completes:")
    print("   1. Close and reopen Terminal")
    print("   2. Run this launcher again")
    
    response = input("\n❓ Would you like to install tkinter now? (y/n): ").strip().lower()
    if response == 'y':
        print("\n⌚ Installing tkinter via brew (this runs in background)...")
        print("   This will take a while. You can switch to Terminal to monitor.")
        subprocess.Popen(["brew", "install", "python-tk@3.14"])
        return False
    
    return False

def main():
    """Main launcher logic."""
    os.chdir(Path(__file__).parent)
    
    print_banner()
    
    if not check_dependencies():
        print("\n" + "="*70)
        print("❌ MISSING DEPENDENCIES DETECTED")
        print("="*70)
        
        if not check_tkinter():
            install_tkinter_prompt()
        
        return 1
    
    print("\n" + "="*70)
    print("✅ All dependencies ready!")
    print("="*70)
    
    success = launch_eve()
    
    if not success:
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
