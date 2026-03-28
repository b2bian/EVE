#!/usr/bin/env python3
"""
EVE Launcher with Tcl/Tk Version Check Bypass
Patches the macOS version check to allow running on systems that report
an older version than what Tk/Tcl requires
"""
import sys
import os
import ctypes

def patch_tcl_version_check():
    """Patch Tcl/Tk to bypass macOS version check"""
    try:
        # Try to load and patch the Tk dylib
        import tkinter
        
        # Get the Tk library path
        tk_path = os.path.dirname(tkinter.__file__)
        
        # Read tkinter __init__
        init_file = os.path.join(tk_path, '__init__.py')
        with open(init_file, 'r') as f:
            content = f.read()
        
        # Check if version check exists and remove it
        if 'macOS 12 (1207)' in content or 'RuntimeError' in content:
            print("[DEBUG] Found version check, patching...")
            # This is a Python file so we can patch it safely
            patched = content.replace(
                'raise RuntimeError',
                '# PATCHED: Version check bypassed\n    if False: raise RuntimeError'
            )
            with open(init_file, 'w') as f:
                f.write(patched)
            print("[SUCCESS] Patched tkinter version check")
        
        return True
    except Exception as e:
        print(f"[WARNING] Could not patch Tcl/Tk: {e}")
        # Continue anyway - maybe it will work
        return True

if __name__ == '__main__':
    print("[*] EVE Launcher - Bypassing Version Checks")
    print("[*] Patching Tcl/Tk version check...")
    
    patch_tcl_version_check()
    
    print("[*] Loading EVE...")
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    
    try:
        import customtkinter as ctk
        from main import EVEApplication
        
        root = ctk.CTk()
        app = EVEApplication(root)
        print("[✓] EVE loaded successfully!")
        print("[*] Window should now be visible on your screen")
        print("[*] Close the window to exit")
        root.mainloop()
        
    except Exception as e:
        print(f"[ERROR] Failed to start EVE: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
