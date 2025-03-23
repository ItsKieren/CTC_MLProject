#!/usr/bin/env python3
import os
import platform
import subprocess
import sys

def get_script_dir():
    """Get the directory where the scripts are located"""
    return os.path.dirname(os.path.abspath(__file__))

def run_windows():
    """Run the Windows batch script"""
    script_path = os.path.join(get_script_dir(), "run_scripts.bat")
    if os.path.exists(script_path):
        print("Running Windows script...")
        # Use shell=True for Windows batch files
        subprocess.run([script_path], shell=True)
    else:
        print("Error: Windows script not found!")
        print(f"Expected path: {script_path}")

def run_unix():
    """Run the shell script for Mac/Linux"""
    script_path = os.path.join(get_script_dir(), "run_scripts.sh")
    if os.path.exists(script_path):
        print("Running Unix script...")
        # Make sure the script is executable
        os.chmod(script_path, 0o755)
        subprocess.run([script_path])
    else:
        print("Error: Unix script not found!")
        print(f"Expected path: {script_path}")

def main():
    system = platform.system().lower()
    
    print(f"Detected OS: {platform.system()}")
    
    try:
        if system == "windows":
            run_windows()
        elif system in ["linux", "darwin"]:  # darwin is macOS
            run_unix()
        else:
            print(f"Unsupported operating system: {system}")
            sys.exit(1)
    except Exception as e:
        print(f"Error running script: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
