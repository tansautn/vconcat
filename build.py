#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Build script for V-CONCAT

This script builds a standalone executable for the V-CONCAT tool using PyInstaller.
"""

#              M""""""""`M            dP
#              Mmmmmm   .M            88
#              MMMMP  .MMM  dP    dP  88  .dP   .d8888b.
#              MMP  .MMMMM  88    88  88888"    88'  `88
#              M' .MMMMMMM  88.  .88  88  `8b.  88.  .88
#              M         M  `88888P'  dP   `YP  `88888P'
#              MMMMMMMMMMM    -*-  Created by Zuko  -*-
#
#              * * * * * * * * * * * * * * * * * * * * *
#              * -    - -   F.R.E.E.M.I.N.D   - -    - *
#              * -  Copyright © 2025 (Z) Programing  - *
#              *    -  -  All Rights Reserved  -  -    *
#              * * * * * * * * * * * * * * * * * * * * *

#
#
import os
import sys
import subprocess
import shutil
import platform
import site
import glob
import json

def check_pyinstaller():
    """Check if PyInstaller is installed."""
    try:
        import PyInstaller
        return True
    except ImportError:
        return False

def install_pyinstaller():
    """Install PyInstaller using pip."""
    print("Installing PyInstaller...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
        return True
    except subprocess.CalledProcessError:
        print("Failed to install PyInstaller.")
        return False

def install_dependencies():
    """Install required dependencies."""
    print("Installing required dependencies...")
    try:
        # Install shtab for command-line completion
        subprocess.run([sys.executable, "-m", "pip", "install", "shtab"], check=False)
        
        # We'll avoid pyreadline in the executable build as it causes issues
        # Instead, we'll modify the script to handle tab completion differently
        return True
    except Exception as e:
        print(f"Warning: Failed to install some dependencies: {str(e)}")
        return False

def find_dlls():
    """Find required DLLs for PyInstaller."""
    dll_paths = []
    
    # Try to find DLLs in common locations
    if platform.system() == "Windows":
        # Check in Python's DLLs directory
        python_dlls = os.path.join(os.path.dirname(sys.executable), "DLLs")
        if os.path.exists(python_dlls):
            dll_paths.append(python_dlls)
        
        # Check in site-packages
        for site_dir in site.getsitepackages():
            dll_paths.append(site_dir)
        
        # Check in Windows system directories
        system32 = os.path.join(os.environ.get("SystemRoot", "C:\\Windows"), "System32")
        if os.path.exists(system32):
            dll_paths.append(system32)
    
    return dll_paths

def build_executable():
    """Build the executable using PyInstaller."""
    print("Building executable...")
    
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Path to vconcat.py
    vconcat_path = os.path.join(script_dir, "vconcat.py")
    
    # Check if vconcat.py exists
    if not os.path.exists(vconcat_path):
        print(f"Error: {vconcat_path} not found.")
        return False
    
    # Create a modified version without pyreadline for the build
    build_script = os.path.join(script_dir, "vconcat_build.py")
    with open(vconcat_path, "r", encoding="utf-8") as src_file:
        content = src_file.read()
    
    # Replace pyreadline imports with a simpler implementation
    content = content.replace("import pyreadline3", "# import pyreadline3 - disabled for build")
    content = content.replace("import pyreadline", "# import pyreadline - disabled for build")
    
    # Simplify the tab completion code
    tab_completion_start = content.find("def get_input_files_interactive():")
    if tab_completion_start > 0:
        tab_completion_end = content.find("def get_output_file_interactive():", tab_completion_start)
        if tab_completion_end > 0:
            simple_implementation = """def get_input_files_interactive():
    \"\"\"Get input files interactively from user.\"\"\"
    input_files = []
    print("Enter video file paths (press Enter on an empty line when done):")
    print("INFO: You can use TAB for filename completion in your terminal")
    while True:
        try:
            file_input = input("> ").strip()
            if not file_input:
                break
                
            # Remove quotes if present
            file_input = file_input.strip('"\\\'')
            
            if os.path.exists(file_input):
                input_files.append(os.path.abspath(file_input))
            else:
                print(f"File not found: {file_input}")
        except KeyboardInterrupt:
            print("\\nInput interrupted.")
            break
    
    return input_files
"""
            content = content[:tab_completion_start] + simple_implementation + content[tab_completion_end:]
    
    # Write the modified script
    with open(build_script, "w", encoding="utf-8") as dst_file:
        dst_file.write(content)
    
    # Find DLL paths
    dll_paths = find_dlls()
    dll_path_str = os.pathsep.join(dll_paths) if dll_paths else ""
    
    # Set environment variables for PyInstaller
    env = os.environ.copy()
    if dll_path_str:
        if "PATH" in env:
            env["PATH"] = dll_path_str + os.pathsep + env["PATH"]
        else:
            env["PATH"] = dll_path_str
    
    # PyInstaller command
    cmd = [
        "pyinstaller",
        "--onefile",  # Create a single executable file
        "--name", "vconcat",  # Name of the output file
        "--icon", "NONE",  # No icon
        "--console",  # Console application
        "--clean",  # Clean PyInstaller cache
        "--noconfirm",  # Overwrite output directory without confirmation
    ]
    
    # Add paths to search for imports
    for path in dll_paths:
        cmd.extend(["--paths", path])
    
    # Add hidden imports
    cmd.extend(["--hidden-import", "argparse"])
    cmd.extend(["--hidden-import", "json"])
    cmd.extend(["--hidden-import", "tempfile"])
    cmd.extend(["--hidden-import", "shutil"])
    cmd.extend(["--hidden-import", "re"])
    cmd.extend(["--hidden-import", "pathlib"])
    cmd.extend(["--hidden-import", "platform"])
    cmd.extend(["--hidden-import", "zipfile"])
    cmd.extend(["--hidden-import", "urllib.request"])
    cmd.extend(["--hidden-import", "collections"])
    
    # Add the script
    cmd.append(build_script)
    
    try:
        subprocess.run(cmd, check=True, env=env)
        # Clean up the temporary build script
        os.remove(build_script)
        return True
    except subprocess.CalledProcessError:
        print("Failed to build executable.")
        if os.path.exists(build_script):
            os.remove(build_script)
        return False

def create_launcher_script():
    """Create a launcher batch script for Windows."""
    print("Creating launcher script...")
    
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Path to the dist directory
    dist_dir = os.path.join(script_dir, "dist")
    
    # Path to the executable
    exe_path = os.path.join(dist_dir, "vconcat.exe")
    
    # Check if the executable exists
    if not os.path.exists(exe_path):
        print(f"Error: {exe_path} not found.")
        return False
    
    # Create the launcher script
    launcher_path = os.path.join(dist_dir, "vconcat.cmd")
    with open(launcher_path, "w") as f:
        f.write("@echo off\n")
        f.write("setlocal enabledelayedexpansion\n\n")
        f.write("echo.\n")
        f.write("echo.\n")
        f.write("echo            M\"\"\"\"\"\"\"\"\"\"\"M            dP                     \n")
        f.write("echo            Mmmmmm   .M            88                     \n")
        f.write("echo            MMMMP  .MMM  dP    dP  88  .dP   .d8888b.     \n")
        f.write("echo            MMP  .MMMMM  88    88  88888\"    88'  `88     \n")
        f.write("echo            M' .MMMMMMM  88.  .88  88  `8b.  88.  .88     \n")
        f.write("echo            M         M  `88888P'  dP   `YP  `88888P'     \n")
        f.write("echo            MMMMMMMMMMM    -*-  Advanced Version  -*-    \n")
        f.write("echo.\n")
        f.write("echo            * * * * * * * * * * * * * * * * * * * * *     \n")
        f.write("echo            * -       V C O N C A T . C M D       - *\n")
        f.write("echo            * * * * * * * * * * * * * * * * * * * * *     \n")
        f.write("echo.\n")
        f.write("echo.\n\n")
        
        f.write("rem Get the directory where this script is located\n")
        f.write("set \"SCRIPT_DIR=%~dp0\"\n\n")
        
        f.write("echo Starting V-CONCAT Advanced Video Concatenation Tool...\n\n")
        
        f.write("rem Check if files were dragged and dropped onto the script\n")
        f.write("if \"%~1\"==\"\" (\n")
        f.write("    rem No files provided, run in interactive mode\n")
        f.write("    \"%SCRIPT_DIR%vconcat.exe\"\n")
        f.write(") else (\n")
        f.write("    rem Files were provided, pass them to the executable\n")
        f.write("    set \"cmd_args=%SCRIPT_DIR%vconcat.exe\"\n")
        f.write("    \n")
        f.write("    rem Add each argument to the command\n")
        f.write("    for %%i in (%*) do (\n")
        f.write("        set \"cmd_args=!cmd_args! \"%%~i\"\"\n")
        f.write("    )\n")
        f.write("    \n")
        f.write("    rem Execute the command with all arguments\n")
        f.write("    !cmd_args!\n")
        f.write(")\n\n")
        
        f.write("if %errorlevel% neq 0 (\n")
        f.write("    echo An error occurred while running the script.\n")
        f.write("    pause\n")
        f.write(")\n\n")
        
        f.write("endlocal\n")
    
    print(f"Launcher script created: {launcher_path}")
    return True

def copy_readme():
    """Copy the README file to the dist directory."""
    print("Copying README...")
    
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Path to the README file
    readme_path = os.path.join(script_dir, "README.md")
    
    # Path to the dist directory
    dist_dir = os.path.join(script_dir, "dist")
    
    # Check if the README file exists
    if not os.path.exists(readme_path):
        print(f"Warning: {readme_path} not found.")
        return False
    
    # Copy the README file
    try:
        shutil.copy2(readme_path, os.path.join(dist_dir, "README.md"))
        return True
    except Exception as e:
        print(f"Error copying README: {str(e)}")
        return False

def main():
    """Main function."""
    print("V-CONCAT Build Script")
    print("=====================")
    
    # Install dependencies
    install_dependencies()
    
    # Check if PyInstaller is installed
    if not check_pyinstaller():
        print("PyInstaller is not installed.")
        if not install_pyinstaller():
            print("Failed to install PyInstaller. Please install it manually:")
            print("pip install pyinstaller")
            return 1
    
    # Build the executable
    if not build_executable():
        print("Failed to build executable.")
        return 1
    
    # Create the launcher script
    if not create_launcher_script():
        print("Failed to create launcher script.")
        return 1
    
    # Copy the README file
    copy_readme()
    
    # Copy the config file if it exists
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, "vconcat.conf")
    dist_dir = os.path.join(script_dir, "dist")
    
    if os.path.exists(config_path):
        try:
            shutil.copy2(config_path, os.path.join(dist_dir, "vconcat.conf"))
            print(f"Config file copied to {os.path.join(dist_dir, 'vconcat.conf')}")
        except Exception as e:
            print(f"Error copying config file: {str(e)}")
    else:
        # Create a sample config file
        sample_config = {
            "prefer_h264": False,
            "no_encode": False,
            "comment": "This is a configuration file for V-CONCAT. Set prefer_h264 to true to always prefer H.264 codec with 29.97 fps when possible. Set no_encode to true to skip re-encoding completely."
        }
        try:
            with open(os.path.join(dist_dir, "vconcat.conf"), 'w') as f:
                json.dump(sample_config, f, indent=4)
            print(f"Sample config file created at {os.path.join(dist_dir, 'vconcat.conf')}")
        except Exception as e:
            print(f"Error creating sample config file: {str(e)}")
    
    print("\nBuild completed successfully!")
    print("The executable and launcher script are in the 'dist' directory.")
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 
