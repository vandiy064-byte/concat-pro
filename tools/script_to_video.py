# SPDX-License-Identifier: AGPL-3.0-or-later
"""
Script-to-Video Engine for Concat
Converts a text script into a fully assembled video timeline with TTS narration,
synchronized subtitles, B-roll visuals, and background music ducking.
"""

import json
import os
import re
import uuid
from typing import Any, Dict, List, Optional

def split_script_into_sentences(text: str) -> List[str]:
    """Splits text/markdown into clean spoken sentences, stripping markdown headers/bullets."""
    lines = text.strip().splitlines()
    cleaned_lines = []
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        line = re.sub(r"^[-*•\d.]+\s*", "", line)  # remove list bullets
        cleaned_lines.append(line)
    
    full_text = " ".join(cleaned_lines)
    # Split on sentence boundaries
    parts = re.split(r"(?<=[.!?…\n])\s+", full_text)
    return [p.strip() for p in parts if len(p.strip()) > 1]


def estimate_sentence_duration(sentence: str, words_per_minute: float = 140.0) -> float:
    """Estimates duration in seconds based on word count when audio file is simulated or pending."""
    words = len(sentence.split())
    # Base duration + punctuation pause
    duration = (words / words_per_minute) * 60.0
    return max(1.5, round(duration, 2))


def assemble_script_to_timeline(
    script_text: str,
    project_name: str = "Script_Video_Auto",
    media_files: Optional[List[str]] = None,
    music_path: Optional[str] = None,
    voice_name: str = "vi-VN-HoaiMyNeural",
    canvas_w: int = 1080,
    canvas_h: int = 1920,
) -> Dict[str, Any]:
    """
    Builds a complete Concat project timeline dictionary from script sentences.
    """
    sentences = split_script_into_sentences(script_text)
    if not sentences:
        raise ValueError("Script contains no readable sentences.")

    tracks = [
        {"id": "track_video_main", "kind": "Video", "name": "B-Roll Visuals"},
        {"id": "track_captions", "kind": "Text", "name": "Subtitles"},
        {"id": "track_voice", "kind": "Audio", "name": "Voiceover Narration"},
    ]
    if music_path:
        tracks.append({"id": "track_bgm", "kind": "Audio", "name": "Background Music"})

    clips: List[Dict[str, Any]] = []
    current_time = 0.0
    broll_idx = 0
    available_media = media_files or []

    for i, sentence in enumerate(sentences):
        duration = estimate_sentence_duration(sentence)
        clip_id_voice = f"voice_{i+1:03d}_{uuid.uuid4().hex[:6]}"
        clip_id_caption = f"sub_{i+1:03d}_{uuid.uuid4().hex[:6]}"
        clip_id_visual = f"visual_{i+1:03d}_{uuid.uuid4().hex[:6]}"

        # 1. Voice clip
        clips.append({
            "id": clip_id_voice,
            "track_id": "track_voice",
            "start": current_time,
            "duration": duration,
            "kind": "Audio",
            "name": f"TTS {i+1}",
            "text_content": sentence,
            "voice": voice_name,
        })

        # 2. Caption clip
        clips.append({
            "id": clip_id_caption,
            "track_id": "track_captions",
            "start": current_time,
            "duration": duration,
            "kind": "Text",
            "name": f"Sub {i+1}",
            "text": {
                "content": sentence,
                "font_family": "Montserrat",
                "font_size": 64.0,
                "color": "#FFFFFF",
                "outline_color": "#000000",
                "outline_width": 3.5,
                "bold": True,
            },
        })

        # 3. B-Roll visual clip
        media_src = available_media[broll_idx % len(available_media)] if available_media else "default_background"
        clips.append({
            "id": clip_id_visual,
            "track_id": "track_video_main",
            "start": current_time,
            "duration": duration,
            "kind": "Video",
            "media_path": media_src,
            "name": f"B-Roll {i+1}",
        })
        broll_idx += 1
        current_time += duration

    # 4. Background music track with volume ducking
    total_duration = current_time
    if music_path:
        clips.append({
            "id": f"bgm_{uuid.uuid4().hex[:6]}",
            "track_id": "track_bgm",
            "start": 0.0,
            "duration": total_duration,
            "kind": "Audio",
            "media_path": music_path,
            "name": "Background Music",
            "volume": 0.15,  # Ducked volume
        })

    project_doc = {
        "version": 1,
        "name": project_name,
        "video": {
            "width": canvas_w,
            "height": canvas_h,
            "frame_rate": 30.0,
        },
        "timeline": {
            "tracks": tracks,
            "clips": clips,
            "duration": total_duration,
        },
    }
    return project_doc


def save_concat_project_file(project_doc: Dict[str, Any], output_path: str) -> str:
    """Saves assembled project to Concat project directory."""
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(project_doc, f, indent=2, ensure_ascii=False)
    return output_path


if __name__ == "__main__":
    sample_script = """
    # Bí quyết xây dựng kênh video ngắn
    Chào bạn! Để video của bạn có nhiều lượt xem, 3 giây đầu tiên là quan trọng nhất.
    Hãy sử dụng tiêu đề thu hút và hình ảnh bắt mắt ngay lập tức.
    Đừng quên sử dụng phụ đề nhảy chữ sinh động để giữ chân người xem đến giây cuối cùng!
    """
    proj = assemble_script_to_timeline(sample_script, "Demo_Shorts")
    print(f"Project '{proj['name']}' assembled:")
    print(f"Canvas: {proj['video']['width']}x{proj['video']['height']}")
    print(f"Total duration: {proj['timeline']['duration']:.1f}s, Clips: {len(proj['timeline']['clips'])}")
