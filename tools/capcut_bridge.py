# SPDX-License-Identifier: AGPL-3.0-or-later
"""
CapCut Draft Converter Bridge (Concat <-> CapCut PC)
Converts Concat timelines to CapCut's native `draft_content.json` structure,
allowing rough cutting and AI captions in Concat, then instant finishing in CapCut PC.
"""

import json
import os
import time
import uuid
from typing import Any, Dict, List, Optional

def find_capcut_draft_directory() -> Optional[str]:
    """Finds CapCut PC drafts folder on Windows."""
    local_appdata = os.environ.get("LOCALAPPDATA", "")
    candidates = [
        os.path.join(local_appdata, "CapCut", "User Data", "Projects", "com.lveditor.draft"),
        os.path.join(local_appdata, "JianyingPro", "User Data", "Projects", "com.lveditor.draft"),
    ]
    for p in candidates:
        if os.path.isdir(p):
            return p
    # Default fallback
    fallback = os.path.join(local_appdata, "CapCut", "User Data", "Projects", "com.lveditor.draft")
    return fallback


def sec_to_us(seconds: float) -> int:
    """Converts seconds (float) to CapCut microseconds (integer)."""
    return int(round(seconds * 1_000_000))


def convert_concat_to_capcut_draft(
    concat_project: Dict[str, Any],
    draft_name: Optional[str] = None,
    output_folder: Optional[str] = None,
) -> str:
    """
    Translates a Concat project dictionary into CapCut PC draft files:
    - draft_content.json
    - draft_meta_info.json
    Returns the absolute path of the created CapCut draft directory.
    """
    proj_name = draft_name or concat_project.get("name", "Concat_Export")
    draft_root = output_folder or find_capcut_draft_directory()
    proj_dir = os.path.join(draft_root, proj_name)
    os.makedirs(proj_dir, exist_ok=True)

    video_cfg = concat_project.get("video", {})
    width = video_cfg.get("width", 1080)
    height = video_cfg.get("height", 1920)
    fps = float(video_cfg.get("frame_rate", 30.0))
    total_duration_sec = float(concat_project.get("timeline", {}).get("duration", 0.0))

    # Materials buckets
    materials_videos = []
    materials_audios = []
    materials_texts = []
    materials_speeds = []

    # Tracks buckets
    track_video_segments = []
    track_audio_segments = []
    track_text_segments = []

    # Map Concat clips
    for clip in concat_project.get("timeline", {}).get("clips", []):
        kind = clip.get("kind", "").lower()
        start_us = sec_to_us(clip.get("start", 0.0))
        duration_us = sec_to_us(clip.get("duration", 1.0))
        speed_id = uuid.uuid4().hex

        materials_speeds.append({
            "id": speed_id,
            "mode": 0,
            "speed": 1.0,
            "type": "speed"
        })

        if kind == "video":
            mat_id = uuid.uuid4().hex
            path = clip.get("media_path", "")
            materials_videos.append({
                "id": mat_id,
                "duration": duration_us,
                "height": height,
                "path": path,
                "type": "video",
                "width": width,
            })
            track_video_segments.append({
                "id": uuid.uuid4().hex,
                "material_id": mat_id,
                "extra_material_refs": [speed_id],
                "target_timerange": {"start": start_us, "duration": duration_us},
                "source_timerange": {"start": 0, "duration": duration_us},
            })

        elif kind == "audio":
            mat_id = uuid.uuid4().hex
            path = clip.get("media_path", "")
            materials_audios.append({
                "id": mat_id,
                "duration": duration_us,
                "path": path,
                "type": "audio",
                "name": clip.get("name", "Audio"),
            })
            track_audio_segments.append({
                "id": uuid.uuid4().hex,
                "material_id": mat_id,
                "extra_material_refs": [speed_id],
                "target_timerange": {"start": start_us, "duration": duration_us},
                "source_timerange": {"start": 0, "duration": duration_us},
            })

        elif kind in ("text", "caption"):
            mat_id = uuid.uuid4().hex
            raw_text = clip.get("text", {}).get("content", clip.get("text_content", ""))
            # CapCut text material stores content as serialized JSON string
            text_payload = json.dumps({"text": raw_text}, ensure_ascii=False)
            materials_texts.append({
                "id": mat_id,
                "content": text_payload,
                "font_size": 15.0,
                "type": "text",
                "typesetting": 0,
            })
            track_text_segments.append({
                "id": uuid.uuid4().hex,
                "material_id": mat_id,
                "extra_material_refs": [speed_id],
                "target_timerange": {"start": start_us, "duration": duration_us},
                "source_timerange": {"start": 0, "duration": duration_us},
            })

    # Build CapCut tracks list
    tracks = []
    if track_video_segments:
        tracks.append({
            "id": uuid.uuid4().hex,
            "type": "video",
            "segments": track_video_segments,
            "attribute": 0,
            "flag": 0,
        })
    if track_audio_segments:
        tracks.append({
            "id": uuid.uuid4().hex,
            "type": "audio",
            "segments": track_audio_segments,
            "attribute": 0,
            "flag": 0,
        })
    if track_text_segments:
        tracks.append({
            "id": uuid.uuid4().hex,
            "type": "text",
            "segments": track_text_segments,
            "attribute": 0,
            "flag": 0,
        })

    # Assemble draft_content.json
    draft_content = {
        "canvas_config": {
            "height": height,
            "ratio": "original",
            "width": width,
        },
        "color_space": 0,
        "config": {
            "adjust_max_index": 1,
            "attachment_info": [],
            "combination_max_index": 1,
            "export_range": None,
            "extract_audio_last_index": 1,
            "lyrics_recognition_id": "",
            "lyrics_sync": True,
            "lyrics_taskinfo": [],
            "maintrack_adsorb": True,
            "material_save_mode": 0,
            "original_sound_last_index": 1,
            "record_audio_last_index": 1,
            "sticker_max_index": 1,
            "subtitle_keywords_config": None,
            "subtitle_recognition_id": "",
            "subtitle_sync": True,
            "subtitle_taskinfo": [],
            "system_font_list": [],
            "video_mute": False,
            "zoom_info_params": None,
        },
        "duration": sec_to_us(total_duration_sec),
        "fps": fps,
        "id": uuid.uuid4().hex,
        "materials": {
            "audio_balances": [],
            "audio_effects": [],
            "audio_fades": [],
            "audios": materials_audios,
            "speeds": materials_speeds,
            "texts": materials_texts,
            "transitions": [],
            "video_effects": [],
            "video_trackings": [],
            "videos": materials_videos,
        },
        "mutable_config": None,
        "name": proj_name,
        "new_version": "120.0.0",
        "relationships": [],
        "tracks": tracks,
        "update_time": int(time.time()),
        "version": 360000,
    }

    content_path = os.path.join(proj_dir, "draft_content.json")
    with open(content_path, "w", encoding="utf-8") as f:
        json.dump(draft_content, f, indent=2, ensure_ascii=False)

    # Assemble draft_meta_info.json
    now_ms = int(time.time() * 1000)
    meta_info = {
        "draft_id": uuid.uuid4().hex,
        "draft_name": proj_name,
        "draft_root_path": proj_dir.replace("\\", "/"),
        "tm_draft_create": now_ms,
        "tm_draft_modified": now_ms,
        "draft_fold_path": proj_dir.replace("\\", "/"),
        "draft_timeline_materials_size_": 0,
    }
    meta_path = os.path.join(proj_dir, "draft_meta_info.json")
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta_info, f, indent=2, ensure_ascii=False)

    return proj_dir


if __name__ == "__main__":
    sample_concat = {
        "name": "Concat_To_CapCut_Demo",
        "video": {"width": 1080, "height": 1920, "frame_rate": 30.0},
        "timeline": {
            "duration": 6.0,
            "clips": [
                {
                    "kind": "video",
                    "start": 0.0,
                    "duration": 6.0,
                    "media_path": "E:/test.mp4",
                },
                {
                    "kind": "text",
                    "start": 0.5,
                    "duration": 2.5,
                    "text": {"content": "Phụ đề xuất sang CapCut!"},
                },
            ],
        },
    }
    out = convert_concat_to_capcut_draft(sample_concat, "CapCut_Export_Test")
    print("Exported CapCut draft successfully to:", out)
