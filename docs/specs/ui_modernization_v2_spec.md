# Feature Specification: Modern UI Redesign for Concat (v2.0.14)

## 1. Executive Summary & Objectives
This specification defines the comprehensive aesthetic and functional modernization of the Concat desktop video editor interface for Windows. The goal is to transform the visual experience into a high-end, sleek, professional video editing workstation inspired by modern dark glassmorphism, DaVinci Resolve, and CapCut Pro, while maintaining 100% architectural compatibility with Slint UI and Rust backend bindings.

---

## 2. Design System & Token Architecture

### 2.1 Color Palette (`ui/theme/dark.slint`)
- **Root Page Background (`page`)**: Deep obsidian `#0a0c13`
- **Panels (`panel`)**: High-depth slate `#121522`
- **Raised Surfaces (`raised`)**: Elevated slate `#1a1e30`
- **Wells / Sunkens (`well`)**: Deep recessed well `#0e101a`
- **Inputs & Fields (`field`)**: `#22283d`
  - Hover: `#2d3550`
  - Active: `#384264`
- **Accent Palette**:
  - Primary Default: Cyber Violet (`#8b5cf6` / `#a78bfa`) & Electric Cyan (`#06b6d4` / `#22d3ee`)
  - Supported: Lime (`#a3e635`), Rose (`#f43f5e`), Amber (`#f59e0b`), Mint (`#10b981`)
- **Hairlines & Borders**:
  - Standard Line: `#ffffff18` (smooth glass edge)
  - Focus / Strong Line: `#8b5cf666` (subtle accent glow)

### 2.2 Typography & Radii (`ui/theme/theme.slint`)
- **Corner Radii**:
  - Small elements (`r-xs`): 4px
  - Inputs / Buttons (`r-sm`): 6px
  - Cards & Panes (`r`): 10px
  - Floating Panels (`r-lg`): 14px
  - Dialog Sheets (`r-xl`): 20px
- **Control Heights & Spacing**:
  - Standard control height `h`: 30px
  - Micro gap: 6px
  - Section pad: 16px

---

## 3. Screen & Component Modernization

### 3.1 Start / Launch Screen (`ui/start.slint`)
- **Hero Card**:
  - Prominent "New Project" action button with radiant gradient fill and active glow.
  - "Open Project" with secondary glass styling.
  - Dropzone tile with animated dash border and icon.
- **Projects Showcase Grid**:
  - Elevation card layout with poster preview, aspect ratio tag, duration pill, and hover actions (Reveal in folder, forget).
- **Learn & Community Hub**:
  - Grid of sleek interactive cards with refined micro-icons and clean typography.

### 3.2 Title Bar & Window Header (`ui/title-bar.slint`)
- Integrated dark acrylic header with smooth bottom separator.
- Modern window control caption buttons (Min, Max, Close with red danger highlight).
- Centered project name breadcrumb with save status indicator.

### 3.3 Workspace & Timeline Panes (`ui/workspace/`, `ui/timeline/`)
- Subtle pane gutters creating true depth.
- Floating pane headers with crisp active tab indicators.
- Neon electric cyan playhead on dark banded timeline tracks for peak visibility.

---

## 4. Verification & Testing Plan
1. **Lint & Static Check**: `cargo check --workspace` & Slint compilation pass without syntax or binding errors.
2. **Automated Unit Tests**: Unit tests in `tools/` verifying theme tokens, color contrast, and Slint structural integrity.
3. **Smoke Test Execution**: Running test suite on Windows to ensure 100% green status.
