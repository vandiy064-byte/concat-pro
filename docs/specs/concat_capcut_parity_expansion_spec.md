# SPECIFICATION: CONCAT CAPCUT PARITY EXPANSION SUITE

## 1. Mục tiêu & Phạm vi
Triển khai trọn bộ các tính năng còn thiếu so với CapCut nhằm đưa Concat đạt 100% độ tương đương kỹ thuật về khả năng dựng video ngắn (Shorts / TikTok / Reels):
1. **Audio Vocal Isolation & Noise Reduction**: Tách lời bài hát, tách beat nhạc nền và khử ồn giọng nói.
2. **Built-in Sound Effects (SFX) Library**: Kho hiệu ứng âm thanh dựng phim (Whoosh, Ding, Pop, Glitch, Applause...).
3. **Animated Text Presets Engine**: 8 mẫu hoạt ảnh chữ chuyển động kinh điển của CapCut (Typewriter, ZoomBounce, NeonGlow, Wave, Glitch...).
4. **Face Beauty & Skin Retouching**: Bộ lọc nhận diện vùng da làm mịn tự nhiên, sáng da nhưng giữ nguyên độ nét của mắt, môi, tóc.
5. **Typography & Styling Presets**: Bộ tạo kiểu chữ phụ đề bắt mắt chuẩn hóa tiếng Việt.

---

## 2. Kiến trúc & Chi tiết Kỹ thuật

### A. Module 1: Vocal Isolation & Denoise Engine (`vocal_separator.py`)
* **Input**: File âm thanh / video track.
* **Modes**:
  * `vocal`: Giữ lại giọng nói/giọng hát, loại bỏ hoàn toàn nhạc nền.
  * `instrumental`: Tách lấy beat nhạc nền (karaoke), xóa giọng ca sĩ.
  * `denoise`: Lọc sạch tiếng quạt, gió, tạp âm nền (spectral noise gating).
* **Phương pháp**:
  * Spectral Subtraction & Harmonic-Percussive Separation kết hợp RMS gating.
  * Hỗ trợ xuất trực tiếp ra file WAV 48kHz stereo chất lượng phòng thu.

### B. Module 2: Built-in Sound Effects Library (`sfx_library.py`)
* **Thư mục**: `e:/concat/assets/sfx/`
* **Danh mục SFX thiết yếu**:
  1. `whoosh_fast.wav`: Hiệu ứng vút gió chuyển cảnh.
  2. `ding_notification.wav`: Chuông ting khi xuất hiện chữ/icon.
  3. `pop_bubble.wav`: Tiếng pop nảy chữ sinh động.
  4. `glitch_digital.wav`: Tiếng rẹt rẹt kỹ thuật số.
  5. `camera_click.wav`: Tiếng tách máy ảnh chụp hình.
  6. `applause_cheer.wav`: Tiếng vỗ tay tán thưởng.
  7. `transition_impact.wav`: Tiếng bass đập mạnh khi chuyển đoạn.
* **Tính năng**: Tự động chèn SFX vào timeline đúng các điểm chuyển cảnh (cut points) hoặc điểm phụ đề xuất hiện.

### C. Module 3: Animated Text Presets Engine (`text_animator.py`)
* **Danh sách 8 Presets**:
  1. `Typewriter`: Đánh máy từng ký tự theo thời gian phát âm.
  2. `ZoomBounce`: Từ kích thước 0.7x phóng vọt lên 1.15x rồi nảy nhẹ về 1.0x trong 0.25s đầu.
  3. `FadeSlideUp`: Độ mờ từ 0% lên 100%, đồng thời trượt từ dưới lên vị trí chuẩn.
  4. `NeonGlow`: Chữ đổi màu chu kỳ và chớp nháy viền neon.
  5. `WavePulse`: Hiệu ứng co giãn nhịp nhàng theo biên độ âm thanh.
  6. `GlitchShake`: Rung lắc nhẹ ngẫu nhiên tọa độ `offset_x`/`offset_y` trong 3 frame.
  7. `CinematicFade`: Mờ dần vào và ra chậm rãi, trang nhã.
  8. `HormoziPop`: Viền đen siêu đậm 6px, chữ vàng neon `#FFE500`, đổi màu khi đọc.
* **Cơ chế**: Tự động sinh mảng keyframes chuẩn xác (`time`, `value`, `ease`) đặt thẳng vào `Clip.keyframes` trong Concat.

### D. Module 4: Face Beauty & Skin Retouch (`beauty_filter.py`)
* **Thuật toán**:
  * Phân đoạn vùng da mặt bằng không gian màu $YC_bC_r$ / $HSV$ để bảo vệ vùng mắt, lông mày, răng và tóc.
  * Áp dụng bộ lọc song phương (Bilateral Filter / Surface Blur) chỉ trên mặt nạ da để làm mờ vết mụn, lỗ chân lông mà không làm mờ nét cạnh.
  * Tăng nhẹ độ sáng (Luminance gamma 1.05 - 1.10) và độ tương phản tự nhiên.

### E. Module 5: Typography Presets (`typography_presets.py`)
* 5 Phong cách chữ có sẵn:
  * `TikTokViral`: Font Montserrat ExtraBold, chữ hoa, viền đen dày, màu vàng hoặc trắng.
  * `CinematicModern`: Font Serif/Sans thanh mảnh, chữ thường, khoảng cách chữ rộng (letter-spacing), bóng đổ mờ.
  * `NewsBreaking`: Nền hộp chữ nhật đỏ/vàng, chữ trắng đậm góc cạnh.
  * `RetroVaporwave`: Chữ hồng neon tím pastel, bóng kép đổ lệch.
  * `MinimalistClean`: Chữ trắng đơn sắc, nền mờ kính mờ (glassmorphism).

---

## 3. Kế hoạch triển khai & Kiểm thử
1. Triển khai 5 module Python độc lập, chuẩn Clean Code trong `e:/concat/tools/`.
2. Tạo các mẫu âm thanh SFX chuẩn trong `e:/concat/assets/sfx/`.
3. Tích hợp các lệnh gọi API mới vào `concat-api` và `concat-mcp`.
4. Cập nhật menu `studio_pro.py` và `Studio_Pro_Tools.bat`.
5. Viết bộ Unit Test kiểm tra toàn bộ 5 module và chạy kiểm thử tự động.
