from __future__ import annotations

import os
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[2]
ENV_PATH = ROOT_DIR / ".env"


def load_env_file(path: Path = ENV_PATH) -> None:
    if not path.exists():
        return

    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip())


load_env_file()

RAW_DIR = ROOT_DIR / "raw"
RAW_VIDEOS_DIR = RAW_DIR / "videos"
WIKI_DIR = ROOT_DIR / "wiki"
SOURCES_DIR = WIKI_DIR / "sources"
TOPICS_DIR = WIKI_DIR / "topics"
CONCEPTS_DIR = WIKI_DIR / "concepts"
DEBATES_DIR = WIKI_DIR / "debates"
SYNTHESIS_DIR = WIKI_DIR / "synthesis"
STATE_DIR = ROOT_DIR / "state"
EXTRACTED_DIR = STATE_DIR / "extracted"
REPORTS_DIR = STATE_DIR / "reports"
MANIFEST_PATH = STATE_DIR / "manifest.json"
INDEX_PATH = WIKI_DIR / "index.md"
LOG_PATH = WIKI_DIR / "log.md"
WORKFLOW_PATH = ROOT_DIR / "docs" / "workflow" / "study_wiki.md"
AGENTS_PATH = ROOT_DIR / "AGENTS.md"

DEFAULT_REINDEX_MODEL = os.getenv("WIKI_AGENT_MODEL", "openai/gpt-5.5")
DEFAULT_LINT_MODEL = os.getenv("WIKI_LINT_MODEL", DEFAULT_REINDEX_MODEL)

SUPPORTED_EXTENSIONS = {
    ".md": "markdown",
    ".txt": "text",
    ".pdf": "pdf",
}
SUPPORTED_VIDEO_PARSERS = {"asr"}
DEFAULT_VIDEO_PARSER = "asr"
DEFAULT_ASR_MODEL = os.getenv("DASHSCOPE_ASR_MODEL", "fun-asr")


def source_roots() -> list[Path]:
    return [RAW_DIR]
