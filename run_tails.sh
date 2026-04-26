#!/bin/bash
cd "$(dirname "$0")"

echo "=================================="
echo "  TRACEGUARD - FORENSIC TOOL"
echo "=================================="
echo ""

if command -v exiftool &>/dev/null; then
    echo "✅ exiftool available - Full forensic mode"
else
    echo "⚠️ exiftool not found - Installing..."
    sudo apt-get update
    sudo apt-get install exiftool -y
fi

echo ""
python3 main.py