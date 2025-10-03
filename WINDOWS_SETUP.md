# Windows Setup Guide - AI Agent

## 🚨 PyAudio Installation Issue Fix

The error you encountered is common on Windows. PyAudio requires the PortAudio library to compile, which can be tricky to install. Here are several solutions:

## 🛠️ Solution 1: Use pipwin (Recommended)

```bash
# Install pipwin first
pip install pipwin

# Install PyAudio through pipwin
pipwin install pyaudio

# Install other dependencies
pip install -r requirements.txt
```

## 🛠️ Solution 2: Use Pre-compiled Wheel

```bash
# Install PyAudio directly (sometimes works)
pip install pyaudio

# If that fails, try with --only-binary
pip install --only-binary=all pyaudio
```

## 🛠️ Solution 3: Manual Installation

1. **Download Visual C++ Build Tools**:
   - Go to: https://visualstudio.microsoft.com/visual-cpp-build-tools/
   - Download and install "Build Tools for Visual Studio 2022"
   - Make sure to include "C++ build tools" during installation

2. **Install PortAudio**:
   ```bash
   # Download pre-compiled PortAudio for Windows
   # Or install through conda if you have it
   conda install portaudio
   ```

3. **Install PyAudio**:
   ```bash
   pip install pyaudio
   ```

## 🛠️ Solution 4: Use Conda (Alternative)

If you have Anaconda or Miniconda:

```bash
# Create new environment
conda create -n ai-agent python=3.9

# Activate environment
conda activate ai-agent

# Install dependencies
conda install pyaudio
pip install pyttsx3 speech_recognition
```

## 🚀 Quick Fix - Try This First

Run these commands in order:

```bash
# 1. Install pipwin
pip install pipwin

# 2. Install PyAudio through pipwin
pipwin install pyaudio

# 3. Install other dependencies
pip install pyttsx3 speech_recognition

# 4. Run the application
python main.py
```

## 🔧 Alternative: Use the Updated Launcher

The `start_ai_agent.bat` file has been updated to handle this automatically. Try running it again:

```bash
# Double-click or run
start_ai_agent.bat
```

## 🆘 If All Else Fails

### Option A: Skip PyAudio (Limited Functionality)
You can run the application without PyAudio, but speech recognition won't work:

```bash
pip install pyttsx3 speech_recognition
python main.py
```

### Option B: Use Online Speech Recognition
Modify the speech recognizer to use a different backend that doesn't require PyAudio.

### Option C: Use Docker
```bash
# Build and run with Docker (bypasses Windows compilation issues)
docker build -t ai-agent .
docker run -it --device /dev/snd ai-agent
```

## 📋 Verification

After installation, verify everything works:

```python
# Test in Python console
import pyttsx3
import speech_recognition
import tkinter

print("All dependencies installed successfully!")
```

## 🔍 Common Issues

1. **"Microsoft Visual C++ 14.0 is required"**
   - Install Visual Studio Build Tools
   - Or use pipwin method above

2. **"Cannot open include file: 'portaudio.h'"**
   - Use pipwin: `pipwin install pyaudio`

3. **"Access denied" during installation**
   - Run command prompt as Administrator

4. **Python version compatibility**
   - Make sure you're using Python 3.7-3.11
   - Python 3.12+ may have compatibility issues

## 🎯 Success Indicators

When everything is working, you should see:
- No error messages during installation
- AI Agent window opens successfully
- Microphone and speaker icons appear in system tray
- You can start a conversation by clicking "開始"

---

**Try the pipwin method first - it solves the PyAudio issue in 90% of cases!** 🎉
