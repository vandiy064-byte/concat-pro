# SPECIFICATION: GitHub Releases Auto-Publishing & In-App Updater Integration

## 1. Mục tiêu (Objective)
Cho phép người dùng cập nhật phiên bản mới của Concat Pro trực tiếp ngay trên giao diện ứng dụng (**Cài đặt -> Phiên bản -> Kiểm tra cập nhật -> Cài đặt**) mỗi khi có tính năng mới (hoặc sửa đổi công cụ), thay vì phải mở trình duyệt web tải thủ công file `.exe` / `.zip` qua GitHub Actions.

## 2. Hiện trạng & Nguyên nhân (Root Cause Analysis)
1. **Giao diện hiện thông báo:** *"Chưa có bản phát hành nào từ 0.2.5 trở đi."*
   - Căn cứ mã nguồn [`concat-host/src/updates.rs`](file:///e:/concat/Concat-main/src/crates/concat-host/src/updates.rs), Concat gọi GitHub API: `https://api.github.com/repos/vandiy064-byte/concat-pro/releases?per_page=100`.
   - Kiểm tra API thực tế: Hiện tại kho `vandiy064-byte/concat-pro` chưa có bất kỳ bản phát hành (GitHub Release) chính thức công khai nào.
   - Workflow `.github/workflows/build-app.yml` trước đây chỉ tải artifact tạm thời lên Actions (`actions/upload-artifact`), không tự động phát hành GitHub Release.
2. **Cấu hình Repo trong Script Manifest:**
   - [`scripts/models.py`](file:///e:/concat/Concat-main/scripts/models.py) dòng 39 đang cố định `REPO = "jub0t/Concat"`, khiến link tải package trong file `manifest.json` có thể trỏ nhầm về repo gốc thay vì repo `vandiy064-byte/concat-pro`.
3. **Môi trường cài đặt trên máy người dùng:**
   - Ứng dụng của người dùng nằm tại `E:\concat\Concat\concat.exe` và đã có sẵn `unins000.exe` (được cài đặt qua bộ cài Inno Setup `PackageKind::Setup`).
   - Điều này xác nhận hệ thống Windows Auto-Updater của Concat đã hoàn toàn đủ điều kiện kích hoạt và hoạt động tự động khi có GitHub Release hợp lệ kèm `manifest.json`.

## 3. Thiết kế giải pháp (Technical Design)

### 3.1. Cập nhật `scripts/models.py`
- Lấy `REPO = os.environ.get("GITHUB_REPOSITORY", "vandiy064-byte/concat-pro")`.
- Đảm bảo URL tải package luôn trỏ đúng `https://github.com/vandiy064-byte/concat-pro/releases/download/{tag}/{file}`.

### 3.2. Cập nhật Workflow `.github/workflows/build-app.yml`
- Bổ sung `permissions: contents: write` cho workflow runner.
- Thêm bước sinh `stage/manifest.json` tự động ngay sau khi đóng gói bộ cài Windows Inno Setup (`Concat-...-setup.exe`), MSI và Portable Zip:
  ```powershell
  python scripts/models.py release-manifest --version $env:VERSION --tag "v$env:VERSION" --bundles stage --out stage/manifest.json
  ```
- Thêm bước tự động Publish / Update GitHub Release sử dụng action `softprops/action-gh-release@v2`:
  - `tag_name: v${{ steps.version.outputs.version }}`
  - `name: Concat v${{ steps.version.outputs.version }}`
  - `draft: false` (bắt buộc `draft: false` để Concat app nhìn thấy bản release)
  - `prerelease: false`
  - `files: stage/*` (chứa `setup.exe`, `msi`, `zip`, `manifest.json`)
  - Chạy tự động khi push nhánh `main` hoặc kích hoạt manual dispatch.

### 3.3. Nâng phiên bản (Version Bump)
- Nâng `version` trong [`src/Cargo.toml`](file:///e:/concat/Concat-main/src/Cargo.toml) từ `2.0.9` lên `2.0.10` (chứa tính năng xuất phụ đề SRT vừa hoàn thiện).
- Khi người dùng đang chạy bản `2.0.9` ấn "Kiểm tra cập nhật", Concat sẽ phát hiện bản `2.0.10` mới hơn và sáng nút "Cài đặt".

### 3.4. Cập nhật script đẩy mã nguồn
- Cập nhật [`Push_To_GitHub.bat`](file:///e:/concat/Push_To_GitHub.bat) để đẩy cả commit và tag `v2.0.10` lên GitHub.

## 4. Kế hoạch kiểm thử (Test Plan)
1. Chạy test `scripts/models.py release-manifest` cục bộ đảm bảo sinh `manifest.json` hợp lệ với URL `vandiy064-byte/concat-pro`.
2. Kiểm tra schema của `manifest.json` có đúng định dạng mà `concat-host/src/updates.rs` đọc (bao gồm key `binaries.windows.x86_64.setup`).
3. Kiểm thử cú pháp YAML của `.github/workflows/build-app.yml`.
