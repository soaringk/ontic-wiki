from __future__ import annotations

import json
import sys
import tempfile
import unittest
from contextlib import ExitStack
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from wiki_agent import repository


def patch_repository_paths(root: Path, stack: ExitStack) -> Path:
    raw = root / "raw"
    wiki = root / "wiki"
    state = root / "state"
    for path in (
        raw,
        state / "extracted",
        state / "reports",
        wiki / "sources",
        wiki / "topics",
        wiki / "concepts",
        wiki / "debates",
        wiki / "synthesis",
    ):
        path.mkdir(parents=True, exist_ok=True)
    manifest_path = state / "manifest.json"
    manifest_path.write_text(json.dumps({"version": 1, "sources": {}}), encoding="utf-8")
    patches = {
        "ROOT_DIR": root,
        "RAW_DIR": raw,
        "WIKI_DIR": wiki,
        "SOURCES_DIR": wiki / "sources",
        "TOPICS_DIR": wiki / "topics",
        "CONCEPTS_DIR": wiki / "concepts",
        "DEBATES_DIR": wiki / "debates",
        "SYNTHESIS_DIR": wiki / "synthesis",
        "STATE_DIR": state,
        "EXTRACTED_DIR": state / "extracted",
        "REPORTS_DIR": state / "reports",
        "MANIFEST_PATH": manifest_path,
        "INDEX_PATH": wiki / "index.md",
        "LOG_PATH": wiki / "log.md",
    }
    for name, value in patches.items():
        stack.enter_context(patch.object(repository, name, value))
    stack.enter_context(patch.object(repository, "source_roots", return_value=[raw]))
    return raw


class RepositoryScanTests(unittest.TestCase):
    def test_markdown_source_becomes_pending_without_sidecar(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            raw = root / "raw"
            raw.mkdir()
            (root / "state" / "extracted").mkdir(parents=True)
            (root / "state" / "reports").mkdir(parents=True)
            (root / "wiki" / "sources").mkdir(parents=True)
            (root / "wiki" / "topics").mkdir(parents=True)
            (root / "wiki" / "concepts").mkdir(parents=True)
            (root / "wiki" / "debates").mkdir(parents=True)
            (root / "wiki" / "synthesis").mkdir(parents=True)
            source = raw / "cuda_intro.md"
            source.write_text("# CUDA Intro\n\nThreads and blocks.\n", encoding="utf-8")

            manifest_path = root / "state" / "manifest.json"
            manifest_path.write_text(json.dumps({"version": 1, "sources": {}}), encoding="utf-8")

            with patch.object(repository, "ROOT_DIR", root), \
                patch.object(repository, "RAW_DIR", raw), \
                patch.object(repository, "WIKI_DIR", root / "wiki"), \
                patch.object(repository, "SOURCES_DIR", root / "wiki" / "sources"), \
                patch.object(repository, "TOPICS_DIR", root / "wiki" / "topics"), \
                patch.object(repository, "CONCEPTS_DIR", root / "wiki" / "concepts"), \
                patch.object(repository, "DEBATES_DIR", root / "wiki" / "debates"), \
                patch.object(repository, "SYNTHESIS_DIR", root / "wiki" / "synthesis"), \
                patch.object(repository, "STATE_DIR", root / "state"), \
                patch.object(repository, "EXTRACTED_DIR", root / "state" / "extracted"), \
                patch.object(repository, "REPORTS_DIR", root / "state" / "reports"), \
                patch.object(repository, "MANIFEST_PATH", manifest_path), \
                patch.object(repository, "INDEX_PATH", root / "wiki" / "index.md"), \
                patch.object(repository, "LOG_PATH", root / "wiki" / "log.md"), \
                patch.object(repository, "source_roots", return_value=[raw]):
                summary = repository.scan_sources()
                manifest = repository.load_manifest()

            self.assertEqual(summary.pending_paths, ["raw/cuda_intro.md"])
            record = manifest["sources"]["raw/cuda_intro.md"]
            self.assertEqual(record["source_type"], "markdown")
            self.assertEqual(record["text_status"], "ready")
            self.assertIsNone(record["text_path"])
            self.assertEqual(list((root / "state" / "extracted").glob("*")), [])

    def test_pdf_source_uses_cached_markdown_sidecar(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            raw = root / "raw"
            raw.mkdir()
            (root / "state" / "extracted").mkdir(parents=True)
            (root / "state" / "reports").mkdir(parents=True)
            (root / "wiki" / "sources").mkdir(parents=True)
            (root / "wiki" / "topics").mkdir(parents=True)
            (root / "wiki" / "concepts").mkdir(parents=True)
            (root / "wiki" / "debates").mkdir(parents=True)
            (root / "wiki" / "synthesis").mkdir(parents=True)
            source = raw / "paper.pdf"
            source.write_bytes(b"%PDF-1.4 fake pdf content")

            manifest_path = root / "state" / "manifest.json"
            manifest_path.write_text(json.dumps({"version": 1, "sources": {}}), encoding="utf-8")

            with patch.object(repository, "ROOT_DIR", root), \
                patch.object(repository, "RAW_DIR", raw), \
                patch.object(repository, "WIKI_DIR", root / "wiki"), \
                patch.object(repository, "SOURCES_DIR", root / "wiki" / "sources"), \
                patch.object(repository, "TOPICS_DIR", root / "wiki" / "topics"), \
                patch.object(repository, "CONCEPTS_DIR", root / "wiki" / "concepts"), \
                patch.object(repository, "DEBATES_DIR", root / "wiki" / "debates"), \
                patch.object(repository, "SYNTHESIS_DIR", root / "wiki" / "synthesis"), \
                patch.object(repository, "STATE_DIR", root / "state"), \
                patch.object(repository, "EXTRACTED_DIR", root / "state" / "extracted"), \
                patch.object(repository, "REPORTS_DIR", root / "state" / "reports"), \
                patch.object(repository, "MANIFEST_PATH", manifest_path), \
                patch.object(repository, "INDEX_PATH", root / "wiki" / "index.md"), \
                patch.object(repository, "LOG_PATH", root / "wiki" / "log.md"), \
                patch.object(repository, "source_roots", return_value=[raw]), \
                patch.object(repository, "MineruPrecisionClient") as mineru_client_cls:
                def parse_pdf_to_dir(_path, *, data_id, output_dir):
                    full_md_path = Path(output_dir) / "full.md"
                    full_md_path.parent.mkdir(parents=True, exist_ok=True)
                    full_md_path.write_text("# Parsed\n\n![](images/figure.jpg)", encoding="utf-8")
                    image_path = full_md_path.parent / "images" / "figure.jpg"
                    image_path.parent.mkdir(parents=True, exist_ok=True)
                    image_path.write_bytes(b"jpg-bytes")
                    return full_md_path

                mineru_client_cls.return_value.parse_pdf_to_dir.side_effect = parse_pdf_to_dir
                summary = repository.scan_sources()
                manifest = repository.load_manifest()

            self.assertEqual(summary.pending_paths, ["raw/paper.pdf"])
            record = manifest["sources"]["raw/paper.pdf"]
            self.assertEqual(record["source_type"], "pdf")
            self.assertEqual(record["text_status"], "ready")
            self.assertTrue(record["text_path"].endswith("/full.md"))
            self.assertTrue((root / record["text_path"]).exists())
            self.assertTrue((root / record["text_path"]).parent.joinpath("images", "figure.jpg").exists())
            mineru_client_cls.return_value.parse_pdf_to_dir.assert_called_once()

    def test_unsupported_file_is_recorded(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            raw = root / "raw"
            raw.mkdir()
            (root / "state" / "extracted").mkdir(parents=True)
            (root / "state" / "reports").mkdir(parents=True)
            manifest_path = root / "state" / "manifest.json"
            manifest_path.write_text(json.dumps({"version": 1, "sources": {}}), encoding="utf-8")
            (raw / "figure.png").write_bytes(b"fake")

            with patch.object(repository, "ROOT_DIR", root), \
                patch.object(repository, "RAW_DIR", raw), \
                patch.object(repository, "WIKI_DIR", root / "wiki"), \
                patch.object(repository, "SOURCES_DIR", root / "wiki" / "sources"), \
                patch.object(repository, "TOPICS_DIR", root / "wiki" / "topics"), \
                patch.object(repository, "CONCEPTS_DIR", root / "wiki" / "concepts"), \
                patch.object(repository, "DEBATES_DIR", root / "wiki" / "debates"), \
                patch.object(repository, "SYNTHESIS_DIR", root / "wiki" / "synthesis"), \
                patch.object(repository, "STATE_DIR", root / "state"), \
                patch.object(repository, "EXTRACTED_DIR", root / "state" / "extracted"), \
                patch.object(repository, "REPORTS_DIR", root / "state" / "reports"), \
                patch.object(repository, "MANIFEST_PATH", manifest_path), \
                patch.object(repository, "INDEX_PATH", root / "wiki" / "index.md"), \
                patch.object(repository, "LOG_PATH", root / "wiki" / "log.md"), \
                patch.object(repository, "source_roots", return_value=[raw]):
                summary = repository.scan_sources()
                manifest = repository.load_manifest()

            self.assertEqual(summary.unsupported_paths, ["raw/figure.png"])
            record = manifest["sources"]["raw/figure.png"]
            self.assertEqual(record["source_type"], "unsupported")
            self.assertIn("unsupported extension", record["unsupported_reason"])

    def test_video_source_frontmatter_materializes_text_path(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir, ExitStack() as stack:
            root = Path(temp_dir)
            raw = patch_repository_paths(root, stack)
            video = raw / "videos" / "demo.video.md"
            video.parent.mkdir(parents=True, exist_ok=True)
            video.write_text(
                "---\n"
                "source_type: video\n"
                "parser: asr\n"
                "url: \"https://example.test/video\"\n"
                "title: \"Demo Video\"\n"
                "---\n\n"
                "# Notes\n\nImportant user note.\n",
                encoding="utf-8",
            )

            def fake_materialize(_path, _frontmatter, _body, output_dir, _record, *, root_dir):
                output_dir.mkdir(parents=True, exist_ok=True)
                paths = {
                    "text_path": output_dir / "full.md",
                    "metadata_path": output_dir / "yt_dlp_metadata.json",
                    "raw_asr_path": output_dir / "asr_result.json",
                    "transcript_path": output_dir / "transcript.md",
                    "materialization_path": output_dir / "materialization.json",
                }
                for path in paths.values():
                    path.write_text("ok\n", encoding="utf-8")
                return SimpleNamespace(**paths, media_cache_key="media-key", asr_model="fun-asr")

            stack.enter_context(patch.object(repository, "materialize_video", side_effect=fake_materialize))

            summary = repository.scan_sources()
            manifest = repository.load_manifest()

        self.assertEqual(summary.pending_paths, ["raw/videos/demo.video.md"])
        record = manifest["sources"]["raw/videos/demo.video.md"]
        self.assertEqual(record["source_type"], "video")
        self.assertEqual(record["parser"], "asr")
        self.assertEqual(record["asr_model"], "fun-asr")
        self.assertEqual(record["media_cache_key"], "media-key")
        self.assertTrue(record["text_path"].endswith("/full.md"))

    def test_video_source_blocks_unknown_parser(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir, ExitStack() as stack:
            root = Path(temp_dir)
            raw = patch_repository_paths(root, stack)
            video = raw / "videos" / "demo.video.md"
            video.parent.mkdir(parents=True, exist_ok=True)
            video.write_text(
                "---\n"
                "source_type: video\n"
                "parser: multimodal\n"
                "url: \"https://example.test/video\"\n"
                "---\n",
                encoding="utf-8",
            )
            materialize_mock = stack.enter_context(patch.object(repository, "materialize_video"))

            summary = repository.scan_sources()
            manifest = repository.load_manifest()

        materialize_mock.assert_not_called()
        self.assertEqual(summary.blocked_paths, ["raw/videos/demo.video.md"])
        record = manifest["sources"]["raw/videos/demo.video.md"]
        self.assertEqual(record["source_type"], "video")
        self.assertEqual(record["text_status"], "blocked")
        self.assertIn("unsupported video parser", record["text_error"])

    def test_mark_paths_ingested_records_video_media_cache_key(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir, ExitStack() as stack:
            root = Path(temp_dir)
            _raw = patch_repository_paths(root, stack)
            manifest = {
                "version": 1,
                "sources": {
                    "raw/videos/demo.video.md": {
                        "current_hash": "hash",
                        "media_cache_key": "media-key",
                    }
                },
            }
            repository.save_manifest(manifest)

            repository.mark_paths_ingested(["raw/videos/demo.video.md"], "2026-04-26T00:00:00Z")
            updated = repository.load_manifest()["sources"]["raw/videos/demo.video.md"]

        self.assertEqual(updated["last_ingested_hash"], "hash")
        self.assertEqual(updated["last_ingested_media_cache_key"], "media-key")

    def test_lint_report_counts_debate_pages(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            wiki = root / "wiki"
            sources = wiki / "sources"
            topics = wiki / "topics"
            concepts = wiki / "concepts"
            debates = wiki / "debates"
            synthesis = wiki / "synthesis"
            reports = root / "state" / "reports"
            for path in (sources, topics, concepts, debates, synthesis, reports):
                path.mkdir(parents=True)
            (debates / "claim.md").write_text("# Debate\n", encoding="utf-8")
            (synthesis / "answer.md").write_text("# Synthesis\n", encoding="utf-8")

            with patch.object(repository, "ROOT_DIR", root), \
                patch.object(repository, "RAW_DIR", root / "raw"), \
                patch.object(repository, "WIKI_DIR", wiki), \
                patch.object(repository, "SOURCES_DIR", sources), \
                patch.object(repository, "TOPICS_DIR", topics), \
                patch.object(repository, "CONCEPTS_DIR", concepts), \
                patch.object(repository, "DEBATES_DIR", debates), \
                patch.object(repository, "SYNTHESIS_DIR", synthesis), \
                patch.object(repository, "STATE_DIR", root / "state"), \
                patch.object(repository, "EXTRACTED_DIR", root / "state" / "extracted"), \
                patch.object(repository, "REPORTS_DIR", reports), \
                patch.object(repository, "MANIFEST_PATH", root / "state" / "manifest.json"), \
                patch.object(repository, "INDEX_PATH", wiki / "index.md"), \
                patch.object(repository, "LOG_PATH", wiki / "log.md"):
                report_path = repository.write_lint_report("2026-04-20T00:00:00Z")

            report = report_path.read_text(encoding="utf-8")
            self.assertIn("- debate_pages: `1`", report)
            self.assertIn("- synthesis_pages: `1`", report)
            self.assertIn("- `wiki/debates/claim.md`", report)


if __name__ == "__main__":
    unittest.main()
