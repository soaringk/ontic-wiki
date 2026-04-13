from __future__ import annotations

import hashlib
import json
import re
import shutil
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

import requests

from client.mineru import MineruParseError, MineruPrecisionClient

from .config import (
    CONCEPTS_DIR,
    EXTRACTED_DIR,
    INDEX_PATH,
    LOG_PATH,
    MANIFEST_PATH,
    RAW_DIR,
    REPORTS_DIR,
    ROOT_DIR,
    SOURCES_DIR,
    STATE_DIR,
    SUPPORTED_EXTENSIONS,
    SYNTHESIS_DIR,
    TOPICS_DIR,
    WIKI_DIR,
    source_roots,
)


ISO_FORMAT = "%Y-%m-%dT%H:%M:%SZ"


@dataclass
class ScanSummary:
    pending_paths: list[str]
    blocked_paths: list[str]
    unsupported_paths: list[str]
    report_path: Path
    scan_time: str


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime(ISO_FORMAT)


def ensure_layout() -> None:
    for path in (RAW_DIR, WIKI_DIR, SOURCES_DIR, TOPICS_DIR, CONCEPTS_DIR, SYNTHESIS_DIR, STATE_DIR, EXTRACTED_DIR, REPORTS_DIR):
        path.mkdir(parents=True, exist_ok=True)

    if not MANIFEST_PATH.exists():
        save_manifest({"version": 1, "sources": {}})
    if not INDEX_PATH.exists():
        INDEX_PATH.write_text("# Wiki Index\n", encoding="utf-8")
    if not LOG_PATH.exists():
        LOG_PATH.write_text("# Wiki Log\n", encoding="utf-8")


def load_manifest() -> dict:
    if not MANIFEST_PATH.exists():
        return {"version": 1, "sources": {}}
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def save_manifest(manifest: dict) -> None:
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value).strip("-").lower()
    return slug or "source"


def guess_title(path: Path, source_type: str) -> str:
    if source_type in {"markdown", "text"}:
        try:
            for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
                stripped = line.strip()
                if stripped.startswith("#"):
                    return stripped.lstrip("#").strip()
                if stripped:
                    return stripped[:120]
        except OSError:
            pass
    return path.stem.replace("_", " ").replace("-", " ").strip() or path.name


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def relative_to_root(path: Path) -> str:
    return path.relative_to(ROOT_DIR).as_posix()


def extracted_bundle_dirname(relative_path: str, sha256: str) -> str:
    stem = slugify(relative_path.replace("/", "-"))
    return f"{stem}-{sha256[:12]}"


def extract_pdf(path: Path, output_dir: Path) -> tuple[Path | None, str | None]:
    output_dir = Path(output_dir)

    try:
        data_id = slugify(path.name.rsplit(".", 1)[0])[:80]
        full_md_path = MineruPrecisionClient().parse_pdf_to_dir(path, data_id=data_id, output_dir=output_dir)
    except MineruParseError as exc:
        return None, str(exc)
    except requests.RequestException as exc:  # pragma: no cover - network dependent
        return None, f"MinerU request failed: {exc}"

    markdown = full_md_path.read_text(encoding="utf-8", errors="ignore")
    if not markdown.strip():
        return None, "MinerU returned empty markdown"
    return full_md_path, None


def iter_source_files() -> list[Path]:
    paths: list[Path] = []
    for root in source_roots():
        if not root.exists():
            continue
        for path in sorted(root.rglob("*")):
            if path.is_file():
                paths.append(path)
    return paths


def cached_text_path(record: dict, current_hash: str) -> Path | None:
    text_path = record.get("text_path")
    if record.get("current_hash") != current_hash or not text_path:
        return None
    candidate = ROOT_DIR / text_path
    if not candidate.exists():
        return None
    return candidate


def cleanup_extracted_files(manifest: dict) -> None:
    referenced_paths: set[Path] = set()
    for record in manifest.get("sources", {}).values():
        if record.get("removed") or not record.get("text_path"):
            continue
        text_path = ROOT_DIR / record["text_path"]
        try:
            relative_text_path = text_path.relative_to(EXTRACTED_DIR)
        except ValueError:
            referenced_paths.add(text_path)
            continue
        if relative_text_path.parts:
            referenced_paths.add(EXTRACTED_DIR / relative_text_path.parts[0])

    for extracted_path in EXTRACTED_DIR.glob("*"):
        if extracted_path in referenced_paths:
            continue
        if extracted_path.is_dir():
            shutil.rmtree(extracted_path)
        else:
            extracted_path.unlink()


def scan_sources() -> ScanSummary:
    ensure_layout()
    manifest = load_manifest()
    manifest_sources = manifest.setdefault("sources", {})
    seen_paths: set[str] = set()

    pending_paths: list[str] = []
    blocked_paths: list[str] = []
    unsupported_paths: list[str] = []
    scan_time = utc_now()

    for path in iter_source_files():
        relative_path = relative_to_root(path)
        seen_paths.add(relative_path)
        suffix = path.suffix.lower()
        source_type = SUPPORTED_EXTENSIONS.get(suffix)
        record = manifest_sources.get(relative_path, {})

        entry = {
            "current_hash": file_sha256(path),
            "current_mtime": path.stat().st_mtime,
            "current_size": path.stat().st_size,
            "last_seen_at": scan_time,
            "raw_path": relative_path,
            "removed": False,
            "source_type": source_type or "unsupported",
            "text_error": None,
            "text_path": None,
            "text_status": None,
            "title": guess_title(path, source_type or "unsupported"),
            "unsupported_reason": None,
        }

        if source_type is None:
            entry["unsupported_reason"] = f"unsupported extension: {suffix or '<none>'}"
            unsupported_paths.append(relative_path)
            manifest_sources[relative_path] = {**record, **entry}
            continue

        if source_type in {"markdown", "text"}:
            entry["text_status"] = "ready"
        else:
            cached_path = cached_text_path(record, entry["current_hash"])
            if cached_path is not None:
                entry["text_path"] = relative_to_root(cached_path)
                entry["text_status"] = "ready"
            else:
                extracted_name = extracted_bundle_dirname(relative_path, entry["current_hash"])
                extracted_dir = EXTRACTED_DIR / extracted_name
                extracted_path, text_error = extract_pdf(path, extracted_dir)
                if text_error:
                    entry["text_error"] = text_error
                    entry["text_status"] = "blocked"
                    blocked_paths.append(relative_path)
                else:
                    entry["text_error"] = None
                    entry["text_path"] = relative_to_root(extracted_path)
                    entry["text_status"] = "ready"

        entry["source_id"] = slugify(relative_path.rsplit(".", 1)[0])
        if entry["text_status"] == "ready" and record.get("last_ingested_hash") != entry["current_hash"]:
            pending_paths.append(relative_path)

        manifest_sources[relative_path] = {**record, **entry}

    removed_paths = sorted(set(manifest_sources) - seen_paths)
    for relative_path in removed_paths:
        manifest_sources[relative_path]["removed"] = True
        manifest_sources[relative_path]["last_seen_at"] = scan_time

    cleanup_extracted_files(manifest)
    save_manifest(manifest)
    report_path = write_ingest_report(manifest, pending_paths, blocked_paths, unsupported_paths, scan_time)
    return ScanSummary(
        pending_paths=pending_paths,
        blocked_paths=blocked_paths,
        unsupported_paths=unsupported_paths,
        report_path=report_path,
        scan_time=scan_time,
    )


def write_ingest_report(
    manifest: dict,
    pending_paths: list[str],
    blocked_paths: list[str],
    unsupported_paths: list[str],
    scan_time: str,
) -> Path:
    report_path = REPORTS_DIR / "latest_reindex_report.md"
    sources = manifest["sources"]

    def lines_for(paths: list[str]) -> list[str]:
        lines: list[str] = []
        for relative_path in paths:
            record = sources[relative_path]
            lines.extend(
                [
                    f"### {record['title']}",
                    f"- raw_path: `{relative_path}`",
                    f"- source_id: `{record.get('source_id', '')}`",
                    f"- source_type: `{record['source_type']}`",
                    f"- current_hash: `{record['current_hash']}`",
                ]
            )
            if record.get("text_path"):
                lines.append(f"- text_path: `{record['text_path']}`")
            if record.get("text_error"):
                lines.append(f"- error: `{record['text_error']}`")
            lines.append("")
        return lines

    content = "\n".join(
        [
            "# Latest Reindex Report",
            "",
            f"- scan_time: `{scan_time}`",
            f"- source_roots: `{', '.join(relative_to_root(path) for path in source_roots())}`",
            f"- pending_supported: `{len(pending_paths)}`",
            f"- blocked_supported: `{len(blocked_paths)}`",
            f"- unsupported: `{len(unsupported_paths)}`",
            "",
            "## Pending Sources",
            "",
            *(lines_for(pending_paths) or ["None", ""]),
            "## Blocked Sources",
            "",
            *(lines_for(blocked_paths) or ["None", ""]),
            "## Unsupported Sources",
            "",
            *(lines_for(unsupported_paths) or ["None", ""]),
        ]
    ).rstrip() + "\n"
    report_path.write_text(content, encoding="utf-8")
    return report_path


def mark_paths_ingested(paths: list[str], ingested_at: str) -> None:
    manifest = load_manifest()
    for relative_path in paths:
        record = manifest["sources"].get(relative_path)
        if not record:
            continue
        record["last_ingested_at"] = ingested_at
        record["last_ingested_hash"] = record.get("current_hash")
    save_manifest(manifest)


def write_lint_report(scan_time: str) -> Path:
    ensure_layout()
    report_path = REPORTS_DIR / "latest_lint_report.md"
    source_pages = sorted(relative_to_root(path) for path in SOURCES_DIR.glob("*.md"))
    topic_pages = sorted(relative_to_root(path) for path in TOPICS_DIR.glob("*.md"))
    concept_pages = sorted(relative_to_root(path) for path in CONCEPTS_DIR.glob("*.md"))
    synthesis_pages = sorted(relative_to_root(path) for path in SYNTHESIS_DIR.glob("*.md"))
    page_lines = [f"- `{path}`" for path in (source_pages + topic_pages + concept_pages + synthesis_pages)]

    content = "\n".join(
        [
            "# Latest Lint Report",
            "",
            f"- scan_time: `{scan_time}`",
            f"- source_pages: `{len(source_pages)}`",
            f"- topic_pages: `{len(topic_pages)}`",
            f"- concept_pages: `{len(concept_pages)}`",
            f"- synthesis_pages: `{len(synthesis_pages)}`",
            "",
            "## Existing Pages",
            "",
            *(page_lines or ["- none"]),
        ]
    ).rstrip() + "\n"
    report_path.write_text(content, encoding="utf-8")
    return report_path
