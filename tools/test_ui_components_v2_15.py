"""
Unit tests for the Concat Pro Component-Level Modernization (v2.0.15).
Validates that:
1. media-pane.slint contains the modern LibraryTab active gradient & indicator,
   and the Empty glassmorphic drop card with neon badge.
2. preview-pane.slint contains the Ultra HD monitor HUD badge and timecode HUD container.
3. config-pane.slint contains Glassmorphic Info Cards and the modern Modify capsule.
4. panel.slint contains glowing gradient accent and modern checked states for IconButton.
5. tray.slint uses subtle neon Divider.
6. All lines in modified files are <= 100 characters.
"""
import pathlib
import unittest

def find_repo_root() -> pathlib.Path:
    cur = pathlib.Path(__file__).resolve().parent
    if (cur / "src" / "Cargo.toml").exists():
        return cur
    if (cur.parent / "src" / "Cargo.toml").exists():
        return cur.parent
    return cur

ROOT = find_repo_root()
UI_DIR = ROOT / "src" / "crates" / "concat" / "ui"

class TestUIComponentsV215(unittest.TestCase):
    def test_media_pane_components(self):
        media_pane = (UI_DIR / "workspace" / "media-pane.slint").read_text(encoding="utf-8")
        self.assertIn("#8b5cf630", media_pane, "LibraryTab should use neon violet gradient")
        self.assertIn("#c084fc", media_pane, "LibraryTab and Empty should use bright neon violet")
        self.assertIn("STUDIO MEDIA DROP", media_pane, "Empty drop card should have HUD badge")
        self.assertIn("icon-badge :=", media_pane, "Empty component should have circular badge")

    def test_preview_pane_components(self):
        preview_pane = (UI_DIR / "workspace" / "preview-pane.slint").read_text(encoding="utf-8")
        self.assertIn("monitor-badge :=", preview_pane, "Preview stage should have monitor badge")
        self.assertIn("ULTRA HD PREVIEW ENGINE", preview_pane, "Stage should have Ultra HD HUD badge")
        self.assertIn("timecode-hud :=", preview_pane, "Transport bar should have timecode HUD container")

    def test_config_pane_components(self):
        config_pane = (UI_DIR / "workspace" / "config-pane.slint").read_text(encoding="utf-8")
        self.assertIn("Project Info Card", config_pane, "Config pane should have Project Info Card")
        self.assertIn("Timeline Info Card", config_pane, "Config pane should have Timeline Info Card")
        self.assertIn("Contents Info Card", config_pane, "Config pane should have Contents Info Card")
        self.assertIn("#c084fc", config_pane, "Modify button should have neon hover border")

    def test_icon_button_components(self):
        panel = (UI_DIR / "primitives" / "panel.slint").read_text(encoding="utf-8")
        self.assertIn("root.accent ? #ffffff", panel, "Accent Play button should have white icon")
        self.assertIn("#c084fc", panel, "Checked icon button should have neon violet icon")
        self.assertIn("border-radius: root.accent ? (self.height / 2)", panel,
                      "Accent button should be circular/capsule")

    def test_tray_divider(self):
        tray = (UI_DIR / "timeline" / "tray.slint").read_text(encoding="utf-8")
        self.assertIn("#8b5cf633", tray, "Tray divider should have subtle neon violet accent")

    def test_line_lengths(self):
        files_to_check = [
            UI_DIR / "workspace" / "media-pane.slint",
            UI_DIR / "workspace" / "preview-pane.slint",
            UI_DIR / "workspace" / "config-pane.slint",
            UI_DIR / "primitives" / "panel.slint",
            UI_DIR / "timeline" / "tray.slint",
        ]
        for f in files_to_check:
            lines = f.read_text(encoding="utf-8").splitlines()
            for idx, line in enumerate(lines, 1):
                self.assertLessEqual(
                    len(line), 100,
                    f"Line {idx} in {f.name} exceeds 100 characters: {line} ({len(line)} chars)"
                )

if __name__ == "__main__":
    unittest.main()
