# SPECIFICATION: Inline Project Renaming from TitleBar

## 1. Mục tiêu (Objective)
Cho phép người dùng nhấp trực tiếp vào tên dự án ở thanh tiêu đề trên cùng (TitleBar - phần đã khoanh tròn trong ảnh) để đổi tên dự án tùy ý bất cứ lúc nào, tự động lưu tên mới vào dự án và đồng bộ lập tức sang bảng Chi tiết (Details panel) và hệ thống lưu trữ mà không cần phải mở hộp thoại Sửa đổi phức tạp.

## 2. Thiết kế Giao diện (UI/UX Design)
- **Trạng thái bình thường (Normal State)**:
  - Hiển thị tên dự án ở vị trí trung tâm thanh tiêu đề.
  - Khi rê chuột vào (hover): Hiển thị nền pill bo tròn nhẹ nhàng (`Theme.field-hover`), đổi màu chữ sáng hơn (`Theme.fg`), kèm icon bút chỉnh sửa (`Glyph.edit`) và con trỏ chuột dạng `pointer`.
  - Tooltip gợi ý: "Nhấp để đổi tên dự án" / "Click to rename project".
- **Trạng thái đang chỉnh sửa (Inline Editing State)**:
  - Khi người dùng click vào tên dự án:
    - Chuyển sang ô nhập liệu (`TextInput`) được bo viền thanh lịch, nền `Theme.field`, viền sáng `Theme.accent`.
    - Tự động điền tên hiện tại và focus sẵn con trỏ.
    - Kèm 2 nút bấm thao tác nhanh:
      - Nút Lưu (Checkmark icon / Enter): Áp dụng tên mới ngay lập tức.
      - Nút Hủy (Close/X icon / Escape): Hủy chỉnh sửa, hoàn nguyên tên cũ.
- **Trạng thái sau khi đổi tên**:
  - Tên dự án cập nhật tức thì trên TitleBar, bảng Details panel (Chi tiết), và lưu vào project document.
  - Hiện thông báo Toast nhỏ: "Đã đổi tên dự án thành: {tên}".

## 3. Kiến trúc Luồng Dữ liệu (Architecture & Data Flow)
1. **Slint UI (`ui/title-bar.slint`)**:
   - Thêm trạng thái `editing: bool` và `draft-name: string`.
   - Bắt sự kiện click để kích hoạt `editing = true`.
   - Bắt sự kiện `accepted` (phím Enter) hoặc nhấn nút xác nhận để gọi callback `rename-project(string)`.
2. **App Root (`ui/app.slint`)**:
   - Truyền callback `rename-project(name)` từ `TitleBar` lên `AppWindow`.
3. **Rust Backend (`src/crates/concat/src/lib.rs` & `studio.rs`)**:
   - Đăng ký handler `app.on_rename_project(...)`.
   - Khi nhận tên mới:
     - Trim khoảng trắng, kiểm tra tên hợp lệ.
     - Cập nhật `studio.project_name = new_name`.
     - Gọi `session.prepare_save(Some(&new_name))` và lưu dự án `studio.save(false)`.
     - Đồng bộ lại toàn bộ giao diện qua `app.set_project_name(...)`.
4. **Locales (`locales/vi.json` & `locales/en.json`)**:
   - Thêm các chuỗi thông báo và tooltip:
     - `project.clickToRename`: "Nhấp để đổi tên dự án" / "Click to rename project"
     - `project.renameSuccess`: "Đã đổi tên dự án thành {0}" / "Project renamed to {0}"

## 4. Kiểm thử Logic (Testing)
- Viết test kiểm tra logic đổi tên dự án trong Rust:
  - Đổi tên hợp lệ -> cập nhật `studio.project_name` và session.
  - Tên rỗng hoặc toàn khoảng trắng -> giữ nguyên tên cũ, không lỗi.
  - Ký tự tiếng Việt có dấu -> lưu và hiển thị trọn vẹn UTF-8.
