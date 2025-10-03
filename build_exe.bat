@echo off
echo AI Agent - Build Executable
echo ===========================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not in PATH.
    echo Please install Python first.
    pause
    exit /b 1
)

echo Installing PyInstaller...
pip install pyinstaller

echo.
echo Building executable...
echo This may take a few minutes...
echo.

REM Build the executable
pyinstaller ^
    --onefile ^
    --windowed ^
    --name "AI_Agent" ^
    --icon=NONE ^
    --add-data "ai_agent;ai_agent" ^
    --hidden-import "pyttsx3" ^
    --hidden-import "speech_recognition" ^
    --hidden-import "tkinter" ^
    --hidden-import "pywintypes" ^
    --hidden-import "win32com.client" ^
    --hidden-import "comtypes" ^
    --collect-all "pyttsx3" ^
    --collect-all "speech_recognition" ^
    main.py

if errorlevel 1 (
    echo.
    echo Build failed! Trying alternative method...
    echo.
    
    REM Alternative build with fewer options
    pyinstaller --onefile --windowed --name "AI_Agent" main.py
    
    if errorlevel 1 (
        echo.
        echo Build failed completely. Check the error messages above.
        echo Common issues:
        echo 1. Missing dependencies
        echo 2. Python path issues
        echo 3. PyInstaller version conflicts
        pause
        exit /b 1
    )
)

echo.
echo ✓ Build completed successfully!
echo.
echo The executable is located in: dist\AI_Agent.exe
echo.
echo You can now distribute this .exe file without requiring Python installation.
echo.
echo Testing the executable...
if exist "dist\AI_Agent.exe" (
    echo ✓ Executable created successfully!
    echo File size:
    dir "dist\AI_Agent.exe" | find "AI_Agent.exe"
    echo.
    echo To run: dist\AI_Agent.exe
) else (
    echo ✗ Executable not found in dist folder.
    echo Check the build output above for errors.
)

echo.
pause