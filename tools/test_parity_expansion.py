# SPDX-License-Identifier: AGPL-3.0-or-later
"""
Automated Test Suite for CapCut Parity Expansion Suite
Validates:
1. Vocal Isolation & Denoise Engine
2. Sound Effects (SFX) Library & Auto Transition Attachment
3. Animated Text Presets Engine (8 Motion Presets)
4. AI Face Beauty & Skin Retouching
5. Typography & Font Styling Presets
"""

import math
import os
import struct
import tempfile
import unittest
import wave

from vocal_separator import VocalSeparator
from sfx_library import ensure_sfx_assets, list_sfx, auto_attach_transition_sfx, SFX_DIR
from text_animator import PRESET_NAMES, generate_text_animation_keyframes, apply_animation_preset_to_clip
from beauty_filter import BeautyFilterSpec, is_skin_tone_rgb, apply_beauty_filter_to_timeline_clip
from typography_presets import (
    list_typography_presets,
    apply_typography_to_caption,
    batch_apply_typography_to_project,
)


class TestCapCutParityExpansion(unittest.TestCase):

    def test_01_vocal_isolation(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            in_wav = os.path.join(tmpdir, "in.wav")
            out_wav = os.path.join(tmpdir, "out.wav")
            sample_rate = 16000
            # Generate test stereo tone
            frames = []
            for i in range(sample_rate // 2):
                tone = int(math.sin(2 * math.pi * 440 * (i / sample_rate)) * 12000)
                frames.extend([tone, tone])
            with wave.open(in_wav, "wb") as wf:
                wf.setnchannels(2)
                wf.setsampwidth(2)
                wf.setframerate(sample_rate)
                wf.writeframes(struct.pack(f"<{len(frames)}h", *frames))

            # Test vocal mode
            res_vocal = VocalSeparator.process_wav(in_wav, out_wav, mode="vocal")
            self.assertTrue(os.path.isfile(out_wav))
            self.assertEqual(res_vocal["mode"], "vocal")

            # Test instrumental mode
            res_inst = VocalSeparator.process_wav(in_wav, out_wav, mode="instrumental")
            self.assertTrue(os.path.isfile(out_wav))
            self.assertEqual(res_inst["mode"], "instrumental")

            # Test denoise mode
            res_denoise = VocalSeparator.process_wav(in_wav, out_wav, mode="denoise")
            self.assertTrue(os.path.isfile(out_wav))
            self.assertEqual(res_denoise["mode"], "denoise")
        print("[PASS] Parity Test 1: Vocal Isolation, Instrumental & Denoise OK")

    def test_02_sfx_library(self):
        ensure_sfx_assets()
        sfx_items = list_sfx()
        self.assertGreaterEqual(len(sfx_items), 5)
        names = [s["id"] for s in sfx_items]
        self.assertIn("whoosh_fast.wav", names)
        self.assertIn("ding_notification.wav", names)
        self.assertIn("pop_bubble.wav", names)

        # Test auto attachment to cut points
        mock_proj = {
            "timeline": {
                "tracks": [],
                "clips": [
                    {"kind": "Video", "start": 0.0, "duration": 3.0},
                    {"kind": "Video", "start": 3.0, "duration": 4.0},
                    {"kind": "Video", "start": 7.0, "duration": 3.0},
                ],
            }
        }
        added = auto_attach_transition_sfx(mock_proj, sfx_type="whoosh_fast.wav")
        self.assertEqual(added, 2)
        sfx_clips = [c for c in mock_proj["timeline"]["clips"] if c.get("track_id") == "track_sfx_effects"]
        self.assertEqual(len(sfx_clips), 2)
        print("[PASS] Parity Test 2: SFX Library & Auto Transition Attachment OK")

    def test_03_text_animation_presets(self):
        self.assertEqual(len(PRESET_NAMES), 8)
        for name in PRESET_NAMES:
            kfs = generate_text_animation_keyframes(name, clip_duration=2.5)
            self.assertTrue(len(kfs) > 0, f"Preset {name} should have keyframes")

        sample_clip = {"id": "c1", "duration": 2.0}
        apply_animation_preset_to_clip(sample_clip, "ZoomBounce")
        self.assertEqual(sample_clip["animation_preset"], "ZoomBounce")
        self.assertIn("scale", sample_clip["keyframes"])
        print("[PASS] Parity Test 3: Animated Text Presets Engine OK")

    def test_04_beauty_filter(self):
        # Known skin tones vs background tones
        # Typical skin color RGB (220, 160, 130)
        self.assertTrue(is_skin_tone_rgb(220, 160, 130))
        # Deep blue background (20, 40, 200) -> Not skin
        self.assertFalse(is_skin_tone_rgb(20, 40, 200))

        spec = BeautyFilterSpec(smoothness=80.0, brighten=20.0)
        d = spec.to_effect_dict()
        self.assertEqual(d["id"], "beauty_retouch")
        self.assertIn("smooth_radius", d["params"])

        clip = {"id": "v1", "kind": "Video"}
        apply_beauty_filter_to_timeline_clip(clip, smoothness=75.0)
        self.assertEqual(len(clip["videoEffects"]), 1)
        self.assertEqual(clip["videoEffects"][0]["id"], "beauty_retouch")
        print("[PASS] Parity Test 4: AI Face Beauty & Skin Retouching OK")

    def test_05_typography_presets(self):
        presets = list_typography_presets()
        self.assertEqual(len(presets), 5)

        proj = {
            "timeline": {
                "clips": [
                    {"kind": "Text", "text": {"content": "Xin chào Concat"}},
                    {"kind": "Text", "text": {"content": "Phụ đề CapCut"}},
                    {"kind": "Video", "id": "v1"},
                ]
            }
        }
        updated = batch_apply_typography_to_project(proj, "TikTokViral")
        self.assertEqual(updated, 2)
        # Check uppercase & yellow color
        self.assertEqual(proj["timeline"]["clips"][0]["text"]["content"], "XIN CHÀO CONCAT")
        self.assertEqual(proj["timeline"]["clips"][0]["text"]["color"], "#FFE500")
        print("[PASS] Parity Test 5: Typography & Font Styling Presets OK")


if __name__ == "__main__":
    unittest.main()
