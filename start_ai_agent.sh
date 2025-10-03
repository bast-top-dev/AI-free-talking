#!/bin/bash

echo "AI Agent - 電話営業ボット"
echo "=========================="
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed or not in PATH."
    echo "Please install Python 3.7+ from your package manager or https://python.org"
    exit 1
fi

# Check if requirements are installed
echo "Checking dependencies..."
python3 -c "import pyttsx3, speech_recognition, tkinter" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Installing dependencies..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "Failed to install dependencies."
        exit 1
    fi
fi

# Run the application
echo "Starting AI Agent..."
python3 main.py
