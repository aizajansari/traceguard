#!/bin/bash
# TraceGuard Launcher for TailsOS
cd "$(dirname "$0")"

echo "=================================="
echo "  TRACEGUARD - FORENSIC TOOL"
echo "=================================="
echo ""

if python3 -c "import tkinter" 2>/dev/null; then
    echo "Starting GUI mode..."
    python3 main.py
else
    echo "Starting CLI mode..."
    python3 cli.py
fi