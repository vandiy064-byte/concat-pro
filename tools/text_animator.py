# SPDX-License-Identifier: AGPL-3.0-or-later
"""
Animated Text Presets Engine for Concat (CapCut Style)
Generates keyframed motion graphics for title and caption clips:
- Typewriter, ZoomBounce, FadeSlideUp, NeonGlow, WavePulse, GlitchShake, CinematicFade, HormoziPop.
"""

from typing import Any, Dict, List, Optional

PRESET_NAMES = [
    "ZoomBounce",
    "Typewriter",
    "FadeSlideUp",
    "NeonGlow",
    "WavePulse",
    "GlitchShake",
    "CinematicFade",
    "HormoziPop",
]

def generate_text_animation_keyframes(
    preset: str,
    clip_duration: float,
    base_scale: float = 1.0,
    base_offset_y: float = 0.35,
) -> Dict[str, List[Dict[str, Any]]]:
    """
    Computes keyframe tracks (scale, opacity, offset_x, offset_y, outline) for the given preset.
    Times are normalized fractions (0.0 to 1.0) of the clip's duration.
    """
    p = preset.lower()
    dur = max(0.2, clip_duration)
    # intro transition takes at most 0.3s or 25% of clip
    intro_frac = min(0.35, 0.25 / dur)

    keyframes: Dict[str, List[Dict[str, Any]]] = {}

    if p == "zoombounce":
        # 0 -> 0.7x, intro_frac/2 -> 1.18x (punch), intro_frac -> 1.0x
        t_peak = intro_frac * 0.6
        keyframes["scale"] = [
            {"time": 0.0, "value": base_scale * 0.5, "ease": [0.25, 0.1, 0.25, 1.0]},
            {"time": t_peak, "value": base_scale * 1.18, "ease": [0.25, 0.1, 0.25, 1.0]},
            {"time": intro_frac, "value": base_scale * 1.0},
            {"time": 1.0, "value": base_scale * 1.0},
        ]
        keyframes["opacity"] = [
            {"time": 0.0, "value": 0.0},
            {"time": t_peak, "value": 1.0},
            {"time": 1.0, "value": 1.0},
        ]

    elif p == "fadeslideup":
        # Slides from below (+0.08 offset) and fades in
        keyframes["offset_y"] = [
            {"time": 0.0, "value": base_offset_y + 0.08, "ease": [0.0, 0.0, 0.2, 1.0]},
            {"time": intro_frac, "value": base_offset_y},
            {"time": 1.0 - intro_frac * 0.5, "value": base_offset_y},
            {"time": 1.0, "value": base_offset_y - 0.04},
        ]
        keyframes["opacity"] = [
            {"time": 0.0, "value": 0.0},
            {"time": intro_frac, "value": 1.0},
            {"time": 1.0 - intro_frac * 0.5, "value": 1.0},
            {"time": 1.0, "value": 0.0},
        ]

    elif p == "neonglow":
        # Pulses scale and outline
        keyframes["scale"] = [
            {"time": 0.0, "value": base_scale * 0.95},
            {"time": 0.25, "value": base_scale * 1.06},
            {"time": 0.5, "value": base_scale * 0.98},
            {"time": 0.75, "value": base_scale * 1.04},
            {"time": 1.0, "value": base_scale * 1.0},
        ]
        keyframes["opacity"] = [
            {"time": 0.0, "value": 0.8},
            {"time": 0.25, "value": 1.0},
            {"time": 0.5, "value": 0.85},
            {"time": 0.75, "value": 1.0},
            {"time": 1.0, "value": 0.9},
        ]

    elif p == "glitchshake":
        # Rapid jitter in horizontal position
        keyframes["offset_x"] = [
            {"time": 0.0, "value": 0.0},
            {"time": 0.05, "value": -0.015},
            {"time": 0.10, "value": 0.02},
            {"time": 0.15, "value": -0.01},
            {"time": 0.20, "value": 0.0},
            {"time": 1.0, "value": 0.0},
        ]
        keyframes["opacity"] = [
            {"time": 0.0, "value": 0.4},
            {"time": 0.05, "value": 1.0},
            {"time": 0.10, "value": 0.7},
            {"time": 0.15, "value": 1.0},
            {"time": 1.0, "value": 1.0},
        ]

    elif p == "wavepulse":
        # Breathing pulse throughout
        keyframes["scale"] = [
            {"time": 0.0, "value": base_scale * 0.96},
            {"time": 0.5, "value": base_scale * 1.05},
            {"time": 1.0, "value": base_scale * 0.96},
        ]

    elif p == "cinematicfade":
        # Slow elegant fade
        keyframes["opacity"] = [
            {"time": 0.0, "value": 0.0},
            {"time": 0.25, "value": 1.0},
            {"time": 0.75, "value": 1.0},
            {"time": 1.0, "value": 0.0},
        ]

    elif p == "hormozipop":
        # Instant pop in with bold scale punch
        keyframes["scale"] = [
            {"time": 0.0, "value": base_scale * 0.8},
            {"time": intro_frac * 0.5, "value": base_scale * 1.15},
            {"time": intro_frac, "value": base_scale * 1.0},
            {"time": 1.0, "value": base_scale * 1.0},
        ]

    else:  # typewriter fallback
        keyframes["opacity"] = [
            {"time": 0.0, "value": 0.0},
            {"time": 0.05, "value": 1.0},
            {"time": 1.0, "value": 1.0},
        ]

    return keyframes


def apply_animation_preset_to_clip(clip: Dict[str, Any], preset_name: str) -> Dict[str, Any]:
    """Applies an animation preset's keyframes to a Concat text/caption clip."""
    dur = float(clip.get("duration", 2.0))
    kfs = generate_text_animation_keyframes(preset_name, dur)
    clip["keyframes"] = kfs
    clip["animation_preset"] = preset_name
    return clip


if __name__ == "__main__":
    kfs = generate_text_animation_keyframes("ZoomBounce", 2.0)
    print("ZoomBounce Keyframes Generated:")
    for prop, keys in kfs.items():
        print(f"  Property '{prop}': {len(keys)} keyframe points")
