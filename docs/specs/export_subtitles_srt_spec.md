# SPECIFICATION: TÍNH NĂNG XUẤT VIDEO KÈM PHỤ ĐỀ SRT TRONG EXPORT DIALOG

## 1. Mục tiêu & Bối cảnh
Người dùng cần khả năng xuất file phụ đề SRT trực tiếp từ thẻ/hộp thoại Xuất video (Export Dialog):
1. **Xuất kèm phụ đề tự động**: Khi xuất video (MP4/HEVC/AV1), nếu timeline có chứa phụ đề / title clips, Concat cho phép người dùng bật tùy chọn xuất kèm file phụ đề `.srt` cùng tên và cùng thư mục với video xuất (ví dụ: `my_video.mp4` đi kèm `my_video.srt`).
2. **Xuất nhanh phụ đề SRT ngay tại Export Dialog**: Cung cấp nút thao tác nhanh "Chỉ xuất tệp phụ đề (.srt)" ngay trong hộp thoại Export, giúp người dùng không cần phải thoát ra mở riêng hộp thoại Captions mới xuất được file phụ đề.

---

## 2. Thiết kế Kiến trúc & Kỹ thuật

### A. Giao diện người dùng (Slint UI)
* **File**: `src/crates/concat/ui/dialogs/export.slint` & `src/crates/concat/ui/app.slint`
* **ExportData cập nhật**:
  * `has-subtitles: bool`: `true` nếu trên timeline có ít nhất 1 clip phụ đề (Text Clip).
  * `export-subtitles: bool`: Trạng thái bật/tắt tùy chọn xuất kèm phụ đề SRT (mặc định `true` nếu có phụ đề).
  * `written-srt: string`: Tên file SRT đã được xuất thành công kèm theo video để thông báo ở Footer.
* **Thành phần UI**:
  * Thêm vào `OutputSection`:
    * Row `I18n.t("export.exportSubtitlesSrt")` kèm `Switch` bật/tắt `export-subtitles`.
    * Row nút bấm phụ `I18n.t("export.exportSrtNow")` cho phép lưu file `.srt` độc lập ngay lập tức.
  * Thêm vào `ExportFooter`:
    * Khi render video hoàn tất, nếu có `written-srt`, hiển thị dòng thông báo màu xanh `✓ Đã xuất kèm tệp phụ đề: <tên_file>.srt`.

### B. Logic Bộ điều khiển Rust (Rust Controller)
* **File**: `src/crates/concat/src/panes/export.rs`
* **ExportMsg**:
  * `ExportSubtitlesChanged(bool)`
  * `ExportSrtOnly`
* **ExportPane**:
  * Trường `export_subtitles: bool`
  * Trường `written_srt: Option<String>`
* **Cơ chế ghi file**:
  * Khi nhận `ExportMsg::Finished(Ok(ref written))`:
    * Nếu `self.export_subtitles == true`:
      * Trích xuất các cue từ timeline: `concat_project::srt::title_cues(studio.timeline(), None)`.
      * Nếu có cues: Ghi file `.srt` tại đường dẫn `Path::new(written).with_extension("srt")`.
      * Cập nhật `self.written_srt = Some(...)`.
      * Thông báo thành công: `studio.notify(&tf("export.exportedWithSubtitles", &[&srt_name]), false)`.
  * Khi nhận `ExportMsg::ExportSrtOnly`:
    * Lấy danh sách cues và đường dẫn xuất (thư mục đích + tên video + `.srt`).
    * Ghi file `.srt` và hiển thị thông báo cho người dùng.

### C. Đa ngôn ngữ (i18n)
* Cập nhật `src/crates/concat/locales/vi.json` và `en.json`:
  * `export.exportSubtitlesSrt`: "Xuất kèm tệp phụ đề (.srt)" / "Export subtitles (.srt)"
  * `export.exportSrtOnly`: "Chỉ xuất tệp phụ đề" / "Export subtitles only"
  * `export.exportSrtNow`: "Xuất tệp SRT…" / "Export SRT…"
  * `export.exportedWithSubtitles`: "Đã xuất kèm tệp phụ đề {0}" / "Also exported subtitles to {0}"
  * `export.noSubtitlesOnTimeline`: "Không có phụ đề nào trên dòng thời gian" / "No subtitles on the timeline"

---

## 3. Kế hoạch Kiểm thử (Test Strategy)
1. Unit test kiểm tra trích xuất cues từ timeline và render chuỗi chuẩn SubRip (`.srt`).
2. Unit test kiểm tra logic `ExportPane::update` khi bật/tắt `ExportSubtitlesChanged`.
3. Integration test kiểm tra tiến trình `ExportMsg::Finished(Ok(...))` tự động tạo file `.srt` hợp lệ trên ổ đĩa.
