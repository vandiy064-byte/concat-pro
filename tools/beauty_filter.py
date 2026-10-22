# SPDX-License-Identifier: AGPL-3.0-or-later
"""
Face Beauty & Skin Retouching Filter (CapCut Style)
Applies edge-preserving skin tone smoothing, blemishes reduction,
and subtle luminance enhancement while keeping eyes and mouth razor sharp.
"""

from typing import Any, Dict, List, Optional, Tuple

class BeautyFilterSpec:
    def __init__(
        self,
        smoothness: float = 65.0,  # 0 to 100
        brighten: float = 15.0,    # 0 to 100
        tone_warmth: float = 5.0,  # 0 to 100
    ):
        self.smoothness = max(0.0, min(100.0, float(smoothness)))
        self.brighten = max(0.0, min(100.0, float(brighten)))
        self.tone_warmth = max(0.0, min(100.0, float(tone_warmth)))

    def to_effect_dict(self) -> Dict[str, Any]:
        """Maps parameters to Concat/FFmpeg effect chain shader specifications."""
        # Bilateral / surface blur radius and spatial sigma
        radius = int(round((self.smoothness / 100.0) * 8.0))
        sigma = round(0.1 + (self.smoothness / 100.0) * 0.4, 2)
        gamma = round(1.0 - (self.brighten / 100.0) * 0.15, 3)

        return {
            "id": "beauty_retouch",
            "name": "AI Skin Beauty & Smoothing",
            "params": {
                "smooth_radius": radius,
                "edge_retention_sigma": sigma,
                "luminance_gamma": gamma,
                "warmth_tint": round(self.tone_warmth / 100.0 * 0.08, 3),
            },
            "enabled": True,
        }


def is_skin_tone_rgb(r: int, g: int, b: int) -> bool:
    """
    Classifies whether an RGB pixel falls into universal human skin chromaticity.
    Uses peer-reviewed YCbCr / RGB skin color distribution rule.
    """
    # Basic bounding condition in RGB
    if not (r > 60 and g > 40 and b > 20 and (r > g) and (r > b) and (abs(r - g) > 10)):
        return False
    # Color difference rule
    y = 0.299 * r + 0.587 * g + 0.114 * b
    cr = (r - y) * 0.713 + 128
    cb = (b - y) * 0.564 + 128
    return (133 <= cr <= 173) and (77 <= cb <= 127)


def apply_beauty_filter_to_timeline_clip(clip: Dict[str, Any], smoothness: float = 65.0) -> Dict[str, Any]:
    """Adds beauty retouch effect to a Concat video clip."""
    spec = BeautyFilterSpec(smoothness=smoothness)
    effects = clip.setdefault("videoEffects", [])
    # Remove previous beauty effect if present
    clip["videoEffects"] = [e for e in effects if e.get("id") != "beauty_retouch"]
    clip["videoEffects"].append(spec.to_effect_dict())
    return clip


if __name__ == "__main__":
    spec = BeautyFilterSpec(smoothness=70.0, brighten=20.0)
    print("Beauty Filter Spec:", spec.to_effect_dict())
    sample_clip = {"id": "vid_1", "kind": "Video"}
    apply_beauty_filter_to_timeline_clip(sample_clip)
    print("Clip with beauty effect applied:", sample_clip["videoEffects"])
