# Python 3.13 Compatibility Guide

## Issue Description

If you're using Python 3.13 and encountering the error:

```
RuntimeError: Your python version made changes to the bytecode
```

This is caused by a compatibility issue between Python 3.13 and the `js2py` library, which is a dependency of `pipwin`. The error occurs because Python 3.13 introduced changes to the bytecode format that `js2py` doesn't recognize.

## Solutions

### Quick Fix

Run one of these commands to install PyAudio using alternative methods:

**Option 1: Use the dedicated Python 3.13 installer**
```bash
python install_pyaudio_python313.py
```

**Option 2: Use the updated batch script**
```bash
install_pyaudio_python313.bat
```

**Option 3: Manual installation**
```bash
# Try direct pip install first
pip install pyaudio

# If that fails, try binary wheel only
pip install --only-binary=all pyaudio

# If that fails, try without cache
pip install --no-cache-dir pyaudio

# If all else fails, install alternatives
pip install sounddevice soundfile
```

### Installation Methods (in order of preference)

1. **Direct pip install** - Works in most cases
2. **Binary wheel only** - Avoids compilation issues
3. **No cache install** - Clears any corrupted cache
4. **Source compilation** - Requires build tools (Visual Studio on Windows)
5. **Alternative libraries** - `sounddevice` and `soundfile` as fallbacks

### Alternative Audio Libraries

If PyAudio installation completely fails, the application will try to use these alternatives:

- **sounddevice**: Modern alternative to PyAudio
- **soundfile**: Audio file I/O operations
- **vosk**: Offline speech recognition

### Requirements for Compilation

If you need to compile PyAudio from source on Windows, you'll need:

1. **Microsoft Visual Studio Build Tools** or **Visual Studio**
2. **Windows SDK**
3. **CMake** (optional but recommended)

Download Visual Studio Build Tools from: https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2022

### Testing Your Installation

After installation, test with:

```python
# Test core dependencies
import pyttsx3
import speech_recognition

# Test PyAudio
try:
    import pyaudio
    print("✓ PyAudio is working")
except ImportError:
    print("PyAudio not available, testing alternatives...")
    try:
        import sounddevice
        print("✓ sounddevice is available")
    except ImportError:
        print("✗ No audio libraries available")
```

### Troubleshooting

**Problem**: `pip install pyaudio` fails with compilation errors
**Solution**: Install Visual Studio Build Tools or use binary wheels

**Problem**: `pipwin install pyaudio` fails with bytecode error
**Solution**: Use the alternative installation methods above

**Problem**: Application runs but audio doesn't work
**Solution**: Check if PyAudio or alternative libraries are properly installed

**Problem**: Speech recognition doesn't work
**Solution**: Ensure internet connection for Google Speech Recognition API

### Python Version Compatibility

- **Python 3.7-3.12**: Full compatibility with all installation methods
- **Python 3.13**: Use alternative installation methods (this guide)
- **Python 3.14+**: Unknown compatibility, may need updates

### Getting Help

If you continue to have issues:

1. Check your Python version: `python --version`
2. Try the dedicated installer: `python install_pyaudio_python313.py`
3. Install Visual Studio Build Tools if compilation is needed
4. Consider using alternative audio libraries

The application should work even without PyAudio, though with limited audio functionality.
