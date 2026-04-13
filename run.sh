#!/bin/bash
echo "============================================================"
echo "   TRACEGUARD - FORENSIC METADATA TOOL"
echo "============================================================"
echo ""
echo "Starting TraceGuard..."
echo ""
if command -v python3 &>/dev/null; then
    python3 main.py
elif command -v python &>/dev/null; then
    python main.py
else
    echo "[ERROR] Python not found"
    exit 1
fi
echo ""
echo "TraceGuard closed."
