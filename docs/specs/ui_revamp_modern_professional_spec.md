# Concat Pro - Modern Professional UI/UX Revamp Specification

## 1. Overview & Objective
This specification defines the complete visual and interactive overhaul of Concat Pro into a
state-of-the-art desktop video editor interface. The objective is to elevate the aesthetics to
match top-tier creative suites (CapCut Pro, DaVinci Resolve, Final Cut Pro) by introducing:
- Deep obsidian and slate glassmorphic surfaces with delicate borders.
- Cyber neon violet (#8b5cf6) and electric cyan (#06b6d4) glowing accents.
- Dynamic micro-interactions (hover glow, scale-lift, smooth timeline feedback).
- Ergonomic workspace organization across Start Hub and Video Editing Workspace.

---

## 2. Design System & Theme Tokens

### 2.1 Surfaces & Depth Ladder
- **Base Ground (`page`)**: `#0b0d13` (Ultra-deep obsidian).
- **Panels & Dividers (`panel`)**: `#131620` with 1px border `rgba(255, 255, 255, 0.07)`.
- **Raised Cards (`raised`)**: `#1a1e2d` with corner radius `10px` - `14px`.
- **Interactive Fields (`field`)**: `#22273b`, hover `#2a314b`, active `#343c5b`.
- **Wells & Sinks (`well`)**: `#0f121b` for timeline bed and track lanes.

### 2.2 Color Palette & Accents
- **Primary Hero Accent**: Neon Violet (`#8b5cf6` to `#a855f7` gradient).
- **Secondary Precision Accent**: Electric Cyan (`#06b6d4` to `#38bdf8`) for playhead and audio.
- **Status & Feedback**:
  * Success / Save: Emerald (`#10b981`).
  * Warning / Alert: Amber (`#f59e0b`).
  * Error: Crimson (`#ef4444`).
- **Timeline Media Tracks**:
  * Video Track: Rich Indigo-Violet (`#6366f1` / `#7c3aed`).
  * Audio Track: Teal-Cyan with luminous white waveform (`#0d9488` / `#06b6d4`).
  * Subtitle Track: Warm Amethyst (`#9333ea`).

---

## 3. UI Component Architecture

### 3.1 Start Screen (Welcome Hub)
1. **Header & Navigation**:
   - Modern Concat Pro brand logo with subtle glow.
   - Global quick-search input with instant filter.
   - Quick settings gear with tooltips.
2. **Hero Action Row**:
   - Prominent glowing `+ New Project` button with interactive gradient.
   - `Import Footage` drop-zone card with dashed glowing border.
   - `AI Auto-Cut & Script` quick-launch action.
3. **Project Grid Cards**:
   - 16:9 poster cards with rounded corners (12px) and shadow depth.
   - Hover preview overlay with duration pill (`03:45`), aspect ratio tag (`16:9`), and
     edit timestamp (`Edited 2h ago`).
   - In-place project rename support.
4. **AI Quick Tools Sidebar**:
   - Quick-access cards for Auto Subtitle Generator, Voiceover Studio, and Preset Library.

### 3.2 Editor Workspace
1. **Title Bar & Workflow Switcher**:
   - Project Name with inline pencil edit trigger.
   - Workflow Tabs: `Media`, `Effects`, `Subtitles`, `Color Grading`, `Audio`, `Deliver`.
   - Action controls: Save status indicator, Undo/Redo, and luminous gradient `EXPORT` button.
2. **Media Bin & Asset Browser**:
   - Folders tree (`Footage`, `Audio`, `SFX`) and clip cards with hover video scrub.
3. **4K Monitor & Preview Controls**:
   - Clean 4K viewport with thin frame border.
   - Floating transport bar: Play/Pause, Step frame, Loop, Aspect ratio switcher, Zoom fit.
   - Dual-channel stereo audio peak meters with -12dB green and 0dB yellow/red warning levels.
4. **Multi-Track Magnetic Timeline**:
   - Vertical track headers: Track lock, Mute, Solo, Volume knob.
   - Audio tracks with rendered high-contrast waveforms.
   - Subtitle track with karaoke word chips.
   - Glowing magnetic playhead with precision timecode flag.
   - Timeline toolbar: Blade cut, Ripple delete, Slip edit, Magnet snap toggle, Zoom slider.
5. **Inspector & Grading Panel**:
   - Collapsible property sections: Transform (Position, Scale, Rotation, Opacity).
   - 3-Way Color Wheels: Lift, Gamma, Gain with chromatic center dot.
   - Typography presets with dynamic font preview.

---

## 4. Verification & Quality Gates
- **Visual Design Review**: Approval from user on design mockups before merging to code.
- **Theme Integrity**: Zero regressions in `Theme` token hierarchy in Slint.
- **Performance**: 60 FPS UI rendering on Windows desktop runner.
- **Line Length**: All files strictly conform to `<= 100` characters per line.
