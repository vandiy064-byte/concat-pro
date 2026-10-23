# Specification: Windows-Only Build & Release Pipeline

## 1. Context & Motivation
- **User Request**: The user wants to focus the compilation and release exclusively on the Windows build (`Concat-...-windows-x86_64-setup.exe`, `.msi`, `.zip`).
- **Current Problem**:
  - The repository currently triggers builds for 4 mobile phone targets (Android ARM64, Android x86_64, iOS ARM64, iOS Simulator in `mobile.yml`), Nix packages (`nix.yml`), and macOS runners (`ci.yml`).
  - These extra platforms consume enormous GitHub Actions runner minutes (tokens/resources), cause runner queue congestion, and slow down the release process by 40-60+ minutes.
  - Mobile phone jobs frequently encounter transient environmental or signing failures, blocking the release of Windows binaries even when the Windows build succeeds.
- **Goal**:
  - Restructure CI/CD workflows so that all automated pipelines (on push to `main` and release tags `v*`) focus 100% on Windows x86_64.
  - Retain `workflow_dispatch` on phone/macOS/Nix workflows for optional manual triggering if ever needed in the future, but prevent them from running automatically.

---

## 2. Requirements & Architectural Changes

### R1. Streamline `release.yml`
- Remove the `phones` job dependency from the release pipeline.
- Update `publish` job to only depend on `[check, build]`.
- Update release packaging to collect Windows release artifacts (`setup.exe`, `.msi`, `.zip`, `manifest.json`, `SHA256SUMS`).

### R2. Prevent Automatic Execution of Mobile Builds (`mobile.yml`)
- Remove automatic `push: branches: [main]` trigger from `mobile.yml`.
- Retain `workflow_dispatch` for manual on-demand execution.

### R3. Prevent Automatic Execution of Nix Flake Builds (`nix.yml`)
- Remove automatic `push: branches: [main]` trigger from `nix.yml`.
- Retain `workflow_dispatch` for manual on-demand execution.

### R4. Streamline CI Pipeline (`ci.yml`)
- In `desktop` job matrix, remove `macos-15` so CI tests only on Windows (`windows-2022`).
- CI on Windows runs tests, verification, and smoke tests without burning macOS runner minutes.

### R5. Ensure Windows Build Integrity (`build-app.yml`)
- Maintain existing `windows-x86_64` matrix target.
- Verify `Publish to GitHub Releases` continues generating and publishing:
  - `Concat-<version>-windows-x86_64-setup.exe` (NSIS Installer)
  - `Concat-<version>-windows-x86_64.msi` (Windows Installer)
  - `Concat-<version>-windows-x86_64.zip` (Portable Archive)
  - `manifest.json` (In-app auto-updater)
  - `SHA256SUMS` (Verification checksums)

---

## 3. Verification & Acceptance Criteria
- Full test suite passes via automated Python test (`tools/test_windows_only_pipeline.py`).
- No YAML syntax errors in any `.github/workflows/*.yml`.
- Release and CI workflows on push/tag only initiate Windows runners.
