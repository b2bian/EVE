#!/bin/bash
# EVE - Cyberpunk AI Assistant Launcher
# Quick-start script for running EVE CLI

cd "$(dirname "$0")"

# Colors for output
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${CYAN}"
echo "╔════════════════════════════════════════════╗"
echo "║  EVE - Cyberpunk AI Desktop Assistant    ║"
echo "║         CLI Interface (Terminal)          ║"
echo "╚════════════════════════════════════════════╝"
echo -e "${NC}"

# Activate virtual environment
if [ ! -d ".venv_system" ]; then
    echo "⚠️  Virtual environment not found. Creating..."
    python3 -m venv .venv_system
    . .venv_system/bin/activate
    pip install -q customtkinter psutil requests python-dotenv colored pillow
else
    . .venv_system/bin/activate
fi

echo "🚀 Launching EVE CLI Interface..."
echo ""

# Run the CLI
python3 eve_cli_interface.py

echo ""
echo "👋 EVE shutting down. Goodbye!"
