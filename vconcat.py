#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
V-CONCAT | Advanced Video Concatenation Tool

This script helps concatenate multiple video files into one, handling different
encoding settings by re-encoding files that don't match the most common format.

Author: Based on lite version of cmd script by Zuko [tansautn@gmail.com]
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
import json
import subprocess
import tempfile
import shutil
import traceback
from collections import Counter
import re
from pathlib import Path
import platform
import argparse
import zipfile
import urllib.request
import shtab

# ASCII Art Banner
BANNER = """
            M\"\"\"\"\"\"\"\"`M            dP
            Mmmmmm   .M            88                     
            MMMMP  .MMM  dP    dP  88  .dP   .d8888b.     
            MMP  .MMMMM  88    88  88888\"    88'  `88     
            M' .MMMMMMM  88.  .88  88  `8b.  88.  .88     
            M         M  `88888P'  dP   `YP  `88888P'     
            MMMMMMMMMMM    -*-  Advanced Version  -*-    

            * * * * * * * * * * * * * * * * * * * * *     
            * -       V C O N C A T . P Y         - *
            * * * * * * * * * * * * * * * * * * * * *     
"""
DEBUG_MODE = False
def print_banner():
    """Print the application banner."""
    print(BANNER)
    print("\nThis tool helps you quickly merge multiple videos into one, handling different encodings!")
    print("This advanced version will analyze all input videos and re-encode any that don't match the most common format.")
    print("")
    print("\nAuthor: Based on lite version of cmd script by Zuko [tansautn@gmail.com]")
    print()

def get_application_path():
    """Get the correct application path regardless of how the application is run."""
    if getattr(sys, 'frozen', False):
        # Running as compiled executable
        return os.path.dirname(sys.executable)
    else:
        # Running as script
        return os.path.dirname(os.path.abspath(__file__))

def load_config():
    """Load configuration from vconcat.conf if it exists."""
    config = {}
    config_path = os.path.join(get_application_path(), "vconcat.conf")
    
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
            print(f"Loaded configuration from {config_path}")
        except Exception as e:
            print(f"Error loading configuration: {str(e)}")
    if config.get('debug_mode', False):
        DEBUG_MODE = True
    return config

def download_ffmpeg():
    """Download and install FFmpeg if not already installed."""
    print("FFmpeg not found. Downloading...")
    
    # Create a temporary directory for downloading
    with tempfile.TemporaryDirectory() as temp_dir:
        # Download FFmpeg
        ffmpeg_zip = os.path.join(temp_dir, "ffmpeg.zip")
        ffmpeg_url = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"
        
        print(f"Downloading FFmpeg from {ffmpeg_url}...")
        try:
            urllib.request.urlretrieve(ffmpeg_url, ffmpeg_zip)
        except Exception as e:
            print(f"Error downloading FFmpeg: {str(e)}")
            return False
        
        # Extract FFmpeg
        print("Extracting FFmpeg...")
        try:
            with zipfile.ZipFile(ffmpeg_zip, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
            
            # Find the FFmpeg directory
            ffmpeg_dir = None
            for item in os.listdir(temp_dir):
                if os.path.isdir(os.path.join(temp_dir, item)) and item.startswith("ffmpeg"):
                    ffmpeg_dir = os.path.join(temp_dir, item)
                    break
            
            if not ffmpeg_dir:
                print("Could not find FFmpeg directory in the extracted files.")
                return False
            
            # Copy FFmpeg binaries to the application directory
            bin_dir = os.path.join(ffmpeg_dir, "bin")
            app_dir = get_application_path()
            
            for file in os.listdir(bin_dir):
                src = os.path.join(bin_dir, file)
                dst = os.path.join(app_dir, file)
                shutil.copy2(src, dst)
            
            # Add application directory to PATH
            os.environ["PATH"] = app_dir + os.pathsep + os.environ["PATH"]
            
            # Add to PATH permanently for Windows
            if platform.system() == "Windows":
                try:
                    import winreg
                    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment", 0, winreg.KEY_ALL_ACCESS) as key:
                        path_value, _ = winreg.QueryValueEx(key, "Path")
                        if app_dir not in path_value:
                            new_path = path_value + os.pathsep + app_dir
                            winreg.SetValueEx(key, "Path", 0, winreg.REG_EXPAND_SZ, new_path)
                            print("Added FFmpeg to PATH permanently.")
                        else:
                            print("FFmpeg already in PATH.")
                except Exception as e:
                    print(f"Could not add FFmpeg to PATH permanently: {str(e)}")
                    print("FFmpeg will still work for this session.")
            
            print("FFmpeg installed successfully.")
            return True
            
        except Exception as e:
            print(f"Error extracting FFmpeg: {str(e)}")
            return False

def ensure_ffmpeg():
    """Ensure ffmpeg and ffprobe are available."""
    ffmpeg_found = False
    ffprobe_found = False
    
    # First check if ffmpeg and ffprobe are in PATH
    try:
        # Use subprocess.run with capture_output to suppress console output
        result_ffmpeg = subprocess.run(["ffmpeg", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        ffmpeg_found = result_ffmpeg.returncode == 0
        
        result_ffprobe = subprocess.run(["ffprobe", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        ffprobe_found = result_ffprobe.returncode == 0
        
        if ffmpeg_found and ffprobe_found:
            # print("FFmpeg and FFprobe found in PATH.")
            return True
    except FileNotFoundError:
        # Not in PATH, continue to next checks
        pass
    
    # Check if ffmpeg is in the application directory
    app_dir = get_application_path()
    ffmpeg_path = os.path.join(app_dir, "ffmpeg.exe")
    ffprobe_path = os.path.join(app_dir, "ffprobe.exe")
    
    if os.path.exists(ffmpeg_path) and os.path.exists(ffprobe_path):
        # Add application directory to PATH temporarily
        os.environ["PATH"] = app_dir + os.pathsep + os.environ["PATH"]
        # print(f"Using FFmpeg and FFprobe from application directory: {app_dir}")
        return True
    
    # If we get here, we need to download FFmpeg
    print("FFmpeg and FFprobe not found. Attempting to download...")
    if download_ffmpeg():
        return True
    
    print("FFmpeg and FFprobe are required but could not be installed automatically.")
    print("Please download them manually from: https://ffmpeg.org/download.html")
    return False

def get_video_info(video_path):
    """Get video codec and fps information using ffprobe."""
    try:
        cmd = [
            "ffprobe", 
            "-v", "error", 
            "-select_streams", "v:0", 
            "-show_entries", "stream=codec_name,r_frame_rate", 
            "-of", "json", 
            video_path
        ]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        info = json.loads(result.stdout)
        
        if 'streams' in info and info['streams']:
            stream = info['streams'][0]
            codec = stream.get('codec_name', 'unknown')
            
            # Parse frame rate (which might be in fraction form like "30000/1001")
            r_frame_rate = stream.get('r_frame_rate', 'unknown')
            if r_frame_rate != 'unknown':
                if '/' in r_frame_rate:
                    num, den = map(int, r_frame_rate.split('/'))
                    fps = round(num / den, 3) if den != 0 else 0
                else:
                    fps = float(r_frame_rate)
            else:
                fps = 0
                
            return {
                'codec': codec,
                'fps': fps,
                'original_fps': r_frame_rate,
                'format_key': f"{codec}_{fps}"  # Combined key for codec and fps
            }
        return None
    except Exception as e:
        print(f"Error analyzing {video_path}: {str(e)}")
        return None

def find_most_common_format(video_infos, prefer_h264=False):
    """Find the most common codec and fps combination among the videos."""
    if not video_infos:
        return None, None
    
    # Count combined codec_fps format keys
    format_keys = Counter([info['format_key'] for info in video_infos if info])
    
    if not format_keys:
        return None, None
    
    # Get the most common format key
    most_common_format = format_keys.most_common(1)[0][0]
    most_common_count = format_keys.most_common(1)[0][1]
    # print(f"Most common format: {most_common_format} (count: {most_common_count})")
    
    # Extract codec and fps from the format key
    codec, fps_str = most_common_format.split('_')
    fps = float(fps_str)
    
    # Check if we should prefer H.264 with 29.97 fps
    if prefer_h264 and codec != 'h264' and most_common_count >= 3:
        # print("Prefer H.264 option is enabled. Using H.264 codec with 29.97 fps instead.")
        return 'h264', 29.97
    
    return codec, fps

def sanitize_filename(filename):
    """Sanitize filename to avoid issues with special characters."""
    # Replace problematic characters with underscores
    sanitized = re.sub(r'[\'!]', '_', filename)
    return sanitized

def get_temp_filename(original_path, temp_dir):
    """Generate a temporary filename for re-encoded videos."""
    base_name = os.path.basename(original_path)
    sanitized_name = sanitize_filename(base_name)
    return os.path.join(temp_dir, f"reencoded_{sanitized_name}")

def reencode_video(input_path, output_path, target_codec, target_fps):
    """Re-encode a video to match the target codec and fps."""
    try:
        cmd = [
            "ffmpeg",
            "-hide_banner",
            "-i", input_path,
            "-c:v", target_codec,
            "-r", str(target_fps),
            "-c:a", "aac",  # Always use AAC for audio
            "-y",  # Overwrite output file if it exists
            output_path
        ]
        
        print(f"Re-encoding {os.path.basename(input_path)} to match common format...")
        print(f"Command: {' '.join(cmd)}")
        subprocess.run(cmd, check=True)
        return True
    except Exception as e:
        print(f"Error re-encoding {input_path}: {str(e)}")
        return False

def concatenate_videos(file_list, output_path):
    """Concatenate videos using ffmpeg's concat demuxer."""
    try:
        # Create a temporary file list
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as temp_file:
            for file_path in file_list:
                # Escape single quotes in file paths
                escaped_path = file_path.replace("'", "'\\''")
                temp_file.write(f"file '{escaped_path}'\n")
            temp_file_path = temp_file.name
        
        # Run ffmpeg concat
        cmd = [
            "ffmpeg",
            "-hide_banner",
            "-f", "concat",
            "-safe", "0",
            "-i", temp_file_path,
            "-c:v", "copy",  # Use copy since all videos now have the same format
            "-c:a", "aac",  # Always use AAC for audio
            "-y",  # Overwrite output file if it exists
            output_path
        ]
        
        print(f"\nConcatenating {len(file_list)} videos into {output_path}...")
        print(f"Command: {' '.join(cmd)}")
        subprocess.run(cmd, check=True)
        
        # Clean up
        DEBUG_MODE and cleanup_temp_files(temp_file_path)
        return True
    except Exception as e:
        print(f"Error concatenating videos: {str(e)}")
        DEBUG_MODE and cleanup_temp_files(temp_file_path)
        return False
    
def cleanup_temp_files(temp_file_path):
    if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)
    return True

def get_input_files_interactive():
    """Get input files interactively from user."""
    input_files = []
    print("Enter video file paths (press Enter on an empty line when done):")
    
    # Setup Tab completion
    try:
        if platform.system() == "Windows":
            try:
                # Try to use pyreadline3
                import pyreadline3
                readline = pyreadline3.Readline()
            except ImportError:
                try:
                    # Try to use older pyreadline
                    import pyreadline
                    readline = pyreadline.Readline()
                except ImportError:
                    print("Tab completion not available. Install pyreadline3 for this feature.")
                    readline = None
        else:
            # On Linux/macOS, use built-in readline
            import readline
            readline = readline

        if readline:
            def path_completer(text, state):
                # Handle relative and absolute paths
                if os.path.isabs(text):
                    base_dir = os.path.dirname(text) if text else os.path.sep
                    if not os.path.exists(base_dir):
                        base_dir = os.path.sep
                    search_text = os.path.basename(text)
                else:
                    base_dir = "."
                    search_text = text
                
                try:
                    files = os.listdir(base_dir)
                    matches = [f for f in files if f.startswith(search_text)]
                    
                    if os.path.isabs(text):
                        matches = [os.path.join(os.path.dirname(text), m) for m in matches]
                    
                    for i, match in enumerate(matches):
                        full_path = os.path.join(base_dir, match) if not os.path.isabs(text) else match
                        if os.path.isdir(full_path):
                            matches[i] = os.path.join(match, "")
                    
                    if state < len(matches):
                        return matches[state]
                    return None
                except Exception:
                    return None

            if platform.system() == "Windows":
                readline.set_completer(path_completer)
                readline.parse_and_bind("tab: complete")
            else:
                readline.set_completer(path_completer)
                readline.parse_and_bind("bind ^I rl_complete")
            
            #print("Tab completion enabled. Press Tab to complete filenames.")
        else:
            #print("You can use Tab in terminal to complete filenames.")
            pass

    except Exception as e:
        #print(f"Tab completion not available ({str(e)}). You can still enter file paths manually.")
        print(traceback.print_exc())
    # Get user input
    while True:
        try:
            file_input = input("> ").strip()
            if not file_input:
                break
                
            # Remove quotes if present
            file_input = file_input.strip('"\'')
            
            if os.path.exists(file_input):
                input_files.append(os.path.abspath(file_input))
            else:
                print(f"File not found: {file_input}")
        except KeyboardInterrupt:
            print("\nInput interrupted.")
            break
    
    return input_files

def get_output_file_interactive():
    """Get output file path interactively from user."""
    # output_file = input("\nEnter output file path (default: output.mp4): ").strip() or "output.mp4"
    print("output file path default: output.mp4")
    output_file = "output.mp4"
    output_file = output_file.strip('"\'')
    return output_file

def get_main_parser():
    parser = argparse.ArgumentParser(prog="vconcat",description="V-CONCAT Advanced Video Concatenation Tool")
    shtab.add_argument_to(parser, ["-s", "--print-completion"]) # magic!

    # file & directory tab complete

    return parser
def parse_arguments():
    """Parse command line arguments."""
    parser = get_main_parser()
    parser.add_argument("input_files", nargs="*", help="Input video files to concatenate").complete = shtab.FILE
    parser.add_argument("-o", "--output", help="Output file path (default: output.mp4)")
    parser.add_argument("-i", "--interactive", action="store_true", help="Use interactive mode even if files are provided")
    parser.add_argument("--prefer-h264", "-ph4", action="store_true", help="Prefer H.264 codec with 29.97 fps when most common format is different")
    parser.add_argument("--no-encode", action="store_true", help="Disable re-encoding completely, just concatenate files as they are")
    return parser.parse_args()

def main():
    """Main function to run the video concatenation tool."""
    
    print_banner()
    
    if not ensure_ffmpeg():
        input("Press Enter to exit...")
        return
    
    # Load configuration from file
    config = load_config()
    
    # Parse command line arguments
    args = parse_arguments()
    
    # Check if no-encode is enabled (command line takes precedence over config)
    no_encode = args.no_encode or config.get('no_encode', False)
    
    # Merge configuration with command line arguments
    # Command line arguments take precedence over config file
    # If no-encode is enabled, prefer_h264 is disabled
    prefer_h264 = False if no_encode else (args.prefer_h264 or config.get('prefer_h264', False))
    
    # Get input files
    input_files = []
    if args.input_files and not args.interactive:
        # Use files provided as command line arguments
        for file_path in args.input_files:
            if os.path.exists(file_path):
                input_files.append(os.path.abspath(file_path))
            else:
                print(f"File not found: {file_path}")
    else:
        # Get files interactively
        input_files = get_input_files_interactive()
    
    if not input_files:
        print("No valid input files provided. Exiting.")
        input("Press Enter to exit...")
        return
    
    # Get output file path
    if args.output and not args.interactive:
        output_file = args.output
    else:
        output_file = get_output_file_interactive()
    
    # Analyze all videos
    print("\nAnalyzing video files...")
    video_infos = []
    for file_path in input_files:
        print(f"Analyzing {os.path.basename(file_path)}...")
        info = get_video_info(file_path)
        if info:
            info['path'] = file_path
            video_infos.append(info)
            print(f"  - Codec: {info['codec']}, FPS: {info['fps']}")
        else:
            print(f"  - Failed to analyze {file_path}")
    
    if not video_infos:
        print("No valid video files to process. Exiting.")
        input("Press Enter to exit...")
        return
    
    # Count format keys
    format_keys = Counter([info['format_key'] for info in video_infos if info])
    
    # Find most common format (even if we're not re-encoding, we need to know the target format)
    most_common_format = format_keys.most_common(1)[0][0]
    target_codec, target_fps_str = most_common_format.split('_')
    target_fps = float(target_fps_str)
    
    # Check if no-encode is enabled and there are different formats
    if no_encode:
        if len(format_keys) > 1:
            if platform.system() == "Windows":
                os.system('cls')
            else:
                os.system('clear')
            print("\nWARNING: Multiple video formats detected but --no-encode is enabled.\n")
            print(f"\033[34m============== Most common format =============\033[0m")
            print(f" - Codec= \033[32m{target_codec}\033[0m")
            print(f" - FPS= \033[32m{target_fps}\033[0m")
            print(f"\n\033[33m======== Videos with different formats ========\033[0m\n")
            
            # List videos with different formats
            for info in video_infos:
                if info['codec'] != target_codec or abs(info['fps'] - target_fps) > 0.001:
                    print(f"  * \033[38;5;203m{os.path.basename(info['path'])}\033[0m  << Codec = : \033[38;5;215m{info['codec']}\033[0m, FPS = \033[38;5;215m{info['fps']}\033[0m")
            # Ask user if they want to continue
            print("\nContinuing without re-encoding may cause playback issues.")
            user_choice = input("Do you want to continue? (y/n): ").strip().lower()
            
            if user_choice != 'y' and user_choice != 'yes':
                print("Operation cancelled by user.")
                return
            
            print("\nContinuing with concatenation without re-encoding...")
        else:
            print("\nNo re-encoding needed. All videos have the same format.")
        
        # Create a temporary file list for concatenation
        with tempfile.TemporaryDirectory() as temp_dir:
            # Concatenate all videos without re-encoding
            if concatenate_videos([info['path'] for info in video_infos], output_file):
                print(f"\nSuccess! Concatenated video saved to: {output_file}")
            else:
                print("\nFailed to concatenate videos.")
        
        input("\nPress Enter to exit...")
        return
    
    # If we get here, we're re-encoding
    # Find most common format with prefer_h264 option
    target_codec, target_fps = find_most_common_format(video_infos, prefer_h264)
    print(f"\nMost common format: Codec={target_codec}, FPS={target_fps}")
    
    # Create temporary directory for re-encoded files
    with tempfile.TemporaryDirectory() as temp_dir:
        final_file_list = []
        
        # Process each video
        for info in video_infos:
            if info['codec'] == target_codec and abs(info['fps'] - target_fps) < 0.001:
                # No need to re-encode
                print(f"{os.path.basename(info['path'])} already matches target format.")
                final_file_list.append(info['path'])
            else:
                # Need to re-encode
                print(f"{os.path.basename(info['path'])} needs re-encoding:")
                print(f"  - Current: Codec={info['codec']}, FPS={info['fps']}")
                print(f"  - Target: Codec={target_codec}, FPS={target_fps}")
                
                temp_output = get_temp_filename(info['path'], temp_dir)
                if reencode_video(info['path'], temp_output, target_codec, target_fps):
                    final_file_list.append(temp_output)
                else:
                    print(f"Skipping {os.path.basename(info['path'])} due to re-encoding failure.")
        
        # Concatenate all videos
        if final_file_list:
            if concatenate_videos(final_file_list, output_file):
                print(f"\nSuccess! Concatenated video saved to: {output_file}")
            else:
                print("\nFailed to concatenate videos.")
        else:
            print("\nNo videos to concatenate after processing.")
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main() 
