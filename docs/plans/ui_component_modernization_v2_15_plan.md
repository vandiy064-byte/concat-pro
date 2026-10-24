# Plan: Concat Pro Component-Level UI Modernization (v2.0.15)

## 1. Overview
Transform the Concat Pro user interface from flat basic components into an ultra-modern
Cyber Dark Glassmorphism Studio design across all 4 key panes:
Media Library, Preview Monitor, Details/Inspector Panel, and Timeline Tray.

## 2. Atomic Tasks
- [ ] **Task 1: Overhaul LibraryTab & Drop Card in `media-pane.slint`**
  - Add active pill background gradient (`#8b5cf625` to `#06b6d418`) and glowing active line.
  - Upgrade `Empty` component into a sleek Glassmorphic Drop Card with glowing circular badge.
  - Verify line lengths `<= 100` chars.
- [ ] **Task 2: Overhaul Stage & Transport Controls in `preview-pane.slint`**
  - Enhance `!root.has-picture` empty state with 4K Studio Monitor HUD badge and neon ring.
  - Upgrade transport Play button and timecode readout with high-tech badge styling.
  - Verify line lengths `<= 100` chars.
- [ ] **Task 3: Modernize Details / Inspector Panel in `config-pane.slint`**
  - Group Project, Timeline, and Contents facts into styled Glassmorphic Info Cards.
  - Upgrade Modify button to modern neon capsule button.
  - Verify line lengths `<= 100` chars.
- [ ] **Task 4: Modernize IconButton & Tool Tray in `panel.slint` & `tray.slint`**
  - Update `IconButton` in `primitives/panel.slint` to render glowing gradient pill when `accent: true`.
  - Enhance active checked state with neon border and subtle glass background.
  - Verify line lengths `<= 100` chars.
- [ ] **Task 5: Version Bump, Automated Testing & Verification**
  - Bump version in `src/Cargo.toml` to `2.0.15`.
  - Create and run `tools/test_ui_components_v2_15.py` to test component tokens, metrics,
    and verify all lines `<= 100` chars.
  - Run full test suite: `python -m unittest discover -s tools`.
- [ ] **Task 6: Git Commit, Tag, Push & GitHub Actions Monitoring**
  - Commit changes with conventional commit message.
  - Tag `v2.0.15`.
  - Push commit and tag to `origin`.
  - Continuously monitor release run until 100% completed and assets are published.
