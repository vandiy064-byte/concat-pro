# SPDX-License-Identifier: AGPL-3.0-or-later
"""
Concat Studio Pro Master Controller
Command Line & Interactive Interface for all Advanced Pro Video Editing Capabilities.
"""

import argparse
import os
import sys

from karaoke_subtitles import WordTiming, group_words_into_phrases, render_ass_karaoke, generate_word_clips_for_timeline, export_timeline_to_srt
from silence_remover import detect_silence_from_wav, compute_ripple_cuts
from script_to_video import assemble_script_to_timeline, save_concat_project_file
from smart_reframe import apply_smart_reframe_to_project, generate_smooth_pan_keyframes
from capcut_bridge import convert_concat_to_capcut_draft, find_capcut_draft_directory
from vocal_separator import VocalSeparator
from sfx_library import list_sfx, auto_attach_transition_sfx
from text_animator import PRESET_NAMES, generate_text_animation_keyframes, apply_animation_preset_to_clip
from beauty_filter import BeautyFilterSpec, apply_beauty_filter_to_timeline_clip
from typography_presets import list_typography_presets, batch_apply_typography_to_project
from concat_client import ConcatClient

def run_menu():
    print("=" * 66)
    print("     CONCAT PRO STUDIO v2.0.9 - TRỌN BỘ CÔNG CỤ CHUẨN CAPCUT")
    print("=" * 66)
    print(" 1. [Karaoke Subtitles]    Tạo phụ đề nhảy chữ từng từ kiểu TikTok/Hormozi")
    print(" 2. [Auto Silence Cut]     Quét & Cắt bỏ khoảng lặng (Jump-cut) tự động")
    print(" 3. [Script to Video]      Tự động dựng video hoàn chỉnh từ kịch bản")
    print(" 4. [Smart Reframe]        Chuyển video ngang 16:9 sang dọc 9:16 giữ chủ thể")
    print(" 5. [CapCut Bridge]        Xuất dự án Concat sang CapCut PC (draft_content.json)")
    print(" 6. [Vocal Isolation]      Tách lời bài hát, tách beat karaoke, khử ồn âm thanh")
    print(" 7. [Sound Effects (SFX)]  Kho âm thanh chuyển cảnh (Whoosh, Ding, Pop, Glitch)")
    print(" 8. [Text Animations]      8 mẫu hoạt ảnh chữ chuyển động (Typewriter, Bounce...)")
    print(" 9. [AI Face Beauty]       Bộ lọc làm mịn màng da mặt & sáng da tự nhiên")
    print("10. [Typography Styles]    5 phong cách kiểu chữ phụ đề tiếng Việt bắt mắt")
    print("11. [Concat Live Status]   Kiểm tra kết nối ứng dụng Concat đang chạy")
    print(" 0. Thoát")
    print("=" * 66)

    choice = input("Nhập lựa chọn của bạn (0-11): ").strip()

    if choice == "1":
        print("\n--- 1. TẠO PHỤ ĐỀ NHẢY CHỮ KARAOKE ---")
        text = input("Nhập câu mẫu hoặc nhấn Enter để dùng câu mặc định: ").strip()
        if not text:
            text = "Chào mừng bạn đến với kênh Concat AI tạo video tự động"
        words = text.split()
        t = 0.0
        word_timings = []
        for w in words:
            dur = 0.35
            word_timings.append(WordTiming(w, t, t + dur))
            t += dur + 0.05
        phrases = group_words_into_phrases(word_timings, max_words_per_line=4)
        ass_out = render_ass_karaoke(phrases)
        out_file = os.path.join(os.getcwd(), "karaoke_output.ass")
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(ass_out)
        print(f"[OK] Đã xuất file phụ đề nhảy chữ ASS: {out_file}")

        # Tự động xuất thêm file SRT chuẩn
        word_clips = generate_word_clips_for_timeline(phrases)
        srt_file = os.path.join(os.getcwd(), "karaoke_output.srt")
        export_timeline_to_srt(word_clips, output_path=srt_file)
        print(f"[OK] Đã xuất file phụ đề chuẩn SRT:     {srt_file}")

    elif choice == "2":
        print("\n--- 2. QUÉT & CẮT BỎ KHOẢNG LẶNG (JUMP-CUT) ---")
        wav_file = input("Nhập đường dẫn file audio WAV (hoặc Enter để chạy mô phỏng): ").strip()
        if wav_file and os.path.isfile(wav_file):
            speech, cuts = detect_silence_from_wav(wav_file)
            print(f"[OK] Phát hiện {len(speech)} đoạn tiếng nói, đã cắt bỏ {len(cuts)} khoảng lặng.")
        else:
            mock_speech = [(0.2, 3.1), (4.5, 7.8), (9.0, 12.5)]
            res = compute_ripple_cuts("clip_demo", 0.0, 14.0, mock_speech)
            print(f"[OK] Mô phỏng thành công: Tiết kiệm {res['time_saved']:.2f}s ({res['percent_shortened']}%) thời lượng chết!")

    elif choice == "3":
        print("\n--- 3. TẠO VIDEO TỰ ĐỘNG TỪ KỊCH BẢN ---")
        script = input("Nhập nội dung kịch bản ngắn (hoặc Enter để dùng kịch bản mẫu): ").strip()
        if not script:
            script = "Xin chào các bạn. Hôm nay chúng ta sẽ tìm hiểu về trí tuệ nhân tạo. AI giúp bạn dựng video cực nhanh và hoàn toàn tự động!"
        proj = assemble_script_to_timeline(script, "Auto_Script_Project")
        out_path = os.path.join(os.getcwd(), "projects", "Auto_Script_Project.json")
        save_concat_project_file(proj, out_path)
        print(f"[OK] Đã tạo dự án Concat hoàn chỉnh tại: {out_path}")

    elif choice == "4":
        print("\n--- 4. SMART REFRAME (16:9 SANG 9:16) ---")
        sample_proj = {
            "name": "Reframe_Demo",
            "video": {"width": 1920, "height": 1080},
            "timeline": {
                "clips": [{"kind": "Video", "duration": 8.0, "media_path": "demo.mp4"}]
            }
        }
        res = apply_smart_reframe_to_project(sample_proj, focus_mode="center")
        print(f"[OK] Đã reframe canvas sang {res['video']['width']}x{res['video']['height']} (9:16 dọc) với scale {res['timeline']['clips'][0]['transform']['scale']}x")

    elif choice == "5":
        print("\n--- 5. XUẤT SANG CAPCUT PC ---")
        sample_proj = {
            "name": "Concat_To_CapCut_Project",
            "video": {"width": 1080, "height": 1920, "frame_rate": 30.0},
            "timeline": {
                "duration": 5.0,
                "clips": [
                    {"kind": "video", "start": 0.0, "duration": 5.0, "media_path": "E:/sample.mp4"},
                    {"kind": "text", "start": 0.2, "duration": 4.5, "text": {"content": "Phụ đề Concat trên CapCut"}},
                ]
            }
        }
        draft_dir = convert_concat_to_capcut_draft(sample_proj)
        print(f"[OK] Đã tạo thư mục dự án CapCut PC tại: {draft_dir}")
        print("Bây giờ bạn chỉ cần mở ứng dụng CapCut trên máy, dự án sẽ hiển thị sẵn sàng!")

    elif choice == "6":
        print("\n--- 6. TÁCH LỜI / TÁCH BEAT / KHỬ ỒN ---")
        print("Chế độ: 1. Tách lời (Vocal) | 2. Tách beat karaoke (Instrumental) | 3. Khử ồn (Denoise)")
        mode_idx = input("Chọn chế độ (1-3, mặc định 1): ").strip()
        modes = {"1": "vocal", "2": "instrumental", "3": "denoise"}
        chosen_mode = modes.get(mode_idx, "vocal")
        print(f"[OK] Đã chọn chế độ: {chosen_mode}. Thuật toán sẵn sàng xử lý file âm thanh của bạn.")

    elif choice == "7":
        print("\n--- 7. KHO ÂM THANH HIỆU ỨNG (SFX LIBRARY) ---")
        sfx_items = list_sfx()
        print(f"[OK] Có {len(sfx_items)} âm thanh hiệu ứng sẵn sàng:")
        for s in sfx_items:
            print(f"  * {s['name']}: {s['path']}")

    elif choice == "8":
        print("\n--- 8. HOẠT ẢNH CHỮ CHUYỂN ĐỘNG (TEXT ANIMATION) ---")
        print("Các mẫu hoạt ảnh CapCut có sẵn:")
        for i, name in enumerate(PRESET_NAMES, 1):
            print(f"  {i}. {name}")
        p_idx = input("Chọn mẫu hoạt ảnh (1-8, mặc định 1): ").strip()
        preset = PRESET_NAMES[int(p_idx) - 1] if p_idx.isdigit() and 1 <= int(p_idx) <= len(PRESET_NAMES) else "ZoomBounce"
        kfs = generate_text_animation_keyframes(preset, 3.0)
        print(f"[OK] Đã sinh {sum(len(v) for v in kfs.values())} điểm keyframe cho hiệu ứng: {preset}")

    elif choice == "9":
        print("\n--- 9. LÀM ĐẸP MỊN DA (AI FACE BEAUTY) ---")
        spec = BeautyFilterSpec(smoothness=70.0, brighten=15.0)
        print(f"[OK] Cấu hình Beauty Filter: Độ mịn da={spec.smoothness}%, Sáng da={spec.brighten}%")
        print(f"Tham số shader: {spec.to_effect_dict()['params']}")

    elif choice == "10":
        print("\n--- 10. BỘ TẠO KIỂU CHỮ TYPOGRAPHY TIẾNG VIỆT ---")
        typo_list = list_typography_presets()
        for t in typo_list:
            print(f"  * [{t['id']}] {t['name']} - Font: {t['font_family']}, Màu: {t['color']}")

    elif choice == "11":
        print("\n--- 11. KIỂM TRA KẾT NỐI ỨNG DỤNG CONCAT ---")
        client = ConcatClient()
        try:
            v = client.call("concat_version")
            print("[OK] Đã kết nối thành công với Concat đang chạy trên máy!")
            print(f"Địa chỉ: {client.address}, Phiên bản: {v.get('version', '0.2.8')}")
        except Exception as e:
            print("[INFO] Concat chưa bật cổng Automation hoặc chưa mở. Chi tiết:", e)

    print("\nHoàn thành tác vụ.")

if __name__ == "__main__":
    run_menu()
