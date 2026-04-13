@echo off
title TraceGuard - Forensic Metadata Tool
color 0A
echo ============================================================
echo    TRACEGUARD - FORENSIC METADATA TOOL
echo ============================================================
echo.
echo Starting TraceGuard...
echo.
python main.py
if errorlevel 1 (
    echo.
    echo [ERROR] Failed to start. Please check dependencies.
    echo Run: pip install Pillow
    echo.
    pause
)
