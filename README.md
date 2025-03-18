<a href="http://zuko.pro/">
    <img src="https://avatars0.githubusercontent.com/u/6666271?v=3&s=96" alt="Z-Logo"
         title="Halu Universe" align="right" />
</a>
# VCONCAT

# :film_strip: VCONCAT Project - Video Concatenation Tool :film_strip:

## Công cụ gộp nhiều video thành một video
VCONCAT là project open-source cung cấp giải pháp đơn giản để merge video files tiết kiệm thời gian nhất có thể, sử dụng FFmpeg làm core engine.

Built binaries chỉ có sẵn trên Windows. Do vợ tôi chỉ dùng windows :upside_down_face:

Có 2 phiên bản: [LITE](./README.cmd.md) và [ADVANCED](./README.py.md).
Phiên bản LITE nhắm tới tính đơn giản và nhanh chóng. Chỉ cần duy nhất một thao tác download và chạy file là có thể gộp video.

Phiên bản ADVANCED được ra đời nhằm cải thiện một số vấn đề tồn tại của phiên bản LITE:
- Xử lý source-conflicts như codecs, fps, resolution, etc
- không hỗ trợ các kí tự đặc biệt trong filename. Ví dụ `!`, `'`
  
>> lý do có thằng thứ hai là team vợ tôi mới tuyển đc ổng editor. Ổng export video dùng Capcut. Codec `HEVC/FPS 30.0`. Trong khi toàn team xuất `H264/FPS 29.97`.
>> 
>>Vợ là nhất mà :snowflake:

## Overview in English
VCONCAT is an open-source project that provides a simple solution for merging video files as efficiently as possible, using FFmpeg as the core engine.  

Built binaries are only available on Windows. Because my wife only uses Windows. 😆  

There are two versions: **LITE** and **ADVANCED**.  
The **LITE** version focuses on simplicity and speed. Just one download (**script < 10kb**) and running the file is enough to merge videos.  

The **ADVANCED** version was created to address some of the limitations of the LITE version:  
- Handles source conflicts such as codecs, fps, resolution, etc.  
- Does not support special characters in filenames (e.g., `!`, `'`).  

## Quick Usage  
- Download the `concat.cmd` (LITE version) or `concat.exe` (ADVANCED version).  
- Run the file.  
- Follow the instructions in the console window.  

## Features  
- Auto-download and configure FFmpeg.  
- TAB completion support for filenames.  
- Preserve video quality through stream copying.  
- Cross-platform compatibility (Windows).  
- Minimal dependencies.  

## TODO
- [ ] Add Explorer context menu for quick access
- [ ] Mutil-selection DROP-DRAG support
- [ ] Same as from context menu
## Technical Details  

### Dependencies  
- FFmpeg (auto-downloaded if not installed).  
- Windows PowerShell (to download and extract FFmpeg).  

### Core Components  
1. **FFmpeg Integration**  
   - Auto-downloads from official FFmpeg builds.  
   - Configures PATH environment variables.  
   - Uses stream copying to preserve quality.  

2. **File Handling**  
   - Input validation.  
   - Absolute path conversion.  
   - Special character handling.  

3. **User Interface**  
   - ASCII art logo.  
   - Interactive command prompt.  
   - Progress feedback.  

## Development Guide  

### Project Structure  
```
vconcat/
├── concat.cmd        # LITE Main executable
├── README.md         # Developer documentation
├── README.cmd.md     # User guide
├── README.py.md      # User guide
├── llms.txt          # LLM prompt
├── vconcat.py        # ADVANCED Main executable
├── build.py          # pyInstaller build script (for ADVANCED version)

```  

### Contributing  
1. Fork the repository.  
2. Create a feature branch.  
3. Commit changes.  
4. Submit a pull request.  

### Coding Standards  
- Maintain clear error handling.  
- Add comments for complex logic.  
- Follow batch script best practices.  
- Test across multiple Windows versions.  

### Testing  
Test the following scenarios:  
- FFmpeg installation process.  
- File path handling.  
- Special character handling.  
- Different video formats.  
- Error conditions.  

## License  
MIT License  

## Contact  
- **Author:** Zuko  
- **Email:** tansautn@gmail.com  
