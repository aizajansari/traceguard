# 🛡️ TraceGuard - Forensic Metadata Tool

**Advanced Cross-Platform Forensic Metadata Scanner and Cleaner**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS%20%7C%20TailsOS-green.svg)](https://tails.net)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🔍 Overview

TraceGuard is a professional forensic metadata analysis tool that works on **ALL operating systems** including Windows, Linux, macOS, and **TailsOS**.

### What it does:
- 🔍 **Extracts EVERY hidden metadata** from images (GPS, camera, dates, software)
- 🧹 **Completely removes ALL traces** of metadata
- 🔒 **Anonymizes files** with random names
- 🗑️ **Securely deletes originals** (3x overwrite - unrecoverable)
- 📦 **Batch processes** entire folders

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🔍 **Forensic Scanner** | Extracts ALL metadata (GPS, camera, EXIF, IPTC, XMP) |
| 🧹 **Forensic Cleaner** | Removes EVERY trace of metadata |
| 🔒 **Privacy Options** | Anonymize filename, secure delete, modify timestamps, recompress |
| 📦 **Batch Processor** | Clean multiple files with random names |
| 📄 **Report Generator** | HTML/JSON professional reports |
| 💻 **Cross-Platform** | Windows, Linux, macOS, TailsOS |

## 🚀 Quick Start

# TraceGuard - Forensic Metadata Tool

## One-Click Install

### Windows:
1. Download `install_traceguard.py`
2. Double-click it
3. Follow instructions

### Linux / Mac / TailsOS:
```bash
python3 install_traceguard.py

###EXTRA###
Step 1: Enable Persistent Storage (if not already)
bash
# When booting TailsOS:
1. Select "Tails" from boot menu
2. Select "More options" → "Configure Persistent Storage"
3. Set an administration password
4. Enable "Personal Files" and "Persistent Storage"
5. Click "Save" and restart Tails

Step 2: Download and Install TraceGuard
bash
# Start TailsOS with Persistent Storage unlocked
# Open Terminal (Applications → System Tools → Terminal)

# Navigate to Persistent storage
cd /home/amnesia/Persistent

# Download the installer (or copy from USB)
wget https://raw.githubusercontent.com/YOUR_USERNAME/traceguard/main/install_traceguard.py

# Or if you have the file on USB:
# cp /media/amnesia/USB/install_traceguard.py .

# Run the installer

python3 install_traceguard.py
Step 3: Run TraceGuard on TailsOS
bash
# After installation, run:
cd /home/amnesia/Persistent/traceguard
./run.sh
# OR
python3 main.py

Step 4: Save Results Persistently
bash
# When saving cleaned files or reports:
# ALWAYS save to: /home/amnesia/Persistent/
# Example output folder: /home/amnesia/Persistent/CleanedFiles/

# Reports are auto-saved to: /home/amnesia/Persistent/traceguard/reports/
Troubleshooting TailsOS
bash
# If you get "Permission denied":
chmod +x run.sh install.sh

# If pip fails:
python3 -m pip install --user Pillow

# If exiftool not found:
sudo apt-get update
sudo apt-get install exiftool -y

# To verify installation:
ls -la /home/amnesia/Persistent/traceguard/