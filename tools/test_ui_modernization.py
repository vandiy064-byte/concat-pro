#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
# Test for UI modernization v2.0.14 design tokens and Slint components

from pathlib import Path
import unittest

REPO_ROOT = Path(__file__).resolve().parent.parent


class TestUIModernization(unittest.TestCase):
    def test_dark_palette_tokens(self):
        dark_slint = (REPO_ROOT / "src/crates/concat/ui/theme/dark.slint").read_text(
            encoding="utf-8"
        )
        self.assertIn("panel: #111420;", dark_slint)
        self.assertIn("raised: #181c2c;", dark_slint)
        self.assertIn("well: #0b0d16;", dark_slint)
        self.assertIn("field: #1e2336;", dark_slint)
        self.assertIn("launch-page: #080a10;", dark_slint)
        self.assertIn("page: #080a10;", dark_slint)
        self.assertIn("line: #ffffff18;", dark_slint)
        self.assertIn("line-strong: #8b5cf680;", dark_slint)

    def test_theme_metrics_and_radii(self):
        theme_slint = (
            REPO_ROOT / "src/crates/concat/ui/theme/theme.slint"
        ).read_text(encoding="utf-8")
        self.assertIn("r-xs: 4px;", theme_slint)
        self.assertIn("r-sm: 6px;", theme_slint)
        self.assertIn("r: 10px;", theme_slint)
        self.assertIn("r-lg: 14px;", theme_slint)
        self.assertIn("r-xl: 20px;", theme_slint)
        self.assertIn("h: 30px;", theme_slint)
        self.assertIn("pad: 16px;", theme_slint)

    def test_start_screen_components(self):
        start_slint = (REPO_ROOT / "src/crates/concat/ui/start.slint").read_text(
            encoding="utf-8"
        )
        self.assertIn("✦ CONCAT PRO STUDIO - ULTRA EDITION ✦", start_slint)
        self.assertIn("background: Theme.launch-panel;", start_slint)

    def test_workspace_pane_styling(self):
        pane_slint = (
            REPO_ROOT / "src/crates/concat/ui/workspace/pane.slint"
        ).read_text(encoding="utf-8")
        self.assertIn("border-width: 1px;", pane_slint)
        self.assertIn("border-color: Theme.line;", pane_slint)

    def test_max_line_length(self):
        files_to_check = [
            REPO_ROOT / "src/crates/concat/ui/theme/dark.slint",
            REPO_ROOT / "src/crates/concat/ui/theme/theme.slint",
            REPO_ROOT / "src/crates/concat/ui/workspace/pane.slint",
        ]
        for path in files_to_check:
            lines = path.read_text(encoding="utf-8").splitlines()
            for idx, line in enumerate(lines, start=1):
                self.assertLessEqual(
                    len(line),
                    100,
                    f"Line {idx} in {path.name} exceeds 100 characters: {line}",
                )


if __name__ == "__main__":
    unittest.main()
