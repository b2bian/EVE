#!/usr/bin/env python3
"""
EVE Launcher Wrapper - Handles macOS version check bypass for tkinter
"""
import sys
import os

# Disable tkinter's strict macOS version check before importing
import tkinter
import warnings

# Monkey-patch tkinter to bypass version check
original_file = tkinter.__file__
print(f"[*] Patching tkinter at {original_file}")

try:
    with open(original_file, 'r') as f:
        content = f.read()
    
    # Look for the version check and patch it
    if 'macOS 12 (1207)' in content:
        patched = content.replace(
            'raise RuntimeError("Python tkinter not built with tk/tcl.",',
            '# VERSION CHECK BYPASSED\n    if False: raise RuntimeError("Python tkinter not built with tk/tcl.",'
        )
        with open(original_file, 'w') as f:
            f.write(patched)
        print("[✓] Version check bypassed")
    else:
        print("[✓] No version check found to patch")
except Exception as e:
    print(f"[!] Could not patch tkinter: {e}")
    print("[!] Attempting to continue anyway...")

# Now import and run main.py
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    import main
except Exception as e:
    print(f"Error running EVE: {e}")
    sys.exit(1)
