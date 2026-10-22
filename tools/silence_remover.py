# SPDX-License-Identifier: AGPL-3.0-or-later
"""
Auto Silence / Jump-Cut Removal
Scans audio stream for pauses > 0.5s and computes ripple-cut edits for Concat timeline.
"""

import math
import struct
import wave
from typing import Any, Dict, List, Tuple

class AudioInterval:
    def __init__(self, start: float, end: float, is_speech: bool):
        self.start = float(start)
        self.end = float(end)
        self.is_speech = is_speech

    @property
    def duration(self) -> float:
        return self.end - self.start


def detect_silence_from_wav(
    wav_path: str,
    silence_threshold_db: float = -35.0,
    min_silence_duration: float = 0.5,
    padding: float = 0.08,
) -> Tuple[List[Tuple[float, float]], List[Tuple[float, float]]]:
    """
    Scans a WAV file and returns:
    - speech_intervals: List of (start_time, end_time) to KEEP.
    - silence_intervals: List of (start_time, end_time) that were CUT.
    """
    with wave.open(wav_path, "rb") as wf:
        num_channels = wf.getnchannels()
        sample_width = wf.getsampwidth()
        sample_rate = wf.getframerate()
        num_frames = wf.getnframes()
        raw_data = wf.readframes(num_frames)

    # Convert to 16-bit mono amplitudes
    if sample_width != 2:
        raise ValueError(f"Only 16-bit PCM WAV is supported directly, got {sample_width * 8} bits")

    total_samples = len(raw_data) // (2 * num_channels)
    window_size_ms = 30
    window_samples = int(sample_rate * (window_size_ms / 1000.0))
    window_bytes = window_samples * 2 * num_channels

    # Linear amplitude threshold for dBFS
    # 0 dBFS corresponds to peak amplitude 32768
    amplitude_threshold = 32768.0 * (10.0 ** (silence_threshold_db / 20.0))

    frame_is_speech: List[bool] = []
    num_windows = len(raw_data) // window_bytes

    for i in range(num_windows):
        offset = i * window_bytes
        chunk = raw_data[offset : offset + window_bytes]
        # Unpack samples
        count = len(chunk) // 2
        shorts = struct.unpack(f"<{count}h", chunk)
        # Average power (RMS)
        sum_sq = 0.0
        # If stereo, average channels
        for s in range(0, count, num_channels):
            sample_val = float(shorts[s])
            sum_sq += sample_val * sample_val

        sample_count = count // num_channels
        rms = math.sqrt(sum_sq / max(1, sample_count))
        frame_is_speech.append(rms >= amplitude_threshold)

    # Collapse frames into intervals
    frame_duration = window_size_ms / 1000.0
    intervals: List[AudioInterval] = []
    if not frame_is_speech:
        return [(0.0, float(num_frames) / sample_rate)], []

    cur_state = frame_is_speech[0]
    cur_start = 0.0

    for i, state in enumerate(frame_is_speech):
        t = i * frame_duration
        if state != cur_state:
            intervals.append(AudioInterval(cur_start, t, cur_state))
            cur_state = state
            cur_start = t

    total_duration = float(num_frames) / sample_rate
    intervals.append(AudioInterval(cur_start, total_duration, cur_state))

    # Filter out silence shorter than min_silence_duration (keep as speech)
    merged_speech: List[Tuple[float, float]] = []
    silence_cuts: List[Tuple[float, float]] = []

    for it in intervals:
        if not it.is_speech and it.duration >= min_silence_duration:
            silence_cuts.append((it.start, it.end))
        else:
            # Treat as speech
            if merged_speech and it.start <= merged_speech[-1][1] + padding * 2:
                # Merge adjacent speech segments
                prev_start, prev_end = merged_speech.pop()
                merged_speech.append((prev_start, it.end))
            else:
                merged_speech.append((it.start, it.end))

    # Apply padding to speech intervals
    padded_speech: List[Tuple[float, float]] = []
    for start, end in merged_speech:
        p_start = max(0.0, start - padding)
        p_end = min(total_duration, end + padding)
        if padded_speech and p_start <= padded_speech[-1][1]:
            prev_s, _ = padded_speech.pop()
            padded_speech.append((prev_s, p_end))
        else:
            padded_speech.append((p_start, p_end))

    return padded_speech, silence_cuts


def compute_ripple_cuts(
    original_clip_id: str,
    clip_start: float,
    clip_duration: float,
    speech_intervals: List[Tuple[float, float]],
) -> Dict[str, Any]:
    """
    Calculates Concat timeline edit commands to split a clip and ripple-delete silence.
    Returns:
    - new_clips: List of resulting clips placed back-to-back with zero gaps.
    - time_saved: Seconds of dead air eliminated.
    """
    result_clips = []
    current_timeline_time = clip_start

    for s_in, s_out in speech_intervals:
        seg_duration = s_out - s_in
        if seg_duration <= 0.05:
            continue
        result_clips.append({
            "source_in": s_in,
            "source_out": s_out,
            "duration": seg_duration,
            "timeline_start": current_timeline_time,
        })
        current_timeline_time += seg_duration

    total_speech = current_timeline_time - clip_start
    time_saved = clip_duration - total_speech

    return {
        "original_clip_id": original_clip_id,
        "original_duration": clip_duration,
        "new_duration": total_speech,
        "time_saved": max(0.0, time_saved),
        "percent_shortened": round((time_saved / max(0.001, clip_duration)) * 100, 1),
        "segments": result_clips,
    }


if __name__ == "__main__":
    # Test silence detection logic with mock intervals
    mock_speech = [(0.2, 2.5), (3.8, 6.0), (8.0, 11.2)]
    cuts = compute_ripple_cuts("clip_test_1", 0.0, 12.0, mock_speech)
    print("Ripple cuts calculation test:")
    print(f"Original duration: {cuts['original_duration']}s -> New: {cuts['new_duration']:.2f}s")
    print(f"Saved: {cuts['time_saved']:.2f}s ({cuts['percent_shortened']}%)")
    for seg in cuts["segments"]:
        print(f"  Segment: source {seg['source_in']:.2f}-{seg['source_out']:.2f}s -> timeline at {seg['timeline_start']:.2f}s")
