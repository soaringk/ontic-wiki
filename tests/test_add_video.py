from __future__ import annotations

import json
import io
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from cron import add_video
from wiki_agent.frontmatter import parse_frontmatter


class AddVideoTests(unittest.TestCase):
    def test_descriptor_metadata_maps_yt_dlp_fields(self) -> None:
        metadata = {
            "id": "abc123",
            "title": "A Demo Video",
            "extractor_key": "Youtube",
            "channel": "Demo Channel",
            "channel_url": "https://youtube.example/channel",
            "upload_date": "20260420",
            "duration": 123.8,
            "language": "en",
        }

        descriptor = add_video.descriptor_metadata("https://youtu.be/abc123", metadata)

        self.assertEqual(descriptor["source_type"], "video")
        self.assertEqual(descriptor["parser"], "asr")
        self.assertEqual(descriptor["platform"], "youtube")
        self.assertEqual(descriptor["video_id"], "abc123")
        self.assertEqual(descriptor["published"], "2026-04-20")
        self.assertEqual(descriptor["duration_seconds"], 123)

    def test_fetch_metadata_raises_without_writing_on_failure(self) -> None:
        with patch("cron.add_video.subprocess.run", side_effect=FileNotFoundError):
            with self.assertRaises(add_video.VideoAddError):
                add_video.fetch_metadata("https://example.invalid/video")

    def test_main_uses_configured_cookies_path_for_metadata_fetch(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            raw = Path(temp_dir) / "raw"
            metadata = {
                "id": "abc123",
                "title": "A Demo Video",
                "extractor_key": "Youtube",
            }
            completed = Mock(stdout=json.dumps(metadata), stderr="")

            with patch.object(add_video, "RAW_DIR", raw), patch(
                "cron.add_video.subprocess.run",
                return_value=completed,
            ) as run, patch.object(sys, "argv", ["add_video.py", "https://youtu.be/abc123"]), patch(
                "sys.stdout",
                new_callable=io.StringIO,
            ), patch.dict(
                "os.environ",
                {"YTDLP_COOKIES_PATH": "/tmp/ytdlp-cookies.txt"},
            ):
                self.assertEqual(add_video.main(), 0)

            run.assert_called_once()
            self.assertEqual(
                run.call_args.args[0],
                [
                    "yt-dlp",
                    "--dump-json",
                    "--skip-download",
                    "--cookies",
                    "/tmp/ytdlp-cookies.txt",
                    "https://youtu.be/abc123",
                ],
            )

    def test_main_writes_descriptor_and_detects_duplicate(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            raw = root / "raw"
            metadata = {
                "id": "abc123",
                "title": "A Demo Video",
                "extractor_key": "Bilibili",
                "uploader": "Demo Creator",
                "upload_date": "20260420",
                "duration": 90,
            }
            completed = Mock(stdout=json.dumps(metadata), stderr="")

            with patch.object(add_video, "RAW_DIR", raw), patch(
                "cron.add_video.subprocess.run",
                return_value=completed,
            ), patch.object(sys, "argv", ["add_video.py", "https://bilibili.example/video", "--note", "important note"]), patch(
                "sys.stdout",
                new_callable=io.StringIO,
            ):
                self.assertEqual(add_video.main(), 0)

            descriptors = list((raw / "videos").glob("*.video.md"))
            self.assertEqual(len(descriptors), 1)
            frontmatter, body = parse_frontmatter(descriptors[0].read_text(encoding="utf-8"))
            self.assertEqual(frontmatter["source_type"], "video")
            self.assertEqual(frontmatter["parser"], "asr")
            self.assertEqual(frontmatter["platform"], "bilibili")
            self.assertIn("important note", body)

            with patch.object(add_video, "RAW_DIR", raw), patch(
                "cron.add_video.subprocess.run",
                return_value=completed,
            ), patch.object(sys, "argv", ["add_video.py", "https://bilibili.example/video"]), patch(
                "sys.stdout",
                new_callable=io.StringIO,
            ):
                self.assertEqual(add_video.main(), 0)

            self.assertEqual(len(list((raw / "videos").glob("*.video.md"))), 1)


if __name__ == "__main__":
    unittest.main()
