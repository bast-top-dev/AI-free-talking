@echo off
echo AI Agent - Executable Builder
echo ============================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not in PATH.
    echo Please install Python 3.7+ from https://python.org
    pause
    exit /b 1
)

REM Check if main.py exists
if not exist "main.py" (
    echo main.py not found. Please run this script from the project root directory.
    pause
    exit /b 1
)

echo Installing/updating PyInstaller...
pip install --upgrade pyinstaller>=5.0

echo.
echo Cleaning previous builds...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
if exist "*.spec" del /q "*.spec"

echo.
echo Building executable...
pyinstaller --onefile --console --name "AI_Agent" --add-data "ai_agent;ai_agent" --hidden-import "pyttsx3" --hidden-import "speech_recognition" --hidden-import "pyaudio" --hidden-import "tkinter" --hidden-import "tkinter.ttk" --hidden-import "tkinter.messagebox" --hidden-import "tkinter.filedialog" main.py

if exist "dist\AI_Agent.exe" (
    echo.
    echo [OK] Executable built successfully!
    echo Location: dist\AI_Agent.exe
    echo.
    echo File size:
    dir "dist\AI_Agent.exe" | find "AI_Agent.exe"
    echo.
    echo You can now run the executable by double-clicking it or running:
    echo dist\AI_Agent.exe
) else (
    echo.
    echo [FAIL] Build failed. Check the output above for errors.
    echo Try running: python build_exe.py
)

echo.
pause
