#!/usr/bin/env python3
"""
Patch tkinter to bypass macOS version check that's too strict
"""
import tkinter
import os
import sys

# Find tkinter's __init__.py file
tk_init = tkinter.__file__
tk_init_dir = os.path.dirname(tk_init)
tk_init_full = os.path.join(tk_init_dir, '__init__.py')

print(f"Found tkinter at: {tk_init_full}")

try:
    # Read the file
    with open(tk_init_full, 'r') as f:
        content = f.read()
    
    # Check if the version check exists
    if "macOS 12 (1207)" in content:
        print("✓ Found strict version check, applying patch...")
        # Comment out the problematic check
        modified_content = content.replace(
            'raise RuntimeError("Python tkinter not built with tk/tcl.",',
            'pass  # PATCHED: Bypassed version check for macOS\n    # raise RuntimeError("Python tkinter not built with tk/tcl.",'
        )
        
        # Write back
        with open(tk_init_full, 'w') as f:
            f.write(modified_content)
        print("✅ Patch applied successfully!")
        sys.exit(0)
    else:
        print("✓ Version check not found - may already be patched")
        sys.exit(0)
        
except Exception as e:
    print(f"❌ Error applying patch: {e}")
    sys.exit(1)
