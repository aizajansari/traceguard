#!/bin/bash
# TraceGuard Launcher for TailsOS
cd "$(dirname "$0")"

echo "=================================="
echo "  TRACEGUARD - FORENSIC TOOL"
echo "=================================="
echo ""

# First run installer to ensure dependencies
if [ ! -f "reports/.installed" ]; then
    echo "First time setup. Installing dependencies..."
    python3 install_traceguard.py
    touch reports/.installed
fi

if python3 -c "import tkinter" 2>/dev/null; then
    echo "Starting GUI mode..."
    python3 main.py
else
    echo "Starting CLI mode..."
    python3 cli.py
fi
