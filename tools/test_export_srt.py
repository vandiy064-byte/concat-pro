# SPDX-License-Identifier: AGPL-3.0-or-later
"""
Unit and Integration Tests for Concat Subtitle SRT Export:
1. Validates format_srt_timestamp conversion to SubRip format.
2. Validates export_timeline_to_srt from timeline dictionary.
3. Validates output file creation and content accuracy.
4. Validates empty subtitle handling.
"""

import os
import tempfile
import unittest

from karaoke_subtitles import (
    WordTiming,
    group_words_into_phrases,
    generate_word_clips_for_timeline,
    format_srt_timestamp,
    export_timeline_to_srt,
)


class TestExportSrtFeature(unittest.TestCase):

    def test_format_srt_timestamp(self):
        self.assertEqual(format_srt_timestamp(0.0), "00:00:00,000")
        self.assertEqual(format_srt_timestamp(1.234), "00:00:01,234")
        self.assertEqual(format_srt_timestamp(65.5), "00:01:05,500")
        self.assertEqual(format_srt_timestamp(3661.05), "01:01:01,050")

    def test_export_timeline_to_srt_string(self):
        sample_timeline = {
            "clips": [
                {
                    "kind": "Video",
                    "start": 0.0,
                    "duration": 10.0,
                    "media_path": "background.mp4"
                },
                {
                    "kind": "Text",
                    "start": 1.0,
                    "duration": 2.5,
                    "text": {"content": "Xin chào các bạn đã đến với Concat Pro"}
                },
                {
                    "kind": "Text",
                    "start": 4.0,
                    "duration": 3.0,
                    "text": {"content": "Hôm nay chúng ta xuất video kèm phụ đề SRT"}
                }
            ]
        }

        srt_output = export_timeline_to_srt(sample_timeline)
        self.assertIn("1\n00:00:01,000 --> 00:00:03,500\nXin chào các bạn đã đến với Concat Pro", srt_output)
        self.assertIn("2\n00:00:04,000 --> 00:00:07,000\nHôm nay chúng ta xuất video kèm phụ đề SRT", srt_output)

    def test_export_timeline_to_srt_file(self):
        words = [
            WordTiming("Tự", 0.5, 0.9),
            WordTiming("động", 0.9, 1.3),
            WordTiming("xuất", 1.3, 1.7),
            WordTiming("SRT", 1.7, 2.2),
        ]
        phrases = group_words_into_phrases(words)
        clips = generate_word_clips_for_timeline(phrases)

        with tempfile.TemporaryDirectory() as tmpdir:
            srt_path = os.path.join(tmpdir, "my_video.srt")
            export_timeline_to_srt(clips, output_path=srt_path)

            self.assertTrue(os.path.isfile(srt_path))
            with open(srt_path, "r", encoding="utf-8") as f:
                content = f.read()

            self.assertIn("-->", content)
            self.assertIn("00:00:00,500", content)
            self.assertIn("TỰ", content.upper())

    def test_empty_subtitles_handled_cleanly(self):
        empty_timeline = {"clips": [{"kind": "Video", "start": 0.0, "duration": 5.0}]}
        srt_output = export_timeline_to_srt(empty_timeline)
        self.assertEqual(srt_output.strip(), "")

    def test_subtitles_section_slint_always_visible(self):
        """Verifies SubtitlesSection is declared and placed in 1-col, 2-col, and 3-col layouts."""
        import pathlib
        cur = pathlib.Path(__file__).resolve().parent
        root = cur if (cur / "src" / "Cargo.toml").exists() else (cur.parent if (cur.parent / "src" / "Cargo.toml").exists() else cur.parent / "Concat-main")
        slint_file = root / "src" / "crates" / "concat" / "ui" / "dialogs" / "export.slint"
        content = slint_file.read_text(encoding="utf-8")

        self.assertIn("component SubtitlesSection inherits DialogSection", content)
        self.assertIn("SubtitlesSection", content)
        # Verify it uses enabled: root.data.has-subtitles instead of conditional hide
        self.assertIn("enabled: root.data.has-subtitles", content)
        # Ensure SubtitlesSection is rendered across column modes
        self.assertEqual(content.count("SubtitlesSection {"), 3)

    def test_export_subtitles_locale_integrity(self):
        """Verifies all new keys exist in en.json and vi.json."""
        import json
        import pathlib
        cur = pathlib.Path(__file__).resolve().parent
        root = cur if (cur / "src" / "Cargo.toml").exists() else (cur.parent if (cur.parent / "src" / "Cargo.toml").exists() else cur.parent / "Concat-main")
        locales_dir = root / "src" / "crates" / "concat" / "locales"
        required_keys = [
            "export.subtitlesSection",
            "export.subtitlesDetected",
            "export.noSubtitlesTimelineHint",
            "export.companionSrtHint",
            "export.exportSubtitlesSrt",
            "export.exportSrtOnly",
            "export.exportSrtNow",
            "export.noSubtitlesOnTimeline"
        ]

        for loc in ["en", "vi"]:
            with open(locales_dir / f"{loc}.json", "r", encoding="utf-8") as f:
                data = json.load(f)
            for key in required_keys:
                self.assertIn(key, data, f"Key {key} missing from {loc}.json")
                self.assertTrue(bool(data[key].strip()), f"Key {key} in {loc}.json is empty")


if __name__ == "__main__":
    unittest.main()
