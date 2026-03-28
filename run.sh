#!/bin/bash

# EVE - Cyberpunk AI Desktop Assistant
# Startup script for easy launching

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    pip install customtkinter psutil requests python-dotenv colored -q
else
    source venv/bin/activate
fi

# Check if Ollama is running
echo "Checking Ollama connection..."
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "⚠️  Warning: Ollama is not running!"
    echo "To enable AI features, start Ollama in another terminal:"
    echo "  ollama serve"
    echo ""
    read -p "Continue without Ollama? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Aborted."
        exit 1
    fi
fi

echo "🚀 Starting EVE..."
python3 main.py
