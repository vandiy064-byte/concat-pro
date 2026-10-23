# Implementation Plan - Modern Professional UI/UX Revamp

## Phase 1: Design Review & User Alignment (Current Phase)
- [x] Generate high-resolution Start Screen design mockup (`ui_mockup_start_screen`).
- [x] Generate high-resolution Editor Workspace design mockup (`ui_mockup_editor_workspace`).
- [x] Author technical specification (`docs/specs/ui_revamp_modern_professional_spec.md`).
- [x] Author atomic execution plan (`docs/plans/ui_revamp_modern_professional_plan.md`).
- [ ] Present design mockups and concept to user for feedback and approval.

---

## Phase 2: Theme Tokens & Color Palette Polish
- [ ] Update `src/crates/concat/ui/theme/dark.slint` with modern obsidian surfaces and
      delicate glass borders.
- [ ] Add neon violet (`#8b5cf6`) and electric cyan (`#06b6d4`) accents into `accent.slint`
      and `theme.slint`.
- [ ] Tune surface elevation ladder: `well`, `panel`, `raised`, `field`, `field-hover`,
      `field-active`.
- [ ] Verify `cargo check` and Slint compilation with updated theme values.

---

## Phase 3: Start Screen (Welcome Hub) Enhancement
- [ ] Elevate hero action buttons with gradient borders and glowing accent hover states.
- [ ] Polish project cards: 12px border radius, duration overlay badge, and hover zoom.
- [ ] Add AI quick tools card row/sidebar (Auto Subtitles, Voiceover Studio, Presets).
- [ ] Ensure seamless in-place project renaming on project card title click.

---

## Phase 4: Editor Workspace & Controls Refinement
- [ ] Polish title bar: glowing gradient `EXPORT` button and workflow navigation switcher.
- [ ] Modernize 4K video monitor floating transport bar and stereo audio peak meter.
- [ ] Enhance timeline appearance: high-contrast audio waveforms, glowing playhead, and
      distinct colored track lanes.
- [ ] Polish Inspector: rounded sliders, color wheel visual enhancement, and typography list.

---

## Phase 5: Verification, Automated Testing & QA
- [ ] Run Slint UI compiler checks and `cargo check --workspace --all-targets`.
- [ ] Run automated tests in `tools/` and `cargo test`.
- [ ] Verify all lines conform to `<= 100` characters.
- [ ] Push changes to GitHub and verify green status on Windows CI.
