@echo off
echo AI Agent - PyAudio Fix for Windows
echo ==================================
echo.

echo This script will fix the PyAudio installation issue on Windows.
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not in PATH.
    echo Please install Python 3.7+ from https://python.org
    pause
    exit /b 1
)

echo Installing pipwin...
pip install pipwin

echo Installing PyAudio through pipwin...
pipwin install pyaudio

echo Installing other dependencies...
pip install pyttsx3 speech_recognition

echo.
echo Testing installation...
python -c "import pyttsx3, speech_recognition, pyaudio; print('Success! All dependencies installed.')" 2>nul
if errorlevel 1 (
    echo.
    echo Some dependencies may not be working correctly.
    echo Try running the application anyway: python main.py
) else (
    echo.
    echo ✓ All dependencies installed successfully!
    echo You can now run: python main.py
)

echo.
pause
