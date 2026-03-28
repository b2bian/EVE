#!/usr/bin/env python3
"""
Quick test script to verify EVE application setup.
"""

import os
import sys
import json

def test_config_files():
    """Test if configuration files exist."""
    print("📋 Checking configuration files...")
    
    files_to_check = [
        "style_config.json",
        "requirements.txt",
        "main.py",
        "utils/memory.py",
        "utils/voice.py",
        "utils/system_monitor.py",
        "utils/ollama_handler.py",
        "utils/theme_loader.py",
    ]
    
    all_exist = True
    for filepath in files_to_check:
        if os.path.exists(filepath):
            print(f"  ✓ {filepath}")
        else:
            print(f"  ✗ {filepath} - MISSING")
            all_exist = False
    
    return all_exist

def test_imports():
    """Test if core modules can be imported."""
    print("\n🔍 Testing imports...")
    
    modules = [
        ("customtkinter", "UI Framework"),
        ("psutil", "System Monitoring"),
        ("requests", "HTTP Client"),
        ("json", "JSON Processing"),
    ]
    
    all_ok = True
    for module_name, description in modules:
        try:
            __import__(module_name)
            print(f"  ✓ {module_name} ({description})")
        except ImportError:
            print(f"  ✗ {module_name} ({description}) - MISSING")
            all_ok = False
    
    return all_ok

def test_config_valid():
    """Test if style_config.json is valid JSON."""
    print("\n⚙️  Validating configuration...")
    
    try:
        with open("style_config.json", "r") as f:
            config = json.load(f)
        
        required_keys = ["theme", "ui", "layout", "voice", "persona", "ollama"]
        missing = [key for key in required_keys if key not in config]
        
        if missing:
            print(f"  ✗ Missing config sections: {missing}")
            return False
        
        print("  ✓ style_config.json is valid")
        return True
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"  ✗ Config error: {e}")
        return False

def test_utils_import():
    """Test if utils modules can be imported."""
    print("\n📦 Testing utility modules...")
    
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    
    modules = [
        ("utils.theme_loader", "Theme Loader"),
        ("utils.memory", "Memory Manager"),
        ("utils.system_monitor", "System Monitor"),
        ("utils.ollama_handler", "Ollama Handler"),
        ("utils.voice", "Voice Handler"),
    ]
    
    all_ok = True
    for module_name, description in modules:
        try:
            __import__(module_name)
            print(f"  ✓ {module_name} ({description})")
        except ImportError as e:
            print(f"  ✗ {module_name} ({description}): {e}")
            all_ok = False
    
    return all_ok

def check_ollama():
    """Check if Ollama is running."""
    print("\n🧠 Checking Ollama connection...")
    
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=2)
        if response.status_code == 200:
            data = response.json()
            models = [m["name"] for m in data.get("models", [])]
            print(f"  ✓ Ollama is running")
            if models:
                print(f"  ✓ Available models: {', '.join(models[:3])}")
            else:
                print(f"  ⚠️  No models installed. Run: ollama pull neural-chat")
            return True
        else:
            print(f"  ✗ Ollama responded with status {response.status_code}")
            return False
    except Exception as e:
        print(f"  ⚠️  Ollama not running: {e}")
        print(f"     Start with: ollama serve")
        return False

def main():
    """Run all tests."""
    print("=" * 50)
    print("EVE - Cyberpunk AI Assistant Setup Verification")
    print("=" * 50)
    
    results = {
        "Config files": test_config_files(),
        "Imports": test_imports(),
        "Configuration": test_config_valid(),
        "Utils modules": test_utils_import(),
    }
    
    check_ollama()
    
    print("\n" + "=" * 50)
    print("Test Summary:")
    print("=" * 50)
    
    all_passed = all(results.values())
    
    for test_name, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"  {status}: {test_name}")
    
    print("=" * 50)
    
    if all_passed:
        print("\n✨ All tests passed! Ready to launch EVE.")
        print("\nTo start the application:")
        print("  ./run.sh")
        print("\nOr manually:")
        print("  source venv/bin/activate")
        print("  python3 main.py")
        return 0
    else:
        print("\n❌ Some tests failed. Please fix the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
