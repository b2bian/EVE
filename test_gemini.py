#!/usr/bin/env python3
"""Quick test script to verify Gemini API is working"""

import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Test 1: Check API key is loaded
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    print("✓ API Key loaded from .env")
    print(f"  Key starts with: {api_key[:20]}...")
else:
    print("✗ API Key NOT found in .env")
    exit(1)

# Test 2: Try importing and configuring Gemini
try:
    import google.generativeai as genai
    print("✓ google-generativeai imported successfully")
    
    genai.configure(api_key=api_key)
    print("✓ Gemini API configured successfully")
    
    # Test 3: Try a simple API call
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content("Say 'Hello from Gemini!' in one sentence only.")
    
    if response.text:
        print("✓ Gemini API responding correctly")
        print(f"\n  Response: {response.text}\n")
    else:
        print("✗ No response from Gemini API")
        exit(1)
        
except Exception as e:
    print(f"✗ Error: {e}")
    exit(1)

print("=" * 60)
print("SUCCESS! Gemini API is working correctly.")
print("=" * 60)
