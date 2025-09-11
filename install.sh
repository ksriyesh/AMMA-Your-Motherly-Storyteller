#!/bin/bash
# AMMA Installation Script for Linux/macOS

echo "🌙 AMMA - Bedtime Story Agent Installer 🌙"
echo

# Make sure we can run Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.11+ first."
    exit 1
fi

# Run the Python installer
python3 install.py
