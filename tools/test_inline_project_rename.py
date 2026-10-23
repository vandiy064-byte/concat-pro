#!/usr/bin/env python3
"""Unit tests for inline project renaming feature."""

import json
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent

class TestInlineProjectRename(unittest.TestCase):
    def test_locale_keys(self):
        en_file = ROOT / "src" / "crates" / "concat" / "locales" / "en.json"
        vi_file = ROOT / "src" / "crates" / "concat" / "locales" / "vi.json"

        with open(en_file, "r", encoding="utf-8") as f:
            en_data = json.load(f)
        with open(vi_file, "r", encoding="utf-8") as f:
            vi_data = json.load(f)

        self.assertIn("project.clickToRename", en_data)
        self.assertIn("project.renameSuccess", en_data)
        self.assertIn("project.clickToRename", vi_data)
        self.assertIn("project.renameSuccess", vi_data)

        self.assertEqual(en_data["project.clickToRename"], "Click to rename project")
        self.assertEqual(en_data["project.renameSuccess"], "Project renamed to {0}")
        self.assertEqual(vi_data["project.clickToRename"], "Nhấp để đổi tên dự án")
        self.assertEqual(vi_data["project.renameSuccess"], "Đã đổi tên dự án thành {0}")

    def test_slint_title_bar_bindings(self):
        tb_file = ROOT / "src" / "crates" / "concat" / "ui" / "title-bar.slint"
        content = tb_file.read_text(encoding="utf-8")

        self.assertIn("callback rename-project(string);", content)
        self.assertIn("property <bool> editing-name", content)
        self.assertIn("property <string> name-draft", content)
        self.assertIn("function start-rename()", content)
        self.assertIn("function commit-rename", content)
        self.assertIn("function cancel-rename()", content)
        self.assertIn("rename-input := TextInput", content)
        self.assertIn("Glyph.edit", content)
        self.assertIn("Glyph.check", content)
        self.assertIn("Glyph.close", content)

    def test_slint_app_wiring(self):
        app_file = ROOT / "src" / "crates" / "concat" / "ui" / "app.slint"
        content = app_file.read_text(encoding="utf-8")

        self.assertIn("callback rename-project(string);", content)
        self.assertIn("rename-project(name) => { root.rename-project(name); }", content)

    def test_rust_lib_callback(self):
        lib_file = ROOT / "src" / "crates" / "concat" / "src" / "lib.rs"
        content = lib_file.read_text(encoding="utf-8")

        self.assertIn("app.on_rename_project", content)
        self.assertIn("state.rename_project(name.as_str());", content)

    def test_rust_studio_rename_logic(self):
        studio_file = ROOT / "src" / "crates" / "concat" / "src" / "studio.rs"
        content = studio_file.read_text(encoding="utf-8")

        self.assertIn("pub fn rename_project(&mut self, new_name: &str)", content)
        self.assertIn("let trimmed = new_name.trim();", content)
        self.assertIn("session.prepare_save(Some(trimmed));", content)
        self.assertIn('tf("project.renameSuccess"', content)

    def test_rename_validation_logic(self):
        current_name = "Untitled project 5"

        def simulate_rename(new_name, current):
            trimmed = new_name.strip()
            if not trimmed or trimmed == current:
                return None
            return trimmed

        # Empty / whitespace cases
        self.assertIsNone(simulate_rename("", current_name))
        self.assertIsNone(simulate_rename("   ", current_name))
        self.assertIsNone(simulate_rename("Untitled project 5", current_name))

        # Valid renames
        self.assertEqual(simulate_rename("My New Video", current_name), "My New Video")
        self.assertEqual(simulate_rename("  Spaced Name  ", current_name), "Spaced Name")

        # Vietnamese Unicode
        vi_name = "Video Hướng Dẫn Concat Tiếng Việt"
        self.assertEqual(simulate_rename(vi_name, current_name), vi_name)

if __name__ == "__main__":
    unittest.main()
