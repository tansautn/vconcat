@echo off
setlocal enabledelayedexpansion

echo.
echo.
echo            M""""""""`M            dP                     
echo            Mmmmmm   .M            88                     
echo            MMMMP  .MMM  dP    dP  88  .dP   .d8888b.     
echo            MMP  .MMMMM  88    88  88888"    88'  `88     
echo            M' .MMMMMMM  88.  .88  88  `8b.  88.  .88     
echo            M         M  `88888P'  dP   `YP  `88888P'     
echo            MMMMMMMMMMM    -*-  Advanced Version  -*-    
echo.
echo            * * * * * * * * * * * * * * * * * * * * *     
echo            * -       V C O N C A T . C M D       - *
echo            * * * * * * * * * * * * * * * * * * * * *     
echo.
echo.

rem Get the directory where this script is located
set "SCRIPT_DIR=%~dp0"
:download_ffmpeg
rem Check if ffmpeg exists in PATH
rem Check if ffmpeg exists in PATH or script directory
where ffmpeg >nul 2>nul
if %errorlevel% neq 0 (
    if not exist "%SCRIPT_DIR%ffmpeg.exe" (
        echo FFmpeg not found. Downloading...
        
        rem Download ffmpeg using PowerShell
        powershell -Command "& {Invoke-WebRequest -Uri 'https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip' -OutFile 'ffmpeg.zip'}"
        
        rem Extract using PowerShell
        powershell -Command "& {Expand-Archive -Path 'ffmpeg.zip' -DestinationPath '.' -Force}"

        rem Find the ffmpeg binary directory (it's inside a nested folder)
        for /f "delims=" %%a in ('dir /b /ad ffmpeg*') do set "ffmpeg_dir=%%a"

        rem Move bin directory contents up
        move "!ffmpeg_dir!\bin\*" "%SCRIPT_DIR%" >nul

        rem Clean up
        rmdir /s /q "!ffmpeg_dir!" >nul
        del ffmpeg.zip >nul

        rem Add to PATH permanently for current user using PowerShell
        rem Create PowerShell script file
        (
            echo $scriptDir = '%SCRIPT_DIR:'=''%'
            echo Write-Host "Script directory: $scriptDir"
            echo $oldPath = [Environment]::GetEnvironmentVariable('Path', 'User'^)
            echo Write-Host "Current PATH: $oldPath"
            echo if ($oldPath -notlike "*$scriptDir*"^) {
            echo     Write-Host "Updating PATH..."
            echo     $newPath = "$oldPath;$scriptDir"
            echo     [Environment]::SetEnvironmentVariable('Path', $newPath, 'User'^)
            echo     Write-Host "PATH updated successfully"
            echo } else {
            echo     Write-Host "Directory already in PATH"
            echo }
            echo Write-Host "Final PATH:" ([Environment]::GetEnvironmentVariable('Path', 'User'^)^)
        ) > update_path.ps1
        
        echo Generated PowerShell script:
        type update_path.ps1
        echo.
        echo.
        
        rem Execute the PowerShell script
        powershell -ExecutionPolicy Bypass -File update_path.ps1
        del update_path.ps1
        
        rem Also update current session PATH
        set "PATH=%SCRIPT_DIR%;%PATH%"
        
        echo FFmpeg downloaded successfully and added to PATH permanently
        echo.
    )
)

echo Checking for Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    rem Check if we have the executable version
    if exist "%SCRIPT_DIR%vconcat.exe" (
        goto run_executable
    ) else (
        echo Python is not installed or not in PATH.
        echo Please install Python from https://www.python.org/downloads/
        echo Make sure to check "Add Python to PATH" during installation.
        pause
        exit /b 1
    )
)

rem Check if we have the Python script or executable
if exist "%SCRIPT_DIR%vconcat.py" (
    echo Starting V-CONCAT Advanced Video Concatenation Tool (Python version)...
    
    rem Check for required Python packages
    python -c "import json, subprocess, tempfile, shutil, re, pathlib, argparse" >nul 2>&1
    if %errorlevel% neq 0 (
        echo Installing required Python packages...
        python -m pip install pathlib
    )
    
    rem Check if files were dragged and dropped onto the script
    if "%~1"=="" (
        rem No files provided, run in interactive mode
        python "%SCRIPT_DIR%vconcat.py"
    ) else (
        rem Files were provided, pass them to the Python script
        set "cmd_args=python "%SCRIPT_DIR%vconcat.py""
        
        rem Add each argument to the command
        for %%i in (%*) do (
            set "cmd_args=!cmd_args! "%%~i""
        )
        
        rem Execute the command with all arguments
        !cmd_args!
    )
) else if exist "%SCRIPT_DIR%vconcat.exe" (
    :run_executable
    echo Starting V-CONCAT Advanced Video Concatenation Tool (Executable version)...
    
    rem Check if files were dragged and dropped onto the script
    if "%~1"=="" (
        rem No files provided, run in interactive mode
        "%SCRIPT_DIR%vconcat.exe"
    ) else (
        rem Files were provided, pass them to the executable
        set "cmd_args=%SCRIPT_DIR%vconcat.exe"
        
        rem Add each argument to the command
        for %%i in (%*) do (
            set "cmd_args=!cmd_args! "%%~i""
        )
        
        rem Execute the command with all arguments
        !cmd_args!
    )
) else (
    echo Error: Neither vconcat.py nor vconcat.exe found in %SCRIPT_DIR%
    pause
    exit /b 1
)

if %errorlevel% neq 0 (
    echo An error occurred while running the script.
    pause
)

endlocal 
