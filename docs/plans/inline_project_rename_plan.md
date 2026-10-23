# ATOMIC TASK PLAN: Inline Project Renaming Feature

## Task 1: Locales & Text Strings
- Add `project.clickToRename` and `project.renameSuccess` to `locales/en.json` and `locales/vi.json`.
- Run `python scripts/locales.py --check` to ensure no keys are missing across all locales.

## Task 2: Slint UI Components (`ui/title-bar.slint` & `ui/app.slint`)
- In `title-bar.slint`:
  - Add `callback rename-project(string)`.
  - Add state properties: `property <bool> editing: false`, `property <string> draft: ""`.
  - When not editing:
    - Display project name inside an interactive hoverable pill (`TouchArea` with pointer cursor, `Theme.field-hover` background when hovered).
    - Show an edit pencil icon (`Glyph.edit`) beside the name on hover.
    - Click action: sets `draft = root.project-name; editing = true; input.focus();`.
  - When editing:
    - Display inline editing box with `TextInput` (`text <=> root.draft`).
    - Handle `accepted` (Enter key) to trigger `commit()`.
    - Provide confirm (checkmark) and cancel (close/X) action buttons.
    - Function `commit()`: if draft is valid, calls `root.rename-project(root.draft); editing = false;`.
    - Function `cancel()`: sets `editing = false;`.
- In `app.slint`:
  - Connect `TitleBar.rename-project(name)` to `AppWindow.rename-project(name)`.

## Task 3: Rust Backend Integration (`src/crates/concat/src/`)
- In `src/crates/concat/src/lib.rs`:
  - Register `app.on_rename_project(on_window!(|state, name: SharedString| { ... }))`.
  - Implement handler in `Studio::rename_project(&mut self, new_name: &str)`.
  - In `Studio::rename_project`:
    - Validate and trim name.
    - Update `self.project_name = trimmed.to_owned()`.
    - Update active session via `session.prepare_save(Some(&trimmed))`.
    - Auto-save project via `self.save(false)`.
    - Notify user with Toast: `studio.notify(&i18n::tf("project.renameSuccess", &[&trimmed]), false)`.
    - Sync UI: `app.set_project_name(trimmed.into())`.

## Task 4: Unit Testing & Logic Verification
- Write Rust unit test in `src/crates/concat/tests/` or in `src/crates/concat/src/studio.rs`:
  - Test `rename_project` updates project name and session document.
  - Test empty name / whitespace handling.
  - Test UTF-8 Vietnamese name handling (e.g. "Dự án Concat Tiếng Việt").

## Task 5: Code Quality, Rustfmt & CI Validation
- Ensure all modified files strictly comply with `rustfmt.toml` (max_width = 100).
- Run `python scripts/models.py --check` and `python scripts/locales.py --check`.
- Commit, update tag `v2.0.12`, push to GitHub and verify GitHub Actions build and release.
