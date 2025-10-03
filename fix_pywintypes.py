"""
Fix script for pywintypes and pywin32 issues on Python 3.13
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and return success status."""
    print(f"Running: {description}")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ {description} - Success")
            return True
        else:
            print(f"✗ {description} - Failed")
            print(f"Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"✗ {description} - Exception: {e}")
        return False

def fix_pywintypes():
    """Fix pywintypes installation issues."""
    print("AI Agent - PyWinTypes Fix for Python 3.13")
    print("=" * 50)
    print()
    
    # Check Python version
    python_version = sys.version_info
    print(f"Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    if python_version.major == 3 and python_version.minor >= 13:
        print("⚠️  Warning: Python 3.13+ may have compatibility issues with pywin32")
        print("   Consider using Python 3.11 for better compatibility")
        print()
    
    # Step 1: Uninstall existing pywin32
    print("Step 1: Uninstalling existing pywin32...")
    run_command("pip uninstall pywin32 -y", "Uninstall pywin32")
    
    # Step 2: Install pywin32
    print("\nStep 2: Installing pywin32...")
    success = run_command("pip install pywin32", "Install pywin32")
    
    if not success:
        print("\nTrying alternative installation methods...")
        
        # Try with --force-reinstall
        print("Trying force reinstall...")
        success = run_command("pip install --force-reinstall pywin32", "Force reinstall pywin32")
        
        if not success:
            print("Trying with --no-deps...")
            success = run_command("pip install --no-deps pywin32", "Install pywin32 without dependencies")
    
    # Step 3: Install pyttsx3
    print("\nStep 3: Installing pyttsx3...")
    run_command("pip install pyttsx3", "Install pyttsx3")
    
    # Step 4: Test installation
    print("\nStep 4: Testing installation...")
    test_code = """
try:
    import pywintypes
    print("✓ pywintypes imported successfully")
    
    import pyttsx3
    print("✓ pyttsx3 imported successfully")
    
    # Test TTS engine initialization
    engine = pyttsx3.init()
    print("✓ TTS engine initialized successfully")
    
    print("\\n🎉 All components working correctly!")
    
except ImportError as e:
    print(f"✗ Import error: {e}")
    return False
except Exception as e:
    print(f"✗ Error: {e}")
    return False
"""
    
    try:
        exec(test_code)
        print("\n✓ Installation test passed!")
        return True
    except Exception as e:
        print(f"\n✗ Installation test failed: {e}")
        return False

def show_alternatives():
    """Show alternative solutions."""
    print("\n" + "=" * 50)
    print("ALTERNATIVE SOLUTIONS:")
    print("=" * 50)
    print()
    
    print("1. Use Python 3.11 (Recommended):")
    print("   - Download Python 3.11 from python.org")
    print("   - Create virtual environment: python3.11 -m venv ai_agent_env")
    print("   - Install dependencies: pip install -r requirements.txt")
    print()
    
    print("2. Use conda environment:")
    print("   - conda create -n ai-agent python=3.11")
    print("   - conda activate ai-agent")
    print("   - conda install -c conda-forge pywin32")
    print("   - pip install pyttsx3 speech_recognition")
    print()
    
    print("3. Use alternative TTS engine:")
    print("   - Modify the code to use Windows SAPI directly")
    print("   - Or use online TTS services")
    print()
    
    print("4. Manual pywin32 installation:")
    print("   - Download pywin32 wheel from: https://github.com/mhammond/pywin32/releases")
    print("   - Install with: pip install pywin32-XXX.whl")

def main():
    """Main function."""
    try:
        success = fix_pywintypes()
        
        if success:
            print("\n🎉 Fix completed successfully!")
            print("You can now run: python main.py")
        else:
            print("\n❌ Fix failed. Trying alternative solutions...")
            show_alternatives()
            
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        show_alternatives()

if __name__ == "__main__":
    main()
