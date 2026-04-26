#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SRC_ROOT = Path(__file__).resolve().parents[1]
if str(SRC_ROOT) not in sys.path:
    sys.path.append(str(SRC_ROOT))

from wiki_agent.config import RAW_DIR
from wiki_agent.frontmatter import parse_frontmatter, render_frontmatter


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a raw video descriptor for Ontic Wiki ingest.")
    parser.add_argument("url", help="YouTube, Bilibili, or other yt-dlp supported video URL")
    parser.add_argument("--note", default="", help="Optional note to place in the descriptor body")
    parser.add_argument("--note-file", help="Path to a Markdown file whose contents become the descriptor body")
    parser.add_argument("--cookies", help="Cookies file passed to yt-dlp for metadata fetch")
    args = parser.parse_args()

    note = args.note
    if args.note_file:
        note = Path(args.note_file).read_text(encoding="utf-8")

    try:
        metadata = fetch_metadata(args.url, cookies=configured_cookies_path(args.cookies))
    except VideoAddError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    raw_videos_dir = RAW_DIR / "videos"
    raw_videos_dir.mkdir(parents=True, exist_ok=True)
    descriptor = descriptor_metadata(args.url, metadata)
    existing = find_existing_descriptor(raw_videos_dir, descriptor)
    if existing is not None:
        print(existing.relative_to(Path.cwd()).as_posix() if existing.is_relative_to(Path.cwd()) else existing.as_posix())
        return 0

    target = raw_videos_dir / descriptor_filename(descriptor)
    body = note.strip()
    if body:
        body = f"# Notes\n\n{body}\n"
    else:
        body = "# Notes\n"
    target.write_text(render_frontmatter(descriptor, body), encoding="utf-8")
    print(target.relative_to(Path.cwd()).as_posix() if target.is_relative_to(Path.cwd()) else target.as_posix())
    return 0


class VideoAddError(RuntimeError):
    pass


def configured_cookies_path(explicit_cookies: str | None = None) -> str | None:
    cookies = explicit_cookies or os.getenv("YTDLP_COOKIES_PATH", "").strip()
    return cookies or None


def fetch_metadata(url: str, *, cookies: str | None = None) -> dict[str, Any]:
    args = ["yt-dlp", "--dump-json", "--skip-download"]
    if cookies:
        args.extend(["--cookies", cookies])
    args.append(url)
    try:
        completed = subprocess.run(args, check=True, capture_output=True, text=True)
    except FileNotFoundError as exc:
        raise VideoAddError("yt-dlp is required to add video sources") from exc
    except subprocess.CalledProcessError as exc:
        stderr = (exc.stderr or exc.stdout or "").strip()
        raise VideoAddError(f"yt-dlp metadata fetch failed: {stderr[:1000]}") from exc

    try:
        payload = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        raise VideoAddError(f"yt-dlp returned non-JSON metadata: {completed.stdout[:500]}") from exc
    if not isinstance(payload, dict):
        raise VideoAddError("yt-dlp returned invalid metadata")
    return payload


def descriptor_metadata(url: str, metadata: dict[str, Any]) -> dict[str, Any]:
    return {
        "source_type": "video",
        "parser": "asr",
        "url": url,
        "platform": platform_from_metadata(metadata),
        "video_id": str(metadata.get("id") or ""),
        "title": str(metadata.get("title") or ""),
        "channel": str(metadata.get("channel") or metadata.get("uploader") or ""),
        "channel_url": str(metadata.get("channel_url") or metadata.get("uploader_url") or ""),
        "published": published_date(metadata),
        "duration_seconds": duration_seconds(metadata),
        "language": str(metadata.get("language") or ""),
        "metadata_fetched_at": utc_now(),
    }


def platform_from_metadata(metadata: dict[str, Any]) -> str:
    extractor = str(metadata.get("extractor_key") or metadata.get("extractor") or "").lower()
    webpage_url = str(metadata.get("webpage_url") or "").lower()
    if "bilibili" in extractor or "bilibili" in webpage_url:
        return "bilibili"
    if "youtube" in extractor or "youtube" in webpage_url or "youtu.be" in webpage_url:
        return "youtube"
    return extractor.replace(":", "-") or "video"


def published_date(metadata: dict[str, Any]) -> str:
    value = metadata.get("release_date") or metadata.get("upload_date")
    if not value:
        return ""
    text = str(value)
    if re.fullmatch(r"\d{8}", text):
        return f"{text[0:4]}-{text[4:6]}-{text[6:8]}"
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", text):
        return text
    return ""


def duration_seconds(metadata: dict[str, Any]) -> int | str:
    duration = metadata.get("duration")
    if duration is None or duration == "":
        return ""
    try:
        return int(float(duration))
    except (TypeError, ValueError):
        return ""


def descriptor_filename(metadata: dict[str, Any]) -> str:
    date = datetime.now(timezone.utc).strftime("%Y%m%d")
    platform = slugify(str(metadata.get("platform") or "video"))
    video_id = slugify(str(metadata.get("video_id") or "unknown"))
    title = slugify(str(metadata.get("title") or "video"))[:60]
    return f"{date}_{platform}_{video_id}_{title}.video.md"


def find_existing_descriptor(raw_videos_dir: Path, descriptor: dict[str, Any]) -> Path | None:
    platform = descriptor.get("platform")
    video_id = descriptor.get("video_id")
    url = descriptor.get("url")
    for path in sorted(raw_videos_dir.glob("*.md")):
        frontmatter, _ = parse_frontmatter(path.read_text(encoding="utf-8", errors="ignore"))
        if frontmatter.get("source_type") != "video":
            continue
        if platform and video_id and frontmatter.get("platform") == platform and frontmatter.get("video_id") == video_id:
            return path
        if url and frontmatter.get("url") == url:
            return path
    return None


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value).strip("-").lower()
    return slug or "video"


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


if __name__ == "__main__":
    raise SystemExit(main())
