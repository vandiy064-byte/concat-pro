# SPECIFICATION: Redesigned Video Export Interface & Permanent SRT Subtitle Section

## 1. Yêu cầu & Vấn đề thực tế (Problem Statement)
Người dùng gửi ảnh chụp giao diện cửa sổ "Xuất" (Export Dialog) và đưa ra 2 câu hỏi/yêu cầu:
1. *"Tại sao không thấy phần xuất file srt ở trong phần xuất video này?"*
2. *"Thiết kế lại phần giao diện xuất video này"*

### Phân tích nguyên nhân (Root Cause):
- Trong bản code trước, tùy chọn xuất SRT trong [`export.slint`](file:///e:/concat/Concat-main/src/crates/concat/ui/dialogs/export.slint) bị bao bọc bởi điều kiện `if root.data.has-subtitles:`.
- Khi người dùng mở một dự án mới (ví dụ `Untitled project 5` trong ảnh chụp với `0 clips`, `0:00 duration`), `has-subtitles` bằng `false`.
- Do đó, khối tùy chọn xuất SRT hoàn toàn bị ẩn đi, khiến người dùng không tìm thấy tính năng và tưởng rằng app chưa có tính năng này.
- Bố cục 3 cột hiện tại chưa cân đối: cột 1 (Preview + Summary), cột 2 (Output settings dài), cột 3 (chỉ có Destination ngắn và nhiều khoảng trống thừa).

## 2. Mục tiêu thiết kế mới (Design Goals)
1. **Phần Phụ đề & SRT luôn luôn hiển thị (Always Visible Subtitles & SRT Section)**:
   - Tạo một thẻ giao diện chuyên biệt `SubtitlesSection` riêng biệt, không ẩn đi kể cả khi timeline chưa có clip.
   - Thể hiện trạng thái phụ đề rõ ràng:
     - Khi có phụ đề: Huy hiệu xanh `✓ Đã phát hiện phụ đề trên dòng thời gian` (`Theme.green`).
     - Khi chưa có phụ đề: Huy hiệu ghi chú `(i) Chưa có phụ đề trên dòng thời gian` kèm hướng dẫn rõ ràng.
   - Luôn hiển thị công tắc: *"Xuất kèm tệp phụ đề (.srt) cùng video"*.
   - Luôn hiển thị nút bấm hành động: *"Xuất tệp phụ đề (.srt) riêng ngay"*.
2. **Thiết kế lại giao diện hiện đại, chuyên nghiệp, sang trọng (Rich Aesthetic Redesign)**:
   - Sử dụng thẻ Card hiện đại (`border-radius: 8px`, `background: Theme.raised`, đường viền `Theme.line`).
   - Tiêu đề từng khu vực có biểu tượng (Icon) trực quan:
     - 🎬 **Xem trước & Tóm tắt** (Preview & Summary)
     - ⚙️ **Cấu hình Video & Bộ mã hóa** (Video & Encoder Settings)
     - 📝 **Phụ đề & Bản chép lời (.SRT)** (Subtitles & SRT) - Có viền ánh tím/xanh nổi bật
     - 📁 **Vị trí lưu & Đặt tên tệp** (Destination & File Name)
   - Bố cục cân đối ở cả 3 kích thước:
     - Màn hình rộng (3 cột):
       - Cột 1: PreviewSection + SummarySection
       - Cột 2: OutputSection (Video codec, resolution, bitrate, 10-bit)
       - Cột 3: DestinationSection + SubtitlesSection (Tạo sự cân xứng hoàn hảo, lấp đầy khoảng trống)
     - Màn hình trung bình (2 cột):
       - Cột 1: Preview + Summary + Destination
       - Cột 2: Output + Subtitles
     - Màn hình nhỏ (1 cột):
       - Summary -> Destination -> Subtitles -> Output
3. **Thanh chân trang (Footer)**:
   - Nút Xuất nổi bật, hiển thị dung lượng ước tính.
   - Nút xuất SRT riêng biệt tiện lợi.

## 3. Kế hoạch triển khai
1. Cập nhật chuỗi đa ngôn ngữ trong `locales/vi.json` và `locales/en.json`.
2. Tái cấu trúc component `export.slint` với `SubtitlesSection` chuyên biệt.
3. Cập nhật `src/crates/concat/src/panes/export.rs` để xử lý callback và trạng thái khi nhấn xuất SRT.
4. Nâng version lên `2.0.11` để CI tự động phát hành bản Release mới có giao diện hoàn chỉnh.
