@echo off
echo AI Agent - PyAudio Installation for Python 3.13
echo ================================================
echo.

echo This script will install PyAudio using alternative methods for Python 3.13.
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not in PATH.
    echo Please install Python 3.7+ from https://python.org
    pause
    exit /b 1
)

echo Checking Python version...
python -c "import sys; print(f'Python {sys.version}')"

echo.
echo Installing core dependencies first...
pip install pyttsx3==2.90 SpeechRecognition>=3.14.0

echo.
echo Attempting PyAudio installation methods for Python 3.13...
echo.

echo Method 1: Trying direct pip install...
pip install pyaudio
if not errorlevel 1 (
    echo ✓ PyAudio installed successfully via pip!
    goto test_installation
)

echo.
echo Method 2: Trying with pre-compiled wheel...
pip install --only-binary=all pyaudio
if not errorlevel 1 (
    echo ✓ PyAudio installed successfully via binary wheel!
    goto test_installation
)

echo.
echo Method 3: Trying with no-cache-dir flag...
pip install --no-cache-dir pyaudio
if not errorlevel 1 (
    echo ✓ PyAudio installed successfully without cache!
    goto test_installation
)

echo.
echo Method 4: Installing from conda-forge (if available)...
pip install conda
conda install -c conda-forge pyaudio
if not errorlevel 1 (
    echo ✓ PyAudio installed successfully via conda-forge!
    goto test_installation
)

echo.
echo Method 5: Manual compilation (may require Visual Studio Build Tools)...
echo Installing build dependencies...
pip install wheel setuptools
pip install pyaudio --no-binary=pyaudio
if not errorlevel 1 (
    echo ✓ PyAudio compiled and installed successfully!
    goto test_installation
)

echo.
echo All automatic methods failed. Trying alternative approach...
echo Installing alternative audio libraries...
pip install sounddevice soundfile
echo.
echo Installing alternative speech recognition...
pip install vosk

:test_installation
echo.
echo Testing installation...
python -c "import pyttsx3; print('✓ pyttsx3 OK')" 2>nul
python -c "import speech_recognition; print('✓ speech_recognition OK')" 2>nul
python -c "import pyaudio; print('✓ PyAudio OK')" 2>nul
if errorlevel 1 (
    python -c "import sounddevice; print('✓ sounddevice (alternative) OK')" 2>nul
    if not errorlevel 1 (
        echo.
        echo PyAudio installation failed, but alternative audio libraries are available.
        echo The application may work with limited functionality.
    )
)

echo.
echo Installation complete!
echo You can now try running: python main.py
echo.
pause
