# SPDX-License-Identifier: AGPL-3.0-or-later
"""
Typography & Vietnamese Font Styling Presets (CapCut Style)
Provides trending title and subtitle styles with optimized Vietnamese font families,
strokes, outlines, glows, and shadow backdrops.
"""

from typing import Any, Dict, List, Optional

TYPOGRAPHY_PRESETS: Dict[str, Dict[str, Any]] = {
    "TikTokViral": {
        "name": "TikTok & Shorts Viral (Hormozi)",
        "font_family": "Montserrat",
        "font_size": 68.0,
        "color": "#FFE500",
        "outline_color": "#000000",
        "outline_width": 5.0,
        "bold": True,
        "uppercase": True,
        "shadow_color": "#00000080",
        "shadow_blur": 6.0,
    },
    "CinematicModern": {
        "name": "Cinematic Film Subtitle",
        "font_family": "Be Vietnam Pro",
        "font_size": 52.0,
        "color": "#FFFFFF",
        "outline_color": "#000000",
        "outline_width": 2.5,
        "bold": False,
        "uppercase": False,
        "shadow_color": "#000000B0",
        "shadow_blur": 4.0,
    },
    "NewsBreaking": {
        "name": "Breaking News Headline",
        "font_family": "Arial",
        "font_size": 60.0,
        "color": "#FFFFFF",
        "background": "#D32F2F",
        "outline_color": "#800000",
        "outline_width": 2.0,
        "bold": True,
        "uppercase": True,
        "shadow_blur": 0.0,
    },
    "RetroVaporwave": {
        "name": "Retro 80s Synthwave",
        "font_family": "Montserrat",
        "font_size": 64.0,
        "color": "#FF77FF",
        "outline_color": "#00F0FF",
        "outline_width": 4.0,
        "bold": True,
        "uppercase": True,
        "shadow_color": "#8A2BE2",
        "shadow_blur": 12.0,
    },
    "MinimalistClean": {
        "name": "Minimalist Glassmorphism",
        "font_family": "Inter",
        "font_size": 48.0,
        "color": "#F0F0F0",
        "background": "#00000070",
        "outline_color": "#00000000",
        "outline_width": 0.0,
        "bold": False,
        "uppercase": False,
        "shadow_blur": 2.0,
    },
}


def list_typography_presets() -> List[Dict[str, Any]]:
    """Returns available typography presets."""
    return [{"id": k, **v} for k, v in TYPOGRAPHY_PRESETS.items()]


def apply_typography_to_caption(clip: Dict[str, Any], preset_name: str = "TikTokViral") -> Dict[str, Any]:
    """Applies a typography preset to a Concat text/caption clip."""
    preset = TYPOGRAPHY_PRESETS.get(preset_name, TYPOGRAPHY_PRESETS["TikTokViral"])
    text_data = clip.setdefault("text", {})

    content = text_data.get("content", clip.get("text_content", ""))
    if preset.get("uppercase"):
        content = content.upper()

    text_data["content"] = content
    text_data["font_family"] = preset["font_family"]
    text_data["font_size"] = preset["font_size"]
    text_data["color"] = preset["color"]
    text_data["outline_color"] = preset["outline_color"]
    text_data["outline_width"] = preset["outline_width"]
    text_data["bold"] = preset["bold"]

    if "background" in preset:
        text_data["background"] = preset["background"]
    if "shadow_color" in preset:
        text_data["shadow_color"] = preset["shadow_color"]

    return clip


def batch_apply_typography_to_project(project_doc: Dict[str, Any], preset_name: str = "TikTokViral") -> int:
    """Updates all text and caption clips in a project to the selected typography preset."""
    count = 0
    for clip in project_doc.get("timeline", {}).get("clips", []):
        if clip.get("kind") in ("Text", "text", "caption"):
            apply_typography_to_caption(clip, preset_name)
            count += 1
    return count


if __name__ == "__main__":
    presets = list_typography_presets()
    print(f"Loaded {len(presets)} Typography Presets:")
    for p in presets:
        print(f"  - [{p['id']}] {p['name']} ({p['font_family']}, {p['color']})")
