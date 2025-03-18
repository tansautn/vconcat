# V-CONCAT | Advanced Video Concatenation Tool

** Phiên bản Advanced (Python) **

Công cụ này giúp bạn gộp nhiều video thành một video duy nhất, tự động xử lý các video có codec và fps khác nhau.

## Tính năng

- Phân tích thông tin codec và fps của tất cả các video đầu vào
- Tự động xác định codec và fps phổ biến nhất trong các video đầu vào (xử lý theo cặp codec_fps)
- Tự động re-encode các video có codec hoặc fps khác với định dạng phổ biến nhất
- Xử lý tên file có chứa ký tự đặc biệt như `'` và `!`
- Gộp tất cả các video lại với nhau thành một file duy nhất
- Hỗ trợ kéo thả file video vào script để xử lý nhanh chóng
- Tự động tải FFmpeg nếu chưa được cài đặt
- Hỗ trợ Tab completion khi nhập tên file
- Tùy chọn ưu tiên sử dụng codec H.264 với fps 29.97
- Hỗ trợ file cấu hình để lưu các tùy chọn mặc định
- Tùy chọn bỏ qua re-encode để gộp nhanh các video

## Yêu cầu

### Để chạy từ source code:
- Python 3.6 trở lên
- FFmpeg và FFprobe (sẽ được tự động tải nếu chưa cài đặt)

### Để chạy từ file .exe:
- Không cần cài đặt gì thêm, tất cả đã được đóng gói trong file .exe

## Cách hoạt động

1. Script sẽ phân tích tất cả các video đầu vào để xác định codec và fps của từng file
2. Xác định cặp codec+fps phổ biến nhất trong các video đầu vào (đảm bảo chọn định dạng thực tế tồn tại)
3. Các video có codec hoặc fps khác với định dạng phổ biến nhất sẽ được re-encode
4. Tất cả các video (cả nguyên gốc và đã re-encode) sẽ được gộp lại thành một file duy nhất

## Cách sử dụng

### Sử dụng file .exe (Khuyến nghị cho người dùng Windows)

#### Cách 1: Chạy trực tiếp
1. Chỉ cần chạy file `vconcat.exe` hoặc `vconcat.cmd` bằng cách double-click
2. Nhập đường dẫn đến các file video cần gộp (nhấn Enter sau mỗi file)
   - Bạn có thể sử dụng phím Tab để tự động hoàn thành tên file
   - Ví dụ: Gõ một phần tên file và nhấn Tab để hoàn thành
3. Khi đã nhập xong tất cả các file, nhấn Enter trên một dòng trống
4. Nhập tên file output (hoặc để trống để sử dụng tên mặc định `output.mp4`)
5. Chờ quá trình phân tích và gộp video hoàn tất

#### Cách 2: Kéo thả file
1. Chọn tất cả các file video cần gộp
2. Kéo và thả chúng vào file `vconcat.cmd` hoặc `vconcat.exe`
3. Công cụ sẽ tự động phân tích và gộp các video thành file `output.mp4`

### Sử dụng script Python

#### Cách 1: Chạy trực tiếp
1. Chỉ cần chạy file `vconcat.cmd` bằng cách double-click
2. Nhập đường dẫn đến các file video cần gộp (nhấn Enter sau mỗi file)
   - Bạn có thể sử dụng phím Tab để tự động hoàn thành tên file
   - Ví dụ: Gõ một phần tên file và nhấn Tab để hoàn thành
3. Khi đã nhập xong tất cả các file, nhấn Enter trên một dòng trống
4. Nhập tên file output (hoặc để trống để sử dụng tên mặc định `output.mp4`)
5. Chờ quá trình phân tích và gộp video hoàn tất

#### Cách 2: Kéo thả file
1. Chọn tất cả các file video cần gộp
2. Kéo và thả chúng vào file `vconcat.cmd`
3. Công cụ sẽ tự động phân tích và gộp các video thành file `output.mp4`

### Sử dụng dòng lệnh

```
vconcat.cmd [file1.mp4 file2.mp4 ...] [-o output.mp4] [-i]
```

hoặc

```
python vconcat.py [file1.mp4 file2.mp4 ...] [-o output.mp4] [-i]
```

hoặc (nếu sử dụng file .exe)

```
vconcat.exe [file1.mp4 file2.mp4 ...] [-o output.mp4] [-i]
```

Các tùy chọn:
- `file1.mp4 file2.mp4 ...`: Danh sách các file video cần gộp
- `-o, --output`: Đường dẫn đến file output (mặc định: `output.mp4`)
- `-i, --interactive`: Sử dụng chế độ tương tác ngay cả khi đã cung cấp file qua dòng lệnh
- `--prefer-h264, -ph4`: Ưu tiên sử dụng codec H.264 với fps 29.97 khi định dạng phổ biến nhất khác H.264 và có ít nhất 3 video
- `--no-encode`: Bỏ qua quá trình re-encode, gộp trực tiếp các video. Nếu phát hiện các video có định dạng khác nhau, công cụ sẽ hiển thị cảnh báo và hỏi người dùng có muốn tiếp tục không.

## File cấu hình

Công cụ hỗ trợ tải cấu hình từ file `vconcat.conf` trong thư mục của ứng dụng. File này sử dụng định dạng JSON và có thể chứa các tùy chọn sau:

```json
{
    "prefer_h264": true,
    "no_encode": false,
    "comment": "This is a configuration file for V-CONCAT. Set prefer_h264 to true to always prefer H.264 codec with 29.97 fps when possible. Set no_encode to true to skip re-encoding completely."
}
```

Các tùy chọn trong file cấu hình:
- `prefer_h264`: Khi đặt là `true`, công cụ sẽ ưu tiên sử dụng codec H.264 với fps 29.97 khi định dạng phổ biến nhất khác H.264 và có ít nhất 3 video
- `no_encode`: Khi đặt là `true`, công cụ sẽ bỏ qua quá trình re-encode và gộp trực tiếp các video. Nếu phát hiện các video có định dạng khác nhau, công cụ sẽ hiển thị cảnh báo và hỏi người dùng có muốn tiếp tục không. (tùy chọn này sẽ vô hiệu hóa `prefer_h264`)

Lưu ý: Các tùy chọn dòng lệnh sẽ ghi đè lên các tùy chọn trong file cấu hình.

## Ví dụ sử dụng

### Gộp 3 video với codec và fps khác nhau
```
vconcat.cmd video1.mp4 video2.avi video3.mov -o final_video.mp4
```

### Gộp các video trong thư mục hiện tại có tên bắt đầu bằng "scene"
```
vconcat.cmd scene*.mp4
```

### Gộp các video và ưu tiên sử dụng codec H.264
```
vconcat.cmd video1.mp4 video2.avi video3.mov --prefer-h264
```

### Gộp các video mà không re-encode (nhanh hơn)
```
vconcat.cmd video1.mp4 video2.mp4 video3.mp4 --no-encode
```

## Cách build file .exe

Nếu bạn muốn tạo file .exe từ source code, bạn có thể sử dụng script `build.py`:

```
python build.py
```

Script này sẽ:
1. Kiểm tra và cài đặt PyInstaller nếu cần
2. Build file .exe từ script Python
3. Tạo file launcher script `vconcat.cmd` trong thư mục `dist`
4. Sao chép file README.md vào thư mục `dist`

Sau khi build xong, bạn có thể tìm thấy file .exe và các file liên quan trong thư mục `dist`.

## Cải tiến so với phiên bản lite (CMD)

1. **Xử lý codec và fps theo cặp**: Phiên bản mới xác định định dạng phổ biến nhất dựa trên cặp codec+fps, đảm bảo chọn định dạng thực tế tồn tại trong các video đầu vào.

2. **Tự động tải FFmpeg**: Nếu FFmpeg chưa được cài đặt, công cụ sẽ tự động tải và cài đặt.

3. **Tab completion**: Hỗ trợ Tab completion khi nhập tên file, giúp việc nhập đường dẫn file dễ dàng hơn.

4. **Xử lý ký tự đặc biệt**: Xử lý tên file có chứa ký tự đặc biệt như `'` và `!`.

5. **Giao diện thân thiện**: Giao diện dòng lệnh trực quan và dễ sử dụng.

6. **File .exe độc lập**: Có thể tạo file .exe độc lập để sử dụng mà không cần cài đặt Python.

7. **Ưu tiên H.264**: Tùy chọn ưu tiên sử dụng codec H.264 với fps 29.97 để đảm bảo tương thích tốt nhất với các thiết bị phổ biến.

8. **File cấu hình**: Hỗ trợ file cấu hình để lưu các tùy chọn mặc định.

9. **Chế độ không re-encode**: Tùy chọn bỏ qua quá trình re-encode để gộp nhanh các video khi cần thiết.

## Lưu ý

- Quá trình re-encode có thể mất thời gian tùy thuộc vào kích thước và số lượng video
- Các file tạm thời được tạo ra trong quá trình re-encode sẽ tự động bị xóa sau khi hoàn tất
- Nếu bạn gặp lỗi, hãy đảm bảo rằng Python đã được cài đặt đúng cách (nếu chạy từ source code)
- Khi sử dụng file .exe, có thể sẽ mất một chút thời gian để khởi động lần đầu tiên

## Tác giả

Zuko [tansautn@gmail.com] 