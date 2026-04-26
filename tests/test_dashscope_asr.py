from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from client.dashscope_asr import build_filetrans_payload, extract_transcript_text, transcription_url_from_task


class DashScopeAsrTests(unittest.TestCase):
    def test_builds_fun_asr_payload_with_file_urls_and_diarization(self) -> None:
        payload = build_filetrans_payload(model="fun-asr", file_url="https://oss.example/audio.webm")

        self.assertEqual(payload["model"], "fun-asr")
        self.assertEqual(payload["input"], {"file_urls": ["https://oss.example/audio.webm"]})
        self.assertEqual(payload["parameters"]["channel_id"], [0])
        self.assertTrue(payload["parameters"]["diarization_enabled"])

    def test_builds_qwen_payload_with_single_file_url(self) -> None:
        payload = build_filetrans_payload(model="qwen3-asr-flash-filetrans", file_url="https://oss.example/audio.webm")

        self.assertEqual(payload["input"], {"file_url": "https://oss.example/audio.webm"})
        self.assertEqual(payload["parameters"]["channel_id"], [0])
        self.assertFalse(payload["parameters"]["enable_itn"])
        self.assertFalse(payload["parameters"]["enable_words"])

    def test_extracts_fun_asr_speakers_in_chronological_order(self) -> None:
        text = extract_transcript_text(
            {
                "transcripts": [
                    {
                        "sentences": [
                            {"text": "second", "begin_time": 5000, "speaker_id": 1},
                            {"text": "first", "begin_time": 0, "speaker_id": 0},
                        ]
                    }
                ]
            },
            "fun-asr",
        )

        self.assertEqual(text, "[00:00] Speaker 1: first\n\n[00:05] Speaker 2: second")

    def test_extracts_fallback_transcript_text(self) -> None:
        text = extract_transcript_text({"transcripts": [{"text": "whole transcript"}]}, "fun-asr")

        self.assertEqual(text, "whole transcript")

    def test_fun_asr_transcription_url_uses_results_array(self) -> None:
        url = transcription_url_from_task(
            {"output": {"results": [{"transcription_url": "https://result.example/asr.json"}]}},
            "fun-asr",
        )

        self.assertEqual(url, "https://result.example/asr.json")


if __name__ == "__main__":
    unittest.main()

