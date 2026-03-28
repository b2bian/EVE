#!/usr/bin/env python3
import tkinter
import os
import sys

tk_file = os.path.join(os.path.dirname(tkinter.__file__), '__init__.py')
print(f"Patching: {tk_file}")

with open(tk_file, 'r') as f:
    content = f.read()

if 'macOS 12' in content:
    # Simple approach: comment out the raise RuntimeError line
    patched = content.replace(
        'raise RuntimeError("macOS 12 (1207) or later required, have instead {0} ({1}) !".format(major_version, minor_version))',
        '# Patched: version check removed\npass'
    )
    
    with open(tk_file, 'w') as f:
        f.write(patched)
    print('✅ Successfully patched tkinter!')
else:
    print('ℹ️  No macOS version check found to patch')
