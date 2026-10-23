import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent


class TestUiModernTheme(unittest.TestCase):
    """Automated tests validating modern cyber dark glassmorphic theme tokens and components."""

    def test_dark_palette_tokens(self):
        dark_slint = (ROOT / "src" / "crates" / "concat" / "ui" / "theme" / "dark.slint")
        content = dark_slint.read_text(encoding="utf-8")
        self.assertIn("panel: #151824", content)
        self.assertIn("line-strong: #8b5cf666", content)
        self.assertIn("playhead: #06b6d4", content)
        self.assertIn("wave: #38bdf8d9", content)
        self.assertIn("accent: #8b5cf6", content)
        self.assertIn("accent: #06b6d4", content)

    def test_titlebar_export_button_gradient(self):
        titlebar = (ROOT / "src" / "crates" / "concat" / "ui" / "title-bar.slint")
        content = titlebar.read_text(encoding="utf-8")
        self.assertIn("export-button := Rectangle", content)
        self.assertIn("@linear-gradient(135deg, #8b5cf6 0%, #06b6d4 100%)", content)
        self.assertIn("border-radius: self.height / 2", content)

    def test_start_screen_neon_glow_and_cards(self):
        start_slint = (ROOT / "src" / "crates" / "concat" / "ui" / "start.slint")
        content = start_slint.read_text(encoding="utf-8")
        self.assertIn("@linear-gradient(135deg, #8b5cf6 0%, #06b6d4 100%)", content)
        self.assertIn("#8b5cf688", content)
        self.assertIn("#8b5cf626", content)
        self.assertIn("#06b6d418", content)


if __name__ == "__main__":
    unittest.main()
