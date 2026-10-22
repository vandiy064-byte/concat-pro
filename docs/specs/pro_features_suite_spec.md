# SPECIFICATION: 5 ADVANCED PRO EDITING SUITE FOR CONCAT

## 1. Mục tiêu & Phạm vi
Triển khai trọn bộ 5 tính năng chỉnh sửa video chuyên nghiệp theo chuẩn CapCut & TikTok cho Concat:
1. **Karaoke Subtitles (Word-by-Word)**: Phụ đề nhảy chữ theo từng từ với hiệu ứng phóng to/đổi màu nổi bật.
2. **Auto Silence Removal**: Tự động phát hiện và cắt bỏ các khoảng lặng > 0.5s trên timeline bằng RMS/VAD.
3. **Script-to-Video Engine**: Tự động dựng video hoàn chỉnh từ file kịch bản văn bản.
4. **Smart Reframing (16:9 -> 9:16)**: Tự động chuyển đổi video ngang thành video dọc và bám khung hình chủ thể.
5. **CapCut Draft Converter**: Cầu nối chuyển đổi dự án hai chiều giữa Concat và CapCut PC (`draft_content.json`).

---

## 2. Kiến trúc & Thiết kế kỹ thuật

### Tính năng 1: Word-by-Word Karaoke Subtitles
* **Input**: File âm thanh/video hoặc chuỗi timestamp từ Whisper word-level timestamps (`[{"word": "Xin", "start": 0.1, "end": 0.4}, ...]`).
* **Hiệu ứng**:
  * Phong cách Hormozi: Khung câu đầy đủ hiển thị chữ trắng/mờ; từ đang được đọc đổi sang màu Vàng Neon (`#FFE500`) hoặc Xanh Neon (`#00FF66`), viền đen dày, phóng to 115%.
* **Output**:
  * Timeline Text Clips đồng bộ thời gian.
  * Xuất file ASS / SubRip hỗ trợ Karaoke tags (`{\k}`).

### Tính năng 2: Auto Silence / Jump-Cut Removal
* **Thuật toán**: Voice Activity Detection (VAD) kết hợp ngưỡng năng lượng RMS (dBFS) trên PCM 16kHz mono.
* **Tham số**:
  * `silence_threshold_db`: Mặc định `-35 dB`.
  * `min_silence_duration`: Mặc định `0.5s`.
  * `padding_duration`: Mặc định `0.08s` (đệm trước và sau mỗi từ để tránh bị cụt giọng).
* **Output**: Danh sách khoảng thời gian giữ lại `keep_ranges = [(start, end), ...]`. Tự động ripple-cut timeline.

### Tính năng 3: Script-to-Video Engine
* **Input**: File văn bản `kịch_bản.txt` hoặc `.md` kèm thư mục media (B-roll ảnh/video) và nhạc nền.
* **Pipeline**:
  1. Phân tách câu bằng NLP regex.
  2. Tạo audio TTS từng câu (qua engine Sherpa-ONNX / Edge-TTS tiếng Việt).
  3. Tính toán vị trí timeline liên tiếp, thêm phụ đề tương ứng.
  4. Chèn B-roll lấp đầy timeline video.
  5. Thêm track nhạc nền, tự động ducking (giảm âm lượng xuống -16dB khi có giọng đọc).
* **Output**: Dự án Concat hoàn chỉnh sẵn sàng phát preview hoặc xuất video.

### Tính năng 4: Smart Reframing (16:9 -> 9:16)
* **Input**: Video 16:9 (1920x1080).
* **Output**: Dự án 9:16 (1080x1920).
* **Cơ chế**:
  * Scale factor = `1920 / 1080` (1.7778x).
  * Thuật toán quét vị trí khuôn mặt / vùng chuyển động chính ở mỗi đoạn (hoặc chia đều khung hình).
  * Đặt keyframes `offset_x` mượt mà (smooth interpolation) để chủ thể luôn nằm trong 1/3 chính giữa khung hình.

### Tính năng 5: CapCut Draft Converter
* **CapCut Format**: Thư mục dự án CapCut PC chứa `draft_content.json` và `draft_meta_info.json`.
  * `tracks`: danh sách các track (`video`, `audio`, `text`).
  * `materials`: danh sách video, audio, text với font, style, animation.
* **Cơ chế chuyển đổi**:
  * Đọc `project.json` của Concat -> ánh xạ clips, tracks, transitions sang `draft_content.json` của CapCut.
  * Tự động tạo thư mục dự án trong `%LOCALAPPDATA%\CapCut\User Data\Projects\com.lveditor.draft\...` để khi mở CapCut là thấy ngay dự án!

---

## 3. Kế hoạch triển khai & Kiểm thử
1. Triển khai các API endpoints trong Concat Rust crates (`concat-api`, `concat-mcp`).
2. Xây dựng bộ công cụ điều khiển Studio Automation (`e:\concat\tools\`) bằng Python hỗ trợ gọi trực tiếp qua CLI / GUI / Batch file.
3. Viết Unit Test và Integration Test kiểm tra toàn bộ 5 tính năng.
