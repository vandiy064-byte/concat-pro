# Specification: CI Pipeline Perfection & Windows Release Optimization

## 1. Context & Motivation
- **Issue Observed**:
  - In GitHub Actions workflow execution, the job `CI / Engine tests and lints` on Linux (`ubuntu-24.04`):
    - With single thread (`--build-jobs 1`), timed out after 25 minutes.
    - With 2 parallel threads (`--build-jobs 2`), exceeded GitHub runner memory limits during heavy GUI crate linking, failing with `Error: Process completed with exit code 143` (SIGTERM by kernel/systemd OOM).
  - Meanwhile, the project is configured **exclusively for Windows x86_64** release artifacts:
    - The Windows test job (`desktop` on `windows-2022`) builds and executes tests in 15 minutes, passing 100% green.
    - The Windows application build job (`build-app` on `windows-2022`) packages NSIS installer, MSI, and zip artifacts with 100% green status.
  - The fragile Linux GUI test compilation on Ubuntu was blocking the entire automated release of the Windows application.

## 2. Requirements & Changes

### R1. Restructure Linux CI as Dedicated Static Analysis & Lint Suite
- In `.github/workflows/ci.yml` for job `engine`:
  - Optimize `System libraries` apt-get by disabling `needrestart` prompts and avoiding recommends, reducing duration from 33m to under 2m.
  - Retain full static analysis and verification:
    - `cargo fmt --check`
    - `python3 scripts/locales.py --check`
    - `python3 scripts/models.py --check`
    - `cargo clippy --workspace --all-targets -- -D warnings` (compiles and lints all targets across all crates)
    - `cargo clippy -p concat-server -p concat-cli --features grpc --all-targets -- -D warnings`
  - Remove fragile Linux GUI nextest compilation steps (`Build the tests`, `Run the tests`) from Ubuntu runner, eliminating memory exhaustion (exit code 143) and timeouts.

### R2. Maintain Comprehensive Test Execution on Windows
- Job `desktop` on `windows-2022` remains the authoritative test runner:
  - Compiles all workspace tests (`cargo nextest run --workspace --no-run --build-jobs 2`).
  - Executes the full test suite (`cargo nextest run --workspace --build-jobs 2 --profile ci`).
  - Executes editing session export tests (`cargo nextest run -p concat-host --test export`).

### R3. Strict Code & Formatting Standards
- Every modified line in `.github/workflows/ci.yml` is <= 100 characters.
- Valid YAML syntax.

## 3. Verification & Acceptance Criteria
- Unit tests in `tools/test_ci_optimization.py` and `tools/test_windows_only_pipeline.py` pass.
- All 38+ unit tests pass.
- CI pipeline completes 100% green on both Linux lints and Windows test suites.
- Release pipeline successfully publishes Windows installers to GitHub Releases.
