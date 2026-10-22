# SPDX-License-Identifier: AGPL-3.0-or-later
"""
Automated Test Suite for Concat Pro Features
Validates all 5 capabilities:
1. Word-by-word Karaoke Subtitles
2. Auto Silence Removal & Ripple Cuts
3. Script-to-Video Engine
4. Smart Reframing (16:9 -> 9:16)
5. CapCut PC Draft Converter
"""

import json
import os
import tempfile
import unittest

from karaoke_subtitles import (
    WordTiming,
    group_words_into_phrases,
    render_ass_karaoke,
    generate_word_clips_for_timeline,
)
from silence_remover import compute_ripple_cuts
from script_to_video import (
    split_script_into_sentences,
    estimate_sentence_duration,
    assemble_script_to_timeline,
    save_concat_project_file,
)
from smart_reframe import (
    calculate_scale_to_fill_vertical,
    generate_smooth_pan_keyframes,
    apply_smart_reframe_to_project,
)
from capcut_bridge import convert_concat_to_capcut_draft, sec_to_us


class TestProFeatures(unittest.TestCase):

    def test_01_karaoke_subtitles(self):
        words = [
            WordTiming("Học", 0.0, 0.4),
            WordTiming("AI", 0.4, 0.8),
            WordTiming("thật", 0.8, 1.2),
            WordTiming("đơn", 1.2, 1.5),
            WordTiming("giản", 1.5, 1.9),
        ]
        phrases = group_words_into_phrases(words, max_words_per_line=3)
        self.assertGreaterEqual(len(phrases), 2)
        self.assertEqual(phrases[0].words[0].word, "Học")

        ass = render_ass_karaoke(phrases)
        self.assertIn("[Script Info]", ass)
        self.assertIn("Hormozi", ass)
        self.assertIn("{\\k", ass)

        timeline_clips = generate_word_clips_for_timeline(phrases)
        self.assertEqual(len(timeline_clips), 5)
        self.assertIn("[HỌC]", timeline_clips[0]["text"]["content"])
        self.assertEqual(timeline_clips[0]["active_word"], "Học")
        print("[PASS] Test 1: Karaoke Subtitles OK")

    def test_02_silence_remover_ripple_cuts(self):
        # 10s video with speech at 1-3s and 6-8s (total speech = 4s, silence = 6s)
        speech_intervals = [(1.0, 3.0), (6.0, 8.0)]
        res = compute_ripple_cuts("clip_speech_1", 0.0, 10.0, speech_intervals)

        self.assertEqual(len(res["segments"]), 2)
        self.assertAlmostEqual(res["new_duration"], 4.0, places=2)
        self.assertAlmostEqual(res["time_saved"], 6.0, places=2)
        self.assertEqual(res["segments"][0]["timeline_start"], 0.0)
        self.assertEqual(res["segments"][1]["timeline_start"], 2.0)  # Placed back-to-back
        print("[PASS] Test 2: Auto Silence Removal OK")

    def test_03_script_to_video(self):
        script = """
        # Tiêu đề video
        Đây là câu mở đầu video rất hấp dẫn.
        Đây là nội dung chính cung cấp giá trị.
        Hãy bấm follow kênh để xem thêm nhiều mẹo hay!
        """
        sentences = split_script_into_sentences(script)
        self.assertEqual(len(sentences), 3)

        dur = estimate_sentence_duration(sentences[0])
        self.assertGreater(dur, 1.0)

        proj = assemble_script_to_timeline(
            script,
            project_name="UnitTest_ScriptVideo",
            media_files=["broll1.mp4", "broll2.mp4"],
            music_path="bgm.mp3",
        )
        self.assertEqual(proj["video"]["width"], 1080)
        self.assertEqual(proj["video"]["height"], 1920)
        self.assertGreater(proj["timeline"]["duration"], 4.0)

        # Ensure tracks exist
        track_ids = [t["id"] for t in proj["timeline"]["tracks"]]
        self.assertIn("track_voice", track_ids)
        self.assertIn("track_captions", track_ids)
        self.assertIn("track_video_main", track_ids)
        self.assertIn("track_bgm", track_ids)

        with tempfile.TemporaryDirectory() as tmpdir:
            save_path = os.path.join(tmpdir, "proj.json")
            save_concat_project_file(proj, save_path)
            self.assertTrue(os.path.isfile(save_path))
        print("[PASS] Test 3: Script to Video OK")

    def test_04_smart_reframe(self):
        scale = calculate_scale_to_fill_vertical(1920, 1080, 1080, 1920)
        self.assertAlmostEqual(scale, 1.7778, places=3)

        focal_points = [(0.0, 0.5), (3.0, 0.2), (6.0, 0.8)]
        kfs = generate_smooth_pan_keyframes(focal_points, 10.0, scale)
        self.assertGreaterEqual(len(kfs), 3)
        for k in kfs:
            # Must stay within bounds
            self.assertLessEqual(abs(k.offset_x), 0.35)

        proj = {
            "name": "Test",
            "video": {"width": 1920, "height": 1080},
            "timeline": {
                "clips": [{"kind": "Video", "duration": 5.0, "media_path": "clip.mp4"}]
            },
        }
        reframed = apply_smart_reframe_to_project(proj, focus_mode="center")
        self.assertEqual(reframed["video"]["width"], 1080)
        self.assertEqual(reframed["video"]["height"], 1920)
        self.assertEqual(reframed["timeline"]["clips"][0]["transform"]["scale"], scale)
        print("[PASS] Test 4: Smart Reframe OK")

    def test_05_capcut_bridge(self):
        self.assertEqual(sec_to_us(1.5), 1_500_000)

        concat_proj = {
            "name": "Test_CapCut_Sync",
            "video": {"width": 1080, "height": 1920, "frame_rate": 30.0},
            "timeline": {
                "duration": 4.0,
                "clips": [
                    {"kind": "video", "start": 0.0, "duration": 4.0, "media_path": "E:/vid.mp4"},
                    {"kind": "text", "start": 0.5, "duration": 2.0, "text": {"content": "Phụ đề test"}},
                    {"kind": "audio", "start": 0.0, "duration": 4.0, "media_path": "E:/voice.wav"},
                ],
            },
        }
        with tempfile.TemporaryDirectory() as tmpdir:
            draft_folder = convert_concat_to_capcut_draft(
                concat_proj, draft_name="Demo_Draft", output_folder=tmpdir
            )
            content_json = os.path.join(draft_folder, "draft_content.json")
            meta_json = os.path.join(draft_folder, "draft_meta_info.json")

            self.assertTrue(os.path.isfile(content_json))
            self.assertTrue(os.path.isfile(meta_json))

            with open(content_json, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.assertEqual(data["canvas_config"]["width"], 1080)
            self.assertEqual(data["canvas_config"]["height"], 1920)
            self.assertEqual(len(data["tracks"]), 3)
            self.assertIn("materials", data)
            self.assertEqual(len(data["materials"]["videos"]), 1)
            self.assertEqual(len(data["materials"]["texts"]), 1)
            self.assertEqual(len(data["materials"]["audios"]), 1)
        print("[PASS] Test 5: CapCut Bridge OK")


if __name__ == "__main__":
    unittest.main()
