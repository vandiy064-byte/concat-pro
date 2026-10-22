# SPDX-License-Identifier: AGPL-3.0-or-later
"""
Smart Reframing Engine (16:9 to 9:16)
Automatically adapts horizontal landscape video to vertical portrait format for TikTok / Reels / Shorts,
keeping speakers and main action centered with smooth keyframed camera pans.
"""

import json
import math
from typing import Any, Dict, List, Optional, Tuple

class KeyframePoint:
    def __init__(self, time_sec: float, offset_x: float, scale: float = 1.7778):
        self.time_sec = float(time_sec)
        self.offset_x = float(offset_x)  # Normalized offset (-0.5 to 0.5)
        self.scale = float(scale)

    def to_dict(self) -> Dict[str, Any]:
        return {"time": self.time_sec, "offset_x": self.offset_x, "scale": self.scale}


def calculate_scale_to_fill_vertical(src_w: int = 1920, src_h: int = 1080, target_w: int = 1080, target_h: int = 1920) -> float:
    """Calculates zoom multiplier required so horizontal video completely fills vertical height."""
    scale_y = float(target_h) / float(src_h)
    return round(scale_y, 4)


def generate_smooth_pan_keyframes(
    focal_points: List[Tuple[float, float]],  # List of (time_in_seconds, focal_center_x_normalized_0_to_1)
    clip_duration: float,
    scale: float = 1.7778,
    max_pan_speed: float = 0.25,  # Max offset shift per second to keep panning cinematic
) -> List[KeyframePoint]:
    """
    Transforms detected speaker positions into smooth, cinematic camera pan keyframes.
    focal_center_x: 0.0 is leftmost edge, 0.5 is middle, 1.0 is rightmost edge of 16:9 video.
    """
    if not focal_points:
        return [
            KeyframePoint(0.0, 0.0, scale),
            KeyframePoint(clip_duration, 0.0, scale),
        ]

    # Convert center coordinates (0..1) to normalized offset (-0.34..+0.34)
    # When focal_center is 0.5 (middle), offset_x = 0.0.
    # When focal_center is 0.2 (left), we need to shift right (+offset) to center it.
    raw_keyframes = []
    for t, center_x in focal_points:
        desired_offset = (0.5 - center_x) * (scale - 1.0) / scale
        # Clamp to bounds so black borders never appear
        max_bound = (scale - 1.0) / (2.0 * scale)
        clamped_offset = max(-max_bound, min(max_bound, desired_offset))
        raw_keyframes.append((t, clamped_offset))

    # Smooth out keyframes to avoid jarring camera twitches
    smoothed: List[KeyframePoint] = []
    last_t, last_offset = raw_keyframes[0]
    smoothed.append(KeyframePoint(last_t, last_offset, scale))

    for t, target_offset in raw_keyframes[1:]:
        dt = max(0.001, t - last_t)
        max_shift = max_pan_speed * dt
        diff = target_offset - last_offset

        if abs(diff) > max_shift:
            actual_offset = last_offset + math.copysign(max_shift, diff)
        else:
            actual_offset = target_offset

        smoothed.append(KeyframePoint(t, round(actual_offset, 4), scale))
        last_t, last_offset = t, actual_offset

    # Ensure last keyframe reaches end of clip
    if smoothed[-1].time_sec < clip_duration:
        smoothed.append(KeyframePoint(clip_duration, smoothed[-1].offset_x, scale))

    return smoothed


def apply_smart_reframe_to_project(
    project_doc: Dict[str, Any],
    focus_mode: str = "center",  # 'center', 'left', 'right', or 'auto'
) -> Dict[str, Any]:
    """
    Updates a Concat project to 1080x1920 (9:16) and adjusts video clips.
    """
    project_doc["video"]["width"] = 1080
    project_doc["video"]["height"] = 1920
    scale = calculate_scale_to_fill_vertical()

    default_offsets = {
        "center": 0.0,
        "left": 0.18,
        "right": -0.18,
    }
    offset_x = default_offsets.get(focus_mode, 0.0)

    for clip in project_doc.get("timeline", {}).get("clips", []):
        if clip.get("kind") == "Video":
            clip["transform"] = {
                "scale": scale,
                "offset_x": offset_x,
                "offset_y": 0.0,
            }
            # Add keyframes for dynamic camera centering
            clip["keyframes"] = {
                "offset_x": [
                    {"time": 0.0, "value": offset_x},
                    {"time": clip.get("duration", 5.0), "value": offset_x},
                ],
                "scale": [
                    {"time": 0.0, "value": scale},
                ],
            }

    return project_doc


if __name__ == "__main__":
    sample_detections = [(0.0, 0.5), (2.0, 0.3), (4.5, 0.7), (8.0, 0.5)]
    kfs = generate_smooth_pan_keyframes(sample_detections, 10.0)
    print(f"Generated {len(kfs)} smart reframe keyframes:")
    for k in kfs:
        print(f"  t={k.time_sec:.1f}s: offset_x={k.offset_x:+.4f}, scale={k.scale:.3f}")
