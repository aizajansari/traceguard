#!/bin/bash

# TraceGuard Installation Script for Linux/Mac/TailsOS

echo "============================================================"
echo "   🛡️  TRACEGUARD - INSTALLATION"
echo "============================================================"
echo ""

# Detect OS
if [ -f /etc/os-release ]; then
    . /etc/os-release
    echo "📡 OS: $NAME $VERSION"
else
    echo "📡 OS: $(uname -s)"
fi

# Check Python
if command -v python3 &>/dev/null; then
    PYTHON_CMD="python3"
elif command -v python &>/dev/null; then
    PYTHON_CMD="python"
else
    echo "❌ Python not found. Please install Python 3.8+"
    exit 1
fi

echo "🐍 Python: $($PYTHON_CMD --version)"

# Install Pillow
echo ""
echo "📦 Installing Python dependencies..."
$PYTHON_CMD -m pip install Pillow

# Create directories
echo ""
echo "📁 Creating directories..."
mkdir -p reports logs
echo "   ✅ reports/"
echo "   ✅ logs/"

# Install exiftool based on OS
echo ""
echo "🔧 Installing exiftool..."

if command -v apt-get &>/dev/null; then
    # Debian/Ubuntu
    sudo apt-get update
    sudo apt-get install exiftool -y
elif command -v brew &>/dev/null; then
    # macOS
    brew install exiftool
elif command -v pacman &>/dev/null; then
    # Arch Linux
    sudo pacman -S perl-image-exiftool
else
    echo "⚠️ Could not install exiftool automatically"
    echo "   Please download from: https://exiftool.org/"
fi

# Make scripts executable
chmod +x run.sh

echo ""
echo "============================================================"
echo "✅ INSTALLATION COMPLETE!"
echo ""
echo "📌 To run TraceGuard:"
echo "   ./run.sh"
echo "   OR: $PYTHON_CMD main.py"
echo "============================================================"