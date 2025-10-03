@echo off
echo AI Agent - PyWinTypes Fix for Python 3.13
echo ==========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not in PATH.
    echo Please install Python 3.7-3.11 from https://python.org
    echo Python 3.13 has compatibility issues with pywin32
    pause
    exit /b 1
)

echo Installing pywin32 for Python 3.13...
echo.

REM Uninstall existing pywin32 if present
echo Uninstalling old pywin32...
pip uninstall pywin32 -y

REM Install pywin32
echo Installing pywin32...
pip install pywin32

REM Post-install script for pywin32
echo Running pywin32 post-install script...
python -c "import sys; import subprocess; subprocess.run([sys.executable, '-c', 'import win32com.client; print(\"pywin32 installed successfully\")'])"

REM Install pyttsx3
echo Installing pyttsx3...
pip install pyttsx3

REM Test installation
echo.
echo Testing installation...
python -c "import pywintypes; import pyttsx3; print('✓ pywintypes and pyttsx3 working!')" 2>nul
if errorlevel 1 (
    echo.
    echo Installation may have issues. Trying alternative method...
    echo.
    echo Method 1: Install from conda-forge
    echo conda install -c conda-forge pywin32
    echo.
    echo Method 2: Use older Python version (3.11 recommended)
    echo.
    echo Method 3: Try manual installation
    pip install --force-reinstall pywin32
) else (
    echo.
    echo ✓ pywintypes and pyttsx3 installed successfully!
    echo You can now run: python main.py
)

echo.
pause
