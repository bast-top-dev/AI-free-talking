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
        
        # Install PyAudio separately for Windows compatibility
        print("Installing PyAudio for Windows...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pipwin"])
            subprocess.check_call([sys.executable, "-m", "pipwin", "install", "pyaudio"])
        except subprocess.CalledProcessError:
            print("Warning: PyAudio installation failed. Trying alternative method...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", "pyaudio"])
            except subprocess.CalledProcessError:
                print("Warning: PyAudio could not be installed automatically.")
                print("Please install manually: pip install pipwin && pipwin install pyaudio")
        
        print("✓ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install dependencies: {e}")
        return False

def main():
    """Main launcher function."""
    print("AI Agent - 電話営業ボット")
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
        print(f"✗ Import error: {e}")
        print("Please make sure all required packages are installed:")
        print("pip install -r requirements.txt")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\nApplication stopped by user.")
        sys.exit(0)
    except Exception as e:
        print(f"✗ Application error: {e}")
        print("\nPlease check the error above and try again.")
        sys.exit(1)

if __name__ == "__main__":
    main()
