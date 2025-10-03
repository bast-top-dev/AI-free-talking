#!/usr/bin/env python3
"""
AI Agent - Executable Builder Script
===================================

This script builds a standalone executable (.exe) file from the AI Agent project.
It handles all the necessary configurations for PyInstaller.
"""

import os
import sys
import subprocess
import shutil
import platform
from pathlib import Path

def check_pyinstaller():
    """Check if PyInstaller is installed."""
    try:
        import PyInstaller
        print(f"[OK] PyInstaller {PyInstaller.__version__} is available")
        return True
    except ImportError:
        print("[FAIL] PyInstaller not found")
        return False

def install_pyinstaller():
    """Install PyInstaller if not available."""
    print("Installing PyInstaller...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller>=5.0"])
        print("[OK] PyInstaller installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("[FAIL] Failed to install PyInstaller")
        return False

def clean_build_dirs():
    """Clean previous build directories."""
    dirs_to_clean = ['build', 'dist', '__pycache__']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            print(f"Cleaning {dir_name}...")
            shutil.rmtree(dir_name)
    
    # Clean .spec files
    for spec_file in Path('.').glob('*.spec'):
        print(f"Removing {spec_file}")
        spec_file.unlink()

def create_spec_file():
    """Create a PyInstaller spec file with proper configuration."""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('ai_agent', 'ai_agent'),
    ],
    hiddenimports=[
        'pyttsx3',
        'speech_recognition',
        'pyaudio',
        'sounddevice',
        'soundfile',
        'tkinter',
        'tkinter.ttk',
        'tkinter.messagebox',
        'tkinter.filedialog',
        'threading',
        'queue',
        'json',
        'time',
        'random',
        'os',
        'sys',
        'pathlib',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='AI_Agent',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)
'''
    
    with open('AI_Agent.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    print("[OK] Created AI_Agent.spec file")

def build_executable():
    """Build the executable using PyInstaller."""
    print("Building executable...")
    
    try:
        # Use the spec file for building
        cmd = [sys.executable, "-m", "PyInstaller", "--clean", "AI_Agent.spec"]
        subprocess.check_call(cmd)
        print("[OK] Executable built successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[FAIL] Build failed: {e}")
        return False

def build_simple_executable():
    """Build a simple executable without spec file."""
    print("Building simple executable...")
    
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--console",
        "--name", "AI_Agent",
        "--add-data", "ai_agent;ai_agent",
        "--hidden-import", "pyttsx3",
        "--hidden-import", "speech_recognition", 
        "--hidden-import", "pyaudio",
        "--hidden-import", "tkinter",
        "--hidden-import", "tkinter.ttk",
        "--hidden-import", "tkinter.messagebox",
        "--hidden-import", "tkinter.filedialog",
        "main.py"
    ]
    
    try:
        subprocess.check_call(cmd)
        print("[OK] Simple executable built successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[FAIL] Simple build failed: {e}")
        return False

def test_executable():
    """Test if the executable was created."""
    exe_path = os.path.join("dist", "AI_Agent.exe")
    if os.path.exists(exe_path):
        size = os.path.getsize(exe_path)
        size_mb = size / (1024 * 1024)
        print(f"[OK] Executable created: {exe_path}")
        print(f"Size: {size_mb:.1f} MB")
        return True
    else:
        print("[FAIL] Executable not found")
        return False

def create_build_info():
    """Create build information file."""
    info_content = f"""AI Agent - Build Information
============================

Build Date: {subprocess.check_output(['date', '/t'], shell=True, text=True).strip()}
Python Version: {sys.version}
Platform: {platform.platform()}
Architecture: {platform.architecture()[0]}

Executable Location: dist/AI_Agent.exe

Usage:
1. Double-click AI_Agent.exe to run
2. Or run from command line: dist/AI_Agent.exe

Notes:
- First run may be slower as it extracts dependencies
- Antivirus software may flag the executable (false positive)
- Make sure you have a microphone and speakers connected
- Internet connection required for speech recognition

Troubleshooting:
- If the executable doesn't start, try running from command line
- Check Windows Defender or antivirus exclusions
- Ensure all audio devices are working
"""
    
    with open('BUILD_INFO.txt', 'w', encoding='utf-8') as f:
        f.write(info_content)
    
    print("[OK] Created BUILD_INFO.txt")

def main():
    """Main build function."""
    print("AI Agent - Executable Builder")
    print("=" * 40)
    
    # Check if we're in the right directory
    if not os.path.exists('main.py'):
        print("[FAIL] main.py not found. Please run this script from the project root directory.")
        return False
    
    # Check/install PyInstaller
    if not check_pyinstaller():
        if not install_pyinstaller():
            return False
    
    # Clean previous builds
    clean_build_dirs()
    
    # Try building with spec file first
    create_spec_file()
    if not build_executable():
        print("Spec file build failed, trying simple build...")
        if not build_simple_executable():
            print("[FAIL] All build methods failed")
            return False
    
    # Test the executable
    if test_executable():
        create_build_info()
        print("\n[OK] Build completed successfully!")
        print("Executable location: dist/AI_Agent.exe")
        print("See BUILD_INFO.txt for more details")
        return True
    else:
        print("[FAIL] Build verification failed")
        return False

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\nBuild cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        sys.exit(1)
