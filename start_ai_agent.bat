@echo off
echo AI Agent - 電話営業ボット
echo ==========================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not in PATH.
    echo Please install Python 3.7+ from https://python.org
    pause
    exit /b 1
)

REM Check if requirements are installed
echo Checking dependencies...
python -c "import pyttsx3, speech_recognition, tkinter" >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
    
    REM Install PyAudio separately for Windows
    echo Installing PyAudio for Windows...
    pip install pipwin
    pipwin install pyaudio
    
    if errorlevel 1 (
        echo Failed to install some dependencies.
        echo Please try manual installation:
        echo pip install pipwin
        echo pipwin install pyaudio
        pause
        exit /b 1
    )
)

REM Run the application
echo Starting AI Agent...
python main.py

pause
