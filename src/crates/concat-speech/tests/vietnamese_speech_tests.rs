// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2026 Jareer and Concat contributors

//! Tests for Vietnamese speech & transcription integration.

use concat_speech::transcribe::TranscribeRequest;
use concat_speech::tts::{DEFAULT_VITS_VOICE, Family, VITS_VOICES, family_of, voice_family};

#[test]
fn test_vits_vietnamese_model_family_classification() {
    let model_id = "vits-piper-vi_VN-vivos-x_low";
    assert_eq!(family_of(model_id), Family::Vits);
}

#[test]
fn test_vits_vietnamese_voice_mappings() {
    assert_eq!(DEFAULT_VITS_VOICE, 3000);
    assert_eq!(voice_family(3000), Some(Family::Vits));
    assert_eq!(voice_family(3001), Some(Family::Vits));

    // Ensure Vietnamese voice IDs are unique and defined
    let mut ids = std::collections::HashSet::new();
    for (id, name) in VITS_VOICES {
        assert!(ids.insert(*id), "duplicate voice ID found: {id}");
        assert_eq!(voice_family(*id), Some(Family::Vits));
        assert!(name.starts_with("vf_") || name.starts_with("vm_"));
    }
}

#[test]
fn test_transcribe_request_vietnamese_language_support() {
    let json_with_vi = r#"{
        "path": "/footage/interview_vi.mp4",
        "audioStream": 0,
        "sourceStart": 5.0,
        "window": 25.0,
        "modelId": "base",
        "language": "vi"
    }"#;

    let req: TranscribeRequest =
        serde_json::from_str(json_with_vi).expect("deserialization with vietnamese language");
    assert_eq!(req.path, "/footage/interview_vi.mp4");
    assert_eq!(req.audio_stream, Some(0));
    assert_eq!(req.source_start, 5.0);
    assert_eq!(req.window, 25.0);
    assert_eq!(req.model_id, "base");
    assert_eq!(req.language.as_deref(), Some("vi"));

    // Verify backward compatibility when language is omitted
    let json_legacy = r#"{
        "path": "/footage/interview_vi.mp4",
        "sourceStart": 0.0,
        "window": 10.0,
        "modelId": "small"
    }"#;

    let req_legacy: TranscribeRequest =
        serde_json::from_str(json_legacy).expect("legacy deserialization without language");
    assert_eq!(req_legacy.language, None);
}
