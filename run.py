"""
AI Agent - Simple Launcher Script
=================================

This script provides an easy way to run the AI Agent application.
It handles dependency checking and provides helpful error messages.
"""

import sys
import os
import subprocess

def check_dependencies():
    """Check if required packages are installed."""
    required_packages = ['pyttsx3', 'speech_recognition', 'tkinter']
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'tkinter':
                import tkinter
            elif package == 'pyttsx3':
                import pyttsx3
            elif package == 'speech_recognition':
                import speech_recognition
        except ImportError:
            missing_packages.append(package)
    
    return missing_packages

def install_dependencies():
    """Install missing dependencies."""
    print("Installing required dependencies...")
    try:
        # Install main dependencies
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        
        # Install PyAudio with multiple fallback methods for Python 3.13 compatibility
        print("Installing PyAudio...")
        pyaudio_installed = False
        
        # Method 1: Try direct pip install first
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyaudio"])
            pyaudio_installed = True
            print("[OK] PyAudio installed via direct pip")
        except subprocess.CalledProcessError:
            print("Direct pip install failed, trying alternatives...")
            
            # Method 2: Try binary wheel only
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", "--only-binary=all", "pyaudio"])
                pyaudio_installed = True
                print("[OK] PyAudio installed via binary wheel")
            except subprocess.CalledProcessError:
                print("Binary wheel install failed, trying pipwin...")
                
                # Method 3: Try pipwin (may fail on Python 3.13)
                try:
                    subprocess.check_call([sys.executable, "-m", "pip", "install", "pipwin"])
                    subprocess.check_call([sys.executable, "-m", "pipwin", "install", "pyaudio"])
                    pyaudio_installed = True
                    print("[OK] PyAudio installed via pipwin")
                except subprocess.CalledProcessError:
                    print("pipwin failed (common on Python 3.13), trying compilation...")
                    
                    # Method 4: Try compilation from source
                    try:
                        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "wheel", "setuptools"])
                        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyaudio", "--no-binary=pyaudio"])
                        pyaudio_installed = True
                        print("[OK] PyAudio compiled from source")
                    except subprocess.CalledProcessError:
                        print("Compilation failed, installing alternatives...")
                        
                        # Method 5: Install alternative audio libraries
                        try:
                            subprocess.check_call([sys.executable, "-m", "pip", "install", "sounddevice", "soundfile"])
                            print("[OK] Installed alternative audio libraries (sounddevice, soundfile)")
                        except subprocess.CalledProcessError:
                            print("Warning: Could not install alternative audio libraries")
        
        if not pyaudio_installed:
            print("Warning: PyAudio installation failed.")
            print("The application may work with limited audio functionality.")
            print("For manual installation, try: python install_pyaudio_python313.py")
        
        print("[OK] Dependencies installation completed!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[FAIL] Failed to install dependencies: {e}")
        return False

def main():
    """Main launcher function."""
    print("AI Agent - Telephone Sales Bot")
    print("=" * 40)
    
    # Add current directory to Python path
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    
    # Check dependencies
    missing = check_dependencies()
    
    if missing:
        print(f"Missing dependencies: {', '.join(missing)}")
        print("\nInstalling dependencies...")
        
        if not install_dependencies():
            print("\nPlease install dependencies manually:")
            print("pip install -r requirements.txt")
            sys.exit(1)
    
    # Run the application
    try:
        print("\nStarting AI Agent...")
        from main import main as run_app
        run_app()
    except ImportError as e:
        print(f"[FAIL] Import error: {e}")
        print("Please make sure all required packages are installed:")
        print("pip install -r requirements.txt")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\nApplication stopped by user.")
        sys.exit(0)
    except Exception as e:
        print(f"[FAIL] Application error: {e}")
        print("\nPlease check the error above and try again.")
        sys.exit(1)

if __name__ == "__main__":
    main()
