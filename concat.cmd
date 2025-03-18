@echo off
setlocal enabledelayedexpansion

:logo
echo.
echo.
echo            M""""""""`M            dP                     
echo            Mmmmmm   .M            88                     
echo            MMMMP  .MMM  dP    dP  88  .dP   .d8888b.     
echo            MMP  .MMMMM  88    88  88888"    88'  `88     
echo            M' .MMMMMMM  88.  .88  88  `8b.  88.  .88     
echo            M         M  `88888P'  dP   `YP  `88888P'     
echo            MMMMMMMMMMM    -*-  Created by Zuko  -*-    
echo.
echo            * * * * * * * * * * * * * * * * * * * * *     
echo            * -       V C O N C A T . C M D       - *
echo            * * * * * * * * * * * * * * * * * * * * *     
echo.
echo.
echo.

:info
echo - INFO: This tool help you quickly merge multiple videos into one, FASTEST !
echo Files tobe merging should have same ENCODING settings, otherwise output video might be strange, different from inputs.
echo.
echo For example: if you merging a 60fps with a 30fps videos, incorrect timestamp would be in output.
echo actually the tool just calling bellow command after prepared the input lists:
echo.
echo ffmpeg -f concat -safe 0 -i filelist.txt -c:v copy -c:a aac output.mp4
echo.
echo So, you should double check output everytime you use this tool.
echo - INFO: "TAB" completion when entering filename is allowed
echo.
echo * Author: Zuko [tansautn@gmail.com]
echo.
pause

:download_ffmpeg
rem Check if ffmpeg exists in PATH
where ffmpeg >nul 2>nul
if %errorlevel% neq 0 (
    echo FFmpeg not found. Downloading...
    
    rem Download ffmpeg using PowerShell
    powershell -Command "& {Invoke-WebRequest -Uri 'https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip' -OutFile 'ffmpeg.zip'}"
    
    rem Extract using PowerShell
    powershell -Command "& {Expand-Archive -Path 'ffmpeg.zip' -DestinationPath '.' -Force}"

    rem Find the ffmpeg binary directory (it's inside a nested folder)
    for /f "delims=" %%a in ('dir /b /ad ffmpeg*') do set "ffmpeg_dir=%%a"

    rem Move bin directory contents up
    move "!ffmpeg_dir!\bin\*" "." >nul

    rem Clean up
    rmdir /s /q "!ffmpeg_dir!" >nul
    del ffmpeg.zip >nul

    rem Get current directory
    set "current_dir=%CD%"
	echo ""
	echo ""
    rem Add to PATH permanently for current user using PowerShell
    rem Create PowerShell script file
    (
        echo $currentDir = '!current_dir!'
        echo Write-Host "Current directory: $currentDir"
        echo $oldPath = [Environment]::GetEnvironmentVariable('Path', 'User'^)
        echo Write-Host "Current PATH: $oldPath"
        echo if ($oldPath -notlike "*$currentDir*"^) {
        echo     Write-Host "Updating PATH..."
        echo     $newPath = "$oldPath;$currentDir"
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
	echo ""
	echo ""
    REM pause
    
    rem Execute the PowerShell script
    powershell -ExecutionPolicy Bypass -File update_path.ps1
	del filelist.txt 2>nul
	
	REM powershell -Command "& {
        REM $currentDir = '!current_dir!'
        REM Write-Host 'Current directory in PowerShell:' $currentDir
        REM $oldPath = [Environment]::GetEnvironmentVariable('Path', 'User')
        REM Write-Host 'Current PATH:' $oldPath
        REM if ($oldPath -notlike '*' + $currentDir + '*') {
            REM Write-Host 'Updating PATH...'
            REM $newPath = $currentDir + ';' + $oldPath
            REM [Environment]::SetEnvironmentVariable('Path', $newPath, 'User')
            REM Write-Host 'PATH updated successfully'
        REM } else {
            REM Write-Host 'Directory already in PATH'
        REM }
        REM Write-Host 'New PATH:' ([Environment]::GetEnvironmentVariable('Path', 'User'))
    REM }"
    rem Also update current session PATH
    set "PATH=%CD%;%PATH%"
    
    echo FFmpeg downloaded successfully and added to PATH permanently
	del filelist.txt 2>nul
	goto input_loop
)

:main
rem Initialize temporary file to store file names
del filelist.txt 2>nul
goto input_loop
:input_loop

setlocal DisableDelayedExpansion
set "filename="
set /p "filename=Enter file name (or press Enter to start merge): "
rem Check if input is empty
if "%filename%"=="" goto process_files
rem Remove surrounding quotes if present
set "filename=%filename:"=%"
rem Remove ! char from file name
echo "%filename%" | findstr "!" >nul
if not defined errorlevel set /A "errorlevel=1"
if errorlevel EQU 0 (
    if exist "%filename%" (
        ren "%filename%" "%filename:!=%"
        set "filename=%filename:!=%"
    )
)
endlocal & set "filename=%filename%"

setlocal EnableDelayedExpansion
rem Check if file exists
if exist "%filename%" (
    rem Convert to absolute path and handle spaces correctly
    for %%F in ("%filename%") do set "abs_path=%%~fF"
    echo file '!abs_path!' >> filelist.txt
    endlocal & goto input_loop
) else (
    echo File '%filename%' does not exist. Please try again.
    endlocal & goto input_loop
)

:process_files
Check if filelist.txt exists and has content
if not exist filelist.txt (
    echo No valid files were provided. Exiting.
    goto end
)

rem Execute ffmpeg command
REM ffmpeg -f concat -safe 0 -i filelist.txt -c:v libx264 -c:a aac output.mp4
ffmpeg -f concat -safe 0 -i filelist.txt -c:v copy -c:a aac output.mp4
echo DONE


:end
endlocal
