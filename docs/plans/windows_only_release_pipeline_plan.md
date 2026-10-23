# Plan: Windows-Only Build & Release Pipeline

## Atomic Tasks

- [ ] Task 1: Update `.github/workflows/release.yml`
  - Remove `phones` job block.
  - Update `publish` job `needs: [check, build]` (was `[check, build, phones]`).
  - Verify line lengths <= 100 characters.

- [ ] Task 2: Update `.github/workflows/mobile.yml`
  - Remove automatic `push` and `pull_request` triggers so phone builds never run automatically on git push.
  - Retain `workflow_dispatch` and `workflow_call`.

- [ ] Task 3: Update `.github/workflows/nix.yml`
  - Remove automatic `push` and `pull_request` triggers.
  - Retain `workflow_dispatch`.

- [ ] Task 4: Update `.github/workflows/ci.yml`
  - In `desktop` job matrix, remove `macos-15`, keeping only `windows-2022`.
  - Retain `engine` (Linux linter / fast checks) and `windows-2022` (Windows tests).

- [ ] Task 5: Add automated unit test for Windows-only pipeline
  - Create `tools/test_windows_only_pipeline.py`.
  - Verify YAML syntax and assertions that no phone or macOS jobs are queued in automatic triggers.
  - Run full test suite: `python -m unittest discover -s tools`.

- [ ] Task 6: Commit and Push
  - Commit changes with message: `ci: streamline release pipeline to focus exclusively on Windows x86_64`.
  - Push to GitHub repository.
