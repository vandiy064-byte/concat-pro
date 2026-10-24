# Implementation Plan: UI Modernization v2.0.14

## Task Breakdown (Atomic Tasks)

### Task 1: Theme & Design Tokens (`ui/theme/`)
- [ ] Update `src/crates/concat/ui/theme/dark.slint`:
  - Deep obsidian page ground (`#0a0c13`), high-depth slate panel (`#121522`), raised (`#1a1e30`), field (`#22283d`).
  - Luminous accent default (Violet & Cyan) with proper hover and soft alpha tones.
  - Refined neon playhead (`#06b6d4`), timeline ruler, and hairlines.
- [ ] Update `src/crates/concat/ui/theme/theme.slint`:
  - Adjust radii (`r-xs: 4px`, `r-sm: 6px`, `r: 10px`, `r-lg: 14px`, `r-xl: 20px`).
  - Standardize control height `h: 30px` and padding `pad: 16px`.

### Task 2: Custom Title Bar Modernization (`ui/title-bar.slint`)
- [ ] Refine `WindowButton` hover animations and glass backgrounds.
- [ ] Refine `MenuLabel` and `HeaderIconButton` pill styles and smooth hover transitions.

### Task 3: Start Screen Visual Upgrade (`ui/start.slint`)
- [ ] Upgrade hero action card and create buttons with radiant accents.
- [ ] Enhance recent project cards with rounded frames, duration tags, and hover highlights.
- [ ] Polish Learn and Community cards with sleek card outlines and icon highlights.

### Task 4: Workspace & Pane Polish (`ui/workspace/`, `ui/dock.slint`)
- [ ] Polish `pane.slint` header styling, active tabs, and divider lines.
- [ ] Polish `splitter.slint` hover indicators and grip handles.

### Task 5: Testing & Quality Assurance
- [ ] Create `tools/test_ui_modernization.py` to validate token values, Slint syntax, and file integrity.
- [ ] Execute `cargo check -p concat` locally to verify 100% clean compilation.
- [ ] Run full test suite with `python -m unittest discover -s tools`.

### Task 6: Review & Release `v2.0.14`
- [ ] Increment version in `src/Cargo.toml` to `2.0.14`.
- [ ] Commit changes, create tag `v2.0.14`, and push to GitHub.
- [ ] Monitor GitHub Actions release pipeline.
