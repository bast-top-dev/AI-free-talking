"""
AI Agent - Advanced Build Script for Executable
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(command, description, check=True):
    """Run a command and return success status."""
    print(f"Running: {description}")
    print(f"Command: {command}")
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✓ {description} - Success")
            if result.stdout:
                print(f"Output: {result.stdout}")
            return True
        else:
            print(f"✗ {description} - Failed")
            print(f"Error: {result.stderr}")
            if result.stdout:
                print(f"Output: {result.stdout}")
            if check:
                return False
            return True
            
    except Exception as e:
        print(f"✗ {description} - Exception: {e}")
        return False

def check_requirements():
    """Check if all requirements are met."""
    print("Checking build requirements...")
    
    # Check Python version
    python_version = sys.version_info
    print(f"Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    if python_version.major != 3:
        print("✗ Python 3 is required")
        return False
    
    # Check if main.py exists
    if not os.path.exists("main.py"):
        print("✗ main.py not found")
        return False
    
    # Check if ai_agent package exists
    if not os.path.exists("ai_agent"):
        print("✗ ai_agent package not found")
        return False
    
    print("✓ All requirements met")
    return True

def install_pyinstaller():
    """Install PyInstaller if not already installed."""
    print("\nInstalling PyInstaller...")
    
    # Check if PyInstaller is already installed
    try:
        import PyInstaller
        print("✓ PyInstaller already installed")
        return True
    except ImportError:
        pass
    
    # Install PyInstaller
    return run_command("pip install pyinstaller", "Install PyInstaller")

def clean_build():
    """Clean previous build artifacts."""
    print("\nCleaning previous build artifacts...")
    
    dirs_to_clean = ["build", "dist", "__pycache__"]
    files_to_clean = ["*.spec"]
    
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            try:
                shutil.rmtree(dir_name)
                print(f"✓ Cleaned {dir_name}")
            except Exception as e:
                print(f"⚠ Could not clean {dir_name}: {e}")
    
    # Clean .spec files
    for spec_file in Path(".").glob("*.spec"):
        try:
            spec_file.unlink()
            print(f"✓ Cleaned {spec_file}")
        except Exception as e:
            print(f"⚠ Could not clean {spec_file}: {e}")

def build_executable():
    """Build the executable."""
    print("\nBuilding executable...")
    
    # PyInstaller command with all necessary options
    cmd = [
        "pyinstaller",
        "--onefile",                    # Single executable file
        "--windowed",                   # No console window
        "--name", "AI_Agent",          # Output name
        "--add-data", "ai_agent;ai_agent",  # Include ai_agent package
        "--hidden-import", "pyttsx3",   # Explicitly import pyttsx3
        "--hidden-import", "speech_recognition",
        "--hidden-import", "tkinter",
        "--hidden-import", "pywintypes",
        "--hidden-import", "win32com.client",
        "--hidden-import", "comtypes",
        "--collect-all", "pyttsx3",     # Collect all pyttsx3 dependencies
        "--collect-all", "speech_recognition",
        "--clean",                      # Clean cache
        "main.py"
    ]
    
    command = " ".join(cmd)
    
    print("PyInstaller command:")
    print(command)
    print()
    
    # Try the full command first
    if run_command(command, "Build executable with full options", check=False):
        return True
    
    print("\nFull build failed, trying simplified build...")
    
    # Simplified command
    simple_cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed", 
        "--name", "AI_Agent",
        "--clean",
        "main.py"
    ]
    
    simple_command = " ".join(simple_cmd)
    return run_command(simple_command, "Build executable with simplified options")

def verify_build():
    """Verify the build was successful."""
    print("\nVerifying build...")
    
    exe_path = "dist/AI_Agent.exe"
    
    if not os.path.exists(exe_path):
        print("✗ Executable not found")
        return False
    
    # Get file size
    file_size = os.path.getsize(exe_path)
    file_size_mb = file_size / (1024 * 1024)
    
    print(f"✓ Executable created successfully!")
    print(f"  Location: {exe_path}")
    print(f"  Size: {file_size_mb:.1f} MB")
    
    return True

def create_launcher():
    """Create a simple launcher batch file."""
    print("\nCreating launcher...")
    
    launcher_content = """@echo off
echo Starting AI Agent...
echo ====================
echo.

REM Check if executable exists
if not exist "AI_Agent.exe" (
    echo Error: AI_Agent.exe not found!
    echo Please make sure the executable is in the same folder as this launcher.
    pause
    exit /b 1
)

REM Run the executable
AI_Agent.exe

REM Pause to see any error messages
if errorlevel 1 (
    echo.
    echo Application exited with error code %errorlevel%
    pause
)
"""
    
    try:
        with open("dist/Launch_AI_Agent.bat", "w") as f:
            f.write(launcher_content)
        print("✓ Launcher created: dist/Launch_AI_Agent.bat")
        return True
    except Exception as e:
        print(f"✗ Failed to create launcher: {e}")
        return False

def main():
    """Main build process."""
    print("AI Agent - Advanced Build Script")
    print("=" * 40)
    print()
    
    try:
        # Step 1: Check requirements
        if not check_requirements():
            print("\n❌ Requirements check failed")
            return False
        
        # Step 2: Install PyInstaller
        if not install_pyinstaller():
            print("\n❌ Failed to install PyInstaller")
            return False
        
        # Step 3: Clean previous builds
        clean_build()
        
        # Step 4: Build executable
        if not build_executable():
            print("\n❌ Build failed")
            return False
        
        # Step 5: Verify build
        if not verify_build():
            print("\n❌ Build verification failed")
            return False
        
        # Step 6: Create launcher
        create_launcher()
        
        print("\n" + "=" * 40)
        print("🎉 BUILD COMPLETED SUCCESSFULLY!")
        print("=" * 40)
        print()
        print("Files created:")
        print("  📁 dist/AI_Agent.exe - Main executable")
        print("  📁 dist/Launch_AI_Agent.bat - Windows launcher")
        print()
        print("Usage:")
        print("  1. Copy the 'dist' folder to any Windows computer")
        print("  2. Double-click 'Launch_AI_Agent.bat' or 'AI_Agent.exe'")
        print("  3. No Python installation required on target computer!")
        print()
        
        return True
        
    except KeyboardInterrupt:
        print("\n\nBuild cancelled by user.")
        return False
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        print("\n❌ Build failed. Check the error messages above.")
    input("\nPress Enter to exit...")