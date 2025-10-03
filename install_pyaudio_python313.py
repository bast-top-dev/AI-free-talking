#!/usr/bin/env python3
"""
AI Agent - PyAudio Installation Script for Python 3.13
======================================================

This script provides multiple methods to install PyAudio on Python 3.13,
addressing the compatibility issues with pipwin and js2py.
"""

import sys
import subprocess
import importlib
import platform
from typing import List, Tuple

def check_python_version():
    """Check if we're running on a compatible Python version."""
    version = sys.version_info
    print(f"Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("Warning: Python 3.7+ is recommended")
        return False
    return True

def run_command(cmd: List[str], description: str) -> bool:
    """Run a command and return success status."""
    print(f"\n{description}...")
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"[OK] {description} - Success")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[FAIL] {description} - Failed")
        if e.stderr:
            print(f"Error: {e.stderr.strip()}")
        return False

def test_import(module_name: str, display_name: str = None) -> bool:
    """Test if a module can be imported."""
    if display_name is None:
        display_name = module_name
    
    try:
        importlib.import_module(module_name)
        print(f"[OK] {display_name} - OK")
        return True
    except ImportError:
        print(f"[FAIL] {display_name} - Not available")
        return False

def install_pyaudio_methods():
    """Try multiple methods to install PyAudio."""
    methods = [
        # Method 1: Direct pip install
        ([sys.executable, "-m", "pip", "install", "pyaudio"], "Direct pip install"),
        
        # Method 2: Binary wheel only
        ([sys.executable, "-m", "pip", "install", "--only-binary=all", "pyaudio"], "Binary wheel install"),
        
        # Method 3: No cache
        ([sys.executable, "-m", "pip", "install", "--no-cache-dir", "pyaudio"], "Install without cache"),
        
        # Method 4: Upgrade pip first
        ([sys.executable, "-m", "pip", "install", "--upgrade", "pip", "pyaudio"], "Upgrade pip and install"),
    ]
    
    for cmd, description in methods:
        if run_command(cmd, description):
            return True
    
    # Method 5: Try compilation (requires build tools)
    print("\nTrying manual compilation...")
    if platform.system() == "Windows":
        print("This may require Visual Studio Build Tools or Visual Studio")
    
    build_cmd = [sys.executable, "-m", "pip", "install", "--upgrade", "wheel", "setuptools"]
    if run_command(build_cmd, "Installing build dependencies"):
        compile_cmd = [sys.executable, "-m", "pip", "install", "pyaudio", "--no-binary=pyaudio"]
        if run_command(compile_cmd, "Compiling PyAudio from source"):
            return True
    
    return False

def install_alternatives():
    """Install alternative audio libraries if PyAudio fails."""
    alternatives = [
        ("sounddevice", "sounddevice - Alternative audio I/O"),
        ("soundfile", "soundfile - Audio file I/O"),
        ("vosk", "vosk - Offline speech recognition"),
    ]
    
    print("\nInstalling alternative audio libraries...")
    installed = []
    
    for package, description in alternatives:
        cmd = [sys.executable, "-m", "pip", "install", package]
        if run_command(cmd, f"Installing {description}"):
            installed.append(package)
    
    return installed

def test_installation():
    """Test the installation of required modules."""
    print("\nTesting installation...")
    
    # Test core dependencies
    core_modules = [
        ("pyttsx3", "Text-to-Speech"),
        ("speech_recognition", "Speech Recognition"),
    ]
    
    core_ok = True
    for module, name in core_modules:
        if not test_import(module, name):
            core_ok = False
    
    # Test PyAudio
    pyaudio_ok = test_import("pyaudio", "PyAudio")
    
    if not pyaudio_ok:
        print("\nPyAudio not available, testing alternatives...")
        alternatives = ["sounddevice", "soundfile", "vosk"]
        alt_available = any(test_import(alt, alt) for alt in alternatives)
        
        if alt_available:
            print("Alternative audio libraries are available.")
        else:
            print("No audio libraries available.")
    
    return core_ok and (pyaudio_ok or any(test_import(alt) for alt in ["sounddevice", "soundfile", "vosk"]))

def main():
    """Main installation function."""
    print("AI Agent - PyAudio Installation for Python 3.13")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        print("Please upgrade to Python 3.7 or higher")
        return False
    
    # Install core dependencies
    print("\nInstalling core dependencies...")
    core_cmd = [sys.executable, "-m", "pip", "install", "pyttsx3==2.90", "SpeechRecognition>=3.14.0"]
    if not run_command(core_cmd, "Installing core dependencies"):
        print("Failed to install core dependencies")
        return False
    
    # Try to install PyAudio
    print("\nAttempting PyAudio installation...")
    pyaudio_success = install_pyaudio_methods()
    
    if not pyaudio_success:
        print("\nPyAudio installation failed. Installing alternatives...")
        alternatives = install_alternatives()
        if alternatives:
            print("[OK] Installed alternatives: " + ', '.join(alternatives))
    
    # Test installation
    success = test_installation()
    
    if success:
        print("\n[OK] Installation completed successfully!")
        print("You can now run: python main.py")
    else:
        print("\n[FAIL] Installation completed with issues.")
        print("Some features may not work properly.")
    
    return success

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\nInstallation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        sys.exit(1)
