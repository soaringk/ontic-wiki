from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from wiki_agent.video_materializer import materialize_video, media_cache_key


class VideoMaterializerTests(unittest.TestCase):
    def test_materialize_video_reuses_cached_transcript_for_note_changes(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            old_dir = root / "state" / "extracted" / "old"
            new_dir = root / "state" / "extracted" / "new"
            old_dir.mkdir(parents=True)
            (old_dir / "yt_dlp_metadata.json").write_text(json.dumps({"title": "Cached title"}), encoding="utf-8")
            (old_dir / "asr_result.json").write_text(json.dumps({"transcripts": [{"text": "cached transcript"}]}), encoding="utf-8")
            (old_dir / "transcript.md").write_text(
                "---\nsource: \"https://example/video\"\n---\n\n# Transcript\n\ncached transcript\n",
                encoding="utf-8",
            )

            frontmatter = {
                "source_type": "video",
                "parser": "asr",
                "url": "https://example/video",
                "title": "Descriptor title",
            }
            cache_key = media_cache_key(url="https://example/video", parser="asr", asr_model="fun-asr")
            previous_record = {
                "media_cache_key": cache_key,
                "metadata_path": "state/extracted/old/yt_dlp_metadata.json",
                "raw_asr_path": "state/extracted/old/asr_result.json",
                "transcript_path": "state/extracted/old/transcript.md",
            }

            with patch.dict(os.environ, {"DASHSCOPE_ASR_MODEL": "fun-asr"}, clear=False), patch(
                "wiki_agent.video_materializer.run_video_asr",
            ) as run_video_asr:
                result = materialize_video(
                    root / "raw" / "videos" / "demo.video.md",
                    frontmatter,
                    "# Notes\n\nnew user note\n",
                    new_dir,
                    previous_record,
                    root_dir=root,
                )

            run_video_asr.assert_not_called()
            self.assertEqual(result.media_cache_key, cache_key)
            self.assertTrue((new_dir / "yt_dlp_metadata.json").exists())
            self.assertTrue((new_dir / "asr_result.json").exists())
            self.assertTrue((new_dir / "transcript.md").exists())
            self.assertFalse((new_dir / "chunks").exists())
            full = (new_dir / "full.md").read_text(encoding="utf-8")
            self.assertIn("# User Notes\n\n# Notes\n\nnew user note", full)
            self.assertIn("# Transcript\n\ncached transcript", full)
            self.assertLess(full.index("# User Notes"), full.index("# Transcript"))


if __name__ == "__main__":
    unittest.main()

