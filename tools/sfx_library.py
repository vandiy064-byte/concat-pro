# SPDX-License-Identifier: AGPL-3.0-or-later
"""
Built-in Sound Effects (SFX) Library for Concat
Generates, organizes, and auto-places transition sound effects (Whoosh, Ding, Pop, Glitch, Impact)
onto Concat timeline cut points.
"""

import math
import os
import random
import struct
import uuid
import wave
from typing import Any, Dict, List, Optional

SFX_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "sfx"))

def ensure_sfx_assets() -> None:
    """Ensures standard built-in SFX files exist in the assets directory."""
    os.makedirs(SFX_DIR, exist_ok=True)
    sample_rate = 44100

    def write_wav(filename: str, samples: List[int]):
        path = os.path.join(SFX_DIR, filename)
        if not os.path.isfile(path):
            with wave.open(path, "wb") as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(sample_rate)
                wf.writeframes(struct.pack(f"<{len(samples)}h", *samples))

    # 1. Whoosh transition (Frequency sweep down with noise)
    whoosh_samples = []
    dur = 0.35
    total = int(sample_rate * dur)
    for i in range(total):
        progress = i / total
        # Frequency rises then drops
        freq = 300 + 1200 * math.sin(progress * math.pi)
        env = math.sin(progress * math.pi) ** 2
        noise = (random.random() * 2 - 1) * 0.4
        tone = math.sin(2 * math.pi * freq * (i / sample_rate)) * 0.6
        val = int((tone + noise) * env * 24000)
        whoosh_samples.append(max(-32768, min(32767, val)))
    write_wav("whoosh_fast.wav", whoosh_samples)

    # 2. Ding notification (Pure bell harmonic decay)
    ding_samples = []
    dur = 0.6
    total = int(sample_rate * dur)
    for i in range(total):
        t = i / sample_rate
        decay = math.exp(-t * 6.0)
        tone = (
            math.sin(2 * math.pi * 1760 * t) * 0.7
            + math.sin(2 * math.pi * 3520 * t) * 0.3
        )
        val = int(tone * decay * 28000)
        ding_samples.append(max(-32768, min(32767, val)))
    write_wav("ding_notification.wav", ding_samples)

    # 3. Pop bubble (Quick pitch rise and drop)
    pop_samples = []
    dur = 0.12
    total = int(sample_rate * dur)
    for i in range(total):
        t = i / sample_rate
        p = i / total
        freq = 400 + 900 * p
        decay = math.exp(-p * 8.0)
        tone = math.sin(2 * math.pi * freq * t)
        val = int(tone * decay * 26000)
        pop_samples.append(max(-32768, min(32767, val)))
    write_wav("pop_bubble.wav", pop_samples)

    # 4. Glitch digital (Random frequency steps with distortion)
    glitch_samples = []
    dur = 0.25
    total = int(sample_rate * dur)
    for i in range(total):
        t = i / sample_rate
        f = 200 + ((i // 400) % 7) * 450
        val = int(math.sin(2 * math.pi * f * t) * 20000)
        if random.random() < 0.15:
            val = random.randint(-25000, 25000)
        glitch_samples.append(max(-32768, min(32767, val)))
    write_wav("glitch_digital.wav", glitch_samples)

    # 5. Bass Impact (Sub-bass drop)
    impact_samples = []
    dur = 0.8
    total = int(sample_rate * dur)
    for i in range(total):
        t = i / sample_rate
        p = i / total
        freq = 150 * (1.0 - p * 0.8)
        decay = math.exp(-p * 4.0)
        tone = math.sin(2 * math.pi * freq * t)
        val = int(tone * decay * 30000)
        impact_samples.append(max(-32768, min(32767, val)))
    write_wav("transition_impact.wav", impact_samples)


def list_sfx() -> List[Dict[str, Any]]:
    """Returns all available SFX files and their metadata."""
    ensure_sfx_assets()
    items = []
    for f in os.listdir(SFX_DIR):
        if f.endswith(".wav"):
            p = os.path.join(SFX_DIR, f)
            name = f.replace(".wav", "").replace("_", " ").title()
            items.append({
                "id": f,
                "name": name,
                "path": p.replace("\\", "/"),
                "size_bytes": os.path.getsize(p),
            })
    return items


def auto_attach_transition_sfx(
    project_doc: Dict[str, Any],
    sfx_type: str = "whoosh_fast.wav",
    volume: float = 0.7,
) -> int:
    """
    Detects video cut points (where clip A transitions to clip B) and automatically
    inserts transition sound effects synchronized to each cut point.
    """
    ensure_sfx_assets()
    sfx_path = os.path.join(SFX_DIR, sfx_type).replace("\\", "/")
    if not os.path.isfile(sfx_path):
        sfx_path = os.path.join(SFX_DIR, "whoosh_fast.wav").replace("\\", "/")

    clips = project_doc.get("timeline", {}).get("clips", [])
    video_clips = [c for c in clips if c.get("kind") == "Video"]
    if len(video_clips) < 2:
        return 0

    # Sort video clips by timeline start
    video_clips.sort(key=lambda c: float(c.get("start", 0.0)))
    cut_times = []
    for i in range(len(video_clips) - 1):
        c1 = video_clips[i]
        cut_t = float(c1.get("start", 0.0)) + float(c1.get("duration", 0.0))
        cut_times.append(cut_t)

    # Ensure SFX audio track exists
    tracks = project_doc.setdefault("timeline", {}).setdefault("tracks", [])
    sfx_track_id = "track_sfx_effects"
    if not any(t.get("id") == sfx_track_id for t in tracks):
        tracks.append({
            "id": sfx_track_id,
            "kind": "Audio",
            "name": "Sound Effects (SFX)",
        })

    # Add SFX clips centered around each cut (start 0.15s before cut)
    count = 0
    for cut_t in cut_times:
        sfx_start = max(0.0, cut_t - 0.15)
        clips.append({
            "id": f"sfx_{uuid.uuid4().hex[:6]}",
            "track_id": sfx_track_id,
            "start": sfx_start,
            "duration": 0.35,
            "kind": "Audio",
            "media_path": sfx_path,
            "name": f"SFX {sfx_type.split('.')[0]}",
            "volume": volume,
        })
        count += 1

    return count


if __name__ == "__main__":
    ensure_sfx_assets()
    sfx_list = list_sfx()
    print(f"Generated {len(sfx_list)} built-in sound effects in {SFX_DIR}:")
    for s in sfx_list:
        print(f"  - {s['name']} ({s['id']})")
