# Specification: CI Compilation & Timeout Optimization

## 1. Context & Motivation
- **Issue Reported**: During GitHub Actions workflow execution (Run `40022396189`), the job
  `CI / Engine tests and lints` failed at step `Build the tests` with:
  `Error: The action 'Build the tests' has timed out after 25 minutes.`
- **Root Cause**:
  1. In `.github/workflows/ci.yml`, the Linux test compilation step `Build the tests` had
     a strict single-threaded build constraint: `--build-jobs 1`.
  2. Compiling the complete Concat workspace (including heavy GUI, audio, rendering crates like
     `slint`, `i-slint-core`, `lyon`, `swash`, `wgpu`) with only 1 CPU core on an Ubuntu runner
     exceeds 25 minutes on cold cache / cache miss.
  3. The timeout constraint `timeout-minutes: 25` was overly restrictive compared to the
     Windows runner (`timeout-minutes: 60`).
  4. Subsequent test execution steps (`Run the tests`, `Run the documentation's examples`)
     also suffered from single-thread bottlenecks (`--build-jobs 1`, `-j 1`) and tight timeouts.

## 2. Requirements & Changes

### R1. Parallelize Compilation & Execution in Linux CI
- In `.github/workflows/ci.yml` for job `engine`:
  - `Build the tests`: Change `--build-jobs 1` to `--build-jobs 2`.
  - `Build the tests`: Increase `timeout-minutes` from 25 to 60.
  - `Run the tests`: Change `--build-jobs 1` to `--build-jobs 2`.
  - `Run the tests`: Increase `timeout-minutes` from 20 to 40.
  - `Run cargo clippy`: Increase `timeout-minutes` from 25 to 35.
  - `Run the documentation's examples`: Change `-j 1` to `-j 2` and `timeout-minutes` from 10 to 20.
  - Overall `engine` job timeout: Increase `timeout-minutes` from 130 to 160.

### R2. Maintain Windows Test Integrity
- Preserve Windows job (`desktop`) settings which already use `--build-jobs 2` and
  `timeout-minutes: 60` and passed successfully in CI.

### R3. Strict Formatting & Validation
- Maintain line length `<= 100` characters across all modified workflow files.
- Ensure valid YAML syntax without regression.

## 3. Verification & Acceptance Criteria
- Create automated unit test `tools/test_ci_optimization.py` validating:
  - No `--build-jobs 1` or `-j 1` remaining in `ci.yml`.
  - Step timeouts are >= 35 minutes for heavy steps.
  - Overall job timeout is sufficient.
  - YAML syntax is valid.
- All 34+ unit tests in `tools/` pass.
- Locales check (`scripts/locales.py --check`) and models check pass.
