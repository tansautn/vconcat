### VCONCAT - Video Concatenation Tool  

## Introduction  
VCONCAT is a simple command-line tool designed to merge multiple videos into a single video as FAST as possible.  

## Quick Usage  
1. Download the `concat.cmd` file.  
2. Double-click to run the file.  
3. The tool will automatically:  
   - Check and download FFmpeg if it's not installed.  
   - Add FFmpeg to the system PATH.  
4. Enter the file paths of the videos to be merged:  
   - Use TAB for auto-completing file names.  
   - Press Enter after each file.  
   - Press Enter (without input) to start the merging process.  
5. The output file will be saved as `output.mp4`.  

## Important Notes  
- Input videos SHOULD have the same encoding parameters (fps, resolution, etc.) to ensure output quality.  
- The tool uses the following FFmpeg command:  
  ```sh
  ffmpeg -f concat -safe 0 -i filelist.txt -c:v copy -c:a aac output.mp4
  ```  
- Always check the output file to ensure quality.  

## Contact  
**Author:** Zuko (tansautn@gmail.com)  