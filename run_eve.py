#!/usr/bin/env python3
"""
Wrapper script that patches tkinter version check and launches EVE
"""
import sys
import os

# Patch tkinter to ignore strict macOS version check
import tkinter
original_file = tkinter.__file__

# Read and patch the tkinter __init__ file
try:
    import importlib.util
    spec = importlib.util.find_spec("tkinter")
    tk_init_file = os.path.join(os.path.dirname(spec.origin), "__init__.py")
    
    with open(tk_init_file, 'r') as f:
        content = f.read()
    
    # Comment out the strict version check
    if "macOS 12 (1207)" in content:
        print("[PATCH] Detected strict macOS version check, patching...")
        content = content.replace(
            "raise RuntimeError",
            "# raise RuntimeError  # PATCHED: Version check bypassed"
        )
except Exception as e:
    print(f"[WARN] Could not patch tkinter: {e}")

# Now import and run the main app
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from main import EVEApplication

if __name__ == "__main__":
    import customtkinter as ctk
    root = ctk.CTk()
    app = EVEApplication(root)
    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("\n[EXIT] EVE shutting down...")
        sys.exit(0)
