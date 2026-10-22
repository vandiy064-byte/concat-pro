# SPDX-License-Identifier: AGPL-3.0-or-later
"""
Karaoke & Word-by-Word Subtitle Generator (TikTok / CapCut / Hormozi Style)
Generates high-engagement bouncing & highlighted subtitles from speech.
"""

import json
import math
import os
from typing import Any, Dict, List, Optional, Tuple

class WordTiming:
    def __init__(self, word: str, start: f64 if False else float, end: float):
        self.word = word.strip()
        self.start = float(start)
        self.end = float(end)

    def to_dict(self) -> Dict[str, Any]:
        return {"word": self.word, "start": self.start, "end": self.end}


class KaraokeSentence:
    def __init__(self, words: List[WordTiming]):
        self.words = words
        self.start = words[0].start if words else 0.0
        self.end = words[-1].end if words else 0.0
        self.text = " ".join(w.word for w in words)


def group_words_into_phrases(words: List[WordTiming], max_words_per_line: int = 5, max_duration: float = 2.5) -> List[KaraokeSentence]:
    """Groups a stream of word timestamps into readable short video phrases (3-6 words per line)."""
    phrases: List[KaraokeSentence] = []
    current: List[WordTiming] = []

    for w in words:
        if not current:
            current.append(w)
            continue

        phrase_duration = w.end - current[0].start
        has_punctuation = current[-1].word.endswith((".", "!", "?", ",", ";", ":"))

        if len(current) >= max_words_per_line or phrase_duration >= max_duration or (has_punctuation and len(current) >= 3):
            phrases.append(KaraokeSentence(current))
            current = [w]
        else:
            current.append(w)

    if current:
        phrases.append(KaraokeSentence(current))

    return phrases


def render_ass_karaoke(phrases: List[KaraokeSentence], highlight_color: str = "&H00E5FF00&", base_color: str = "&H00FFFFFF&") -> str:
    """Renders Advanced SubStation Alpha (.ass) format with karaoke tags {\\k}."""
    lines = [
        "[Script Info]",
        "ScriptType: v4.00+",
        "PlayResX: 1080",
        "PlayResY: 1920",
        "",
        "[V4+ Styles]",
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
        f"Style: Hormozi,Arial Black,76,{base_color},{highlight_color},&H00000000,&H80000000,1,0,0,0,100,100,2,0,1,6,2,2,40,40,240,1",
        "",
        "[Events]",
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"
    ]

    def format_ts(sec: float) -> str:
        h = int(sec // 3600)
        m = int((sec % 3600) // 60)
        s = int(sec % 60)
        cs = int(round((sec - math.floor(sec)) * 100))
        return f"{h:d}:{m:02d}:{s:02d}.{cs:02d}"

    for phrase in phrases:
        k_text = ""
        for w in phrase.words:
            duration_cs = max(1, int(round((w.end - w.start) * 100)))
            k_text += f"{{\\k{duration_cs}}}{w.word.upper()} "

        start_s = format_ts(phrase.start)
        end_s = format_ts(phrase.end)
        lines.append(f"Dialogue: 0,{start_s},{end_s},Hormozi,,0,0,0,,{k_text.strip()}")

    return "\n".join(lines) + "\n"


def generate_word_clips_for_timeline(phrases: List[KaraokeSentence], highlight_hex: str = "#FFE500", normal_hex: str = "#FFFFFF") -> List[Dict[str, Any]]:
    """
    Creates individual word-level text clips for Concat timeline tracks.
    Each clip shows the full phrase, but highlights the active word at that precise moment.
    """
    clips: List[Dict[str, Any]] = []
    for phrase in phrases:
        for idx, current_word in enumerate(phrase.words):
            duration = max(0.1, current_word.end - current_word.start)
            # Build text where current word is emphasized
            styled_content = " ".join(
                f"[{w.word.upper()}]" if i == idx else w.word.upper()
                for i, w in enumerate(phrase.words)
            )

            clips.append({
                "start": current_word.start,
                "duration": duration,
                "text": {
                    "content": styled_content,
                    "font_family": "Montserrat",
                    "font_size": 72.0,
                    "color": highlight_hex,
                    "outline_color": "#000000",
                    "outline_width": 4.0,
                    "bold": True,
                },
                "active_word": current_word.word,
                "phrase": phrase.text
            })
    return clips


def format_srt_timestamp(seconds: float) -> str:
    """Formats seconds to SubRip timestamp format HH:MM:SS,mmm."""
    millis = int(round(max(0.0, seconds) * 1000.0))
    hours = millis // 3600000
    minutes = (millis // 60000) % 60
    secs = (millis // 1000) % 60
    ms = millis % 1000
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{ms:03d}"


def export_timeline_to_srt(clips_or_timeline: Any, output_path: Optional[str] = None) -> str:
    """
    Extracts text clips from a Concat project timeline or list of clips
    and formats them as standard SubRip (.srt) subtitle string.
    Optionally writes directly to output_path.
    """
    if isinstance(clips_or_timeline, dict):
        clips = clips_or_timeline.get("timeline", {}).get("clips", [])
        if not clips:
            clips = clips_or_timeline.get("clips", [])
    elif isinstance(clips_or_timeline, list):
        clips = clips_or_timeline
    else:
        clips = []

    text_clips = [
        c for c in clips
        if (c.get("kind") == "Text" or "text" in c) and c.get("text", {}).get("content")
    ]
    # Sort clips chronologically
    text_clips.sort(key=lambda c: float(c.get("start", 0.0)))

    srt_entries = []
    for idx, c in enumerate(text_clips, start=1):
        start = float(c.get("start", 0.0))
        duration = float(c.get("duration", 2.0))
        end = start + duration
        content = c.get("text", {}).get("content", "").strip()

        entry = f"{idx}\n{format_srt_timestamp(start)} --> {format_srt_timestamp(end)}\n{content}\n"
        srt_entries.append(entry)

    srt_body = "\n".join(srt_entries) + "\n"

    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(srt_body)

    return srt_body


if __name__ == "__main__":
    sample_words = [
        WordTiming("Chào", 0.0, 0.3),
        WordTiming("mừng", 0.3, 0.6),
        WordTiming("bạn", 0.6, 0.8),
        WordTiming("đến", 0.8, 1.1),
        WordTiming("với", 1.1, 1.3),
        WordTiming("kênh", 1.3, 1.7),
        WordTiming("chúng", 2.0, 2.3),
        WordTiming("tôi", 2.3, 2.7),
    ]
    phrases = group_words_into_phrases(sample_words, max_words_per_line=4)
    ass_content = render_ass_karaoke(phrases)
    print("Rendered ASS sample lines:")
    print("\n".join(ass_content.splitlines()[-3:]))
    timeline_clips = generate_word_clips_for_timeline(phrases)
    print(f"Generated {len(timeline_clips)} word clips for timeline.")
