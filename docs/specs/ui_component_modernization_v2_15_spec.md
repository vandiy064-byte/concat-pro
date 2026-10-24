# Specification: Concat Pro Component-Level UI Modernization (v2.0.15)

## 1. Overview & Objective
In v2.0.14, global theme palette tokens were shifted to Obsidian Dark (`#111420`). However,
individual UI components (Media Library tabs, Drop-zone, Preview stage, Transport controls,
Inspector facts, Timeline tool buttons) retained their flat, minimalist layouts.
The objective of v2.0.15 is to overhaul these core UI components into a state-of-the-art
Cyber Dark Glassmorphism Studio interface with glowing neon accents, pill badges, and
card-based visual hierarchy.

## 2. Component Overhauls

### 2.1 Media Library & Drop-Zone (`workspace/media-pane.slint`)
- **LibraryTab Component**:
  - Elevated capsule pill shape on active tab (`root.current`).
  - Active background: Soft glass gradient (`#8b5cf625` to `#06b6d418`) with 1px border.
  - Active indicator: Vibrant neon glowing bottom line pill.
  - Text & Glyph tint: Neon violet highlight (`#a78bfa`) for active, glowing hover state.
- **Empty Media Placeholder (`Empty` component)**:
  - Transform from plain text into a high-end Glassmorphic Drop Card.
  - 14px rounded container with 1px border (`#8b5cf633`).
  - Glowing icon ring (52px circle) with `#8b5cf61f` fill and `#8b5cf6` glyph.
  - Modern typography hierarchy with prominent headline and subtle helper text.

### 2.2 Preview Monitor & Transport Controls (`workspace/preview-pane.slint`)
- **Stage (Player Screen)**:
  - High-end studio cinema monitor styling (`#0d0f17` to `#06080e` gradient).
  - Empty state: Circular neon badge (`#8b5cf61a` background, `#8b5cf6` glyph).
  - High-tech HUD badge text for professional look even when idle.
- **Transport Bar**:
  - Timecode display: High-tech HUD pill badge container with dark well background.
  - Play/Pause Button (`accent: true`):
    - Prominent circular/capsule glowing button (`#8b5cf6` to `#06b6d4` gradient).
    - Crisp white play/pause glyph with hover brightness lift (`#a855f7` to `#22d3ee`).

### 2.3 Inspector & Details Panel (`workspace/config-pane.slint`)
- **Project & Timeline Facts**:
  - Convert plain flat rows into three distinct Glassmorphic Info Cards:
    1. Project Card (`DỰ ÁN`)
    2. Timeline Card (`DÒNG THỜI GIAN`)
    3. Contents Card (`NỘI DUNG`)
  - Card styling: Subtle dark glass gradient (`#181c2c88` to `#111420bb`), 10px rounded corners.
  - Fact rows: Elevated readable technical font with clear labels and crisp values.
- **Modify Button**:
  - Modern capsule button with glowing neon border and hover animation.

### 2.4 Timeline Tool Tray & Buttons (`primitives/panel.slint` & `timeline/tray.slint`)
- **IconButton / TrayButton**:
  - Active tool state (`checked: true`): Neon pill highlight with subtle glow.
  - Hover state: Modern glassmorphic feedback (`Theme.field-hover` with 1px border).
  - Subtle group dividers with soft contrast.

## 3. Engineering Constraints
- Slint syntax compliance (no unsupported CSS attributes, no binding loops).
- Maximum line length strictly `<= 100` characters.
- Strict backward compatibility with all Rust callbacks and properties.
- Automated Python unit test coverage verifying modern components and line lengths.
