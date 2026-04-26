from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from client.dashscope_asr import (
    DashScopeFiletransClient,
    DashScopeFiletransConfig,
    DashScopeTranscriptionError,
    extract_transcript_text,
)

from .config import DEFAULT_ASR_MODEL
from .frontmatter import parse_frontmatter, render_frontmatter


AUDIO_NORMALIZATION_VERSION = "mono-opus-16k-v1"


class VideoMaterializationError(RuntimeError):
    """Raised when a video descriptor cannot be converted into parser text."""


@dataclass(frozen=True)
class VideoMaterializationResult:
    text_path: Path
    metadata_path: Path
    raw_asr_path: Path
    transcript_path: Path
    materialization_path: Path
    media_cache_key: str
    asr_model: str


def media_cache_key(*, url: str, parser: str, asr_model: str) -> str:
    digest = hashlib.sha256()
    digest.update(url.encode("utf-8"))
    digest.update(b"\0")
    digest.update(parser.encode("utf-8"))
    digest.update(b"\0")
    digest.update(asr_model.encode("utf-8"))
    digest.update(b"\0")
    digest.update(AUDIO_NORMALIZATION_VERSION.encode("utf-8"))
    return digest.hexdigest()


def materialize_video(
    raw_path: Path,
    frontmatter: dict[str, Any],
    body: str,
    output_dir: Path,
    previous_record: dict[str, Any] | None = None,
    root_dir: Path | None = None,
) -> VideoMaterializationResult:
    url = str(frontmatter.get("url") or "").strip()
    if not url:
        raise VideoMaterializationError("video descriptor is missing url")

    parser = str(frontmatter.get("parser") or "asr").strip()
    if parser != "asr":
        raise VideoMaterializationError(f"unsupported video parser: {parser}")

    asr_model = os.getenv("DASHSCOPE_ASR_MODEL", DEFAULT_ASR_MODEL).strip() or DEFAULT_ASR_MODEL
    cache_key = media_cache_key(url=url, parser=parser, asr_model=asr_model)

    output_dir.mkdir(parents=True, exist_ok=True)
    metadata_path = output_dir / "yt_dlp_metadata.json"
    raw_asr_path = output_dir / "asr_result.json"
    transcript_path = output_dir / "transcript.md"
    materialization_path = output_dir / "materialization.json"
    full_md_path = output_dir / "full.md"

    if not restore_cached_media(
        previous_record=previous_record,
        root_dir=root_dir or Path.cwd(),
        cache_key=cache_key,
        metadata_path=metadata_path,
        raw_asr_path=raw_asr_path,
        transcript_path=transcript_path,
    ):
        run_video_asr(
            url=url,
            raw_path=raw_path,
            metadata_path=metadata_path,
            raw_asr_path=raw_asr_path,
            transcript_path=transcript_path,
            asr_model=asr_model,
        )

    transcript_markdown = transcript_path.read_text(encoding="utf-8", errors="ignore")
    transcript_frontmatter, _ = parse_frontmatter(transcript_markdown)
    transcript_text = transcript_text_from_markdown(transcript_markdown)
    metadata = load_json(metadata_path)
    render_full_markdown(
        full_md_path,
        descriptor=frontmatter,
        body=body,
        metadata=metadata,
        transcript_text=transcript_text,
        asr_model=asr_model,
        transcribed_at=str(transcript_frontmatter.get("transcribed_at") or utc_now()),
    )
    existing_materialization = load_json(materialization_path)
    write_text_if_changed(
        materialization_path,
        json.dumps(
            {
                "source": raw_path.as_posix(),
                "url": url,
                "parser": parser,
                "asr_model": asr_model,
                "media_cache_key": cache_key,
                "audio_normalization_version": AUDIO_NORMALIZATION_VERSION,
                "materialized_at": existing_materialization.get("materialized_at") or utc_now(),
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
    )

    return VideoMaterializationResult(
        text_path=full_md_path,
        metadata_path=metadata_path,
        raw_asr_path=raw_asr_path,
        transcript_path=transcript_path,
        materialization_path=materialization_path,
        media_cache_key=cache_key,
        asr_model=asr_model,
    )


def restore_cached_media(
    *,
    previous_record: dict[str, Any] | None,
    root_dir: Path,
    cache_key: str,
    metadata_path: Path,
    raw_asr_path: Path,
    transcript_path: Path,
) -> bool:
    if not previous_record or previous_record.get("media_cache_key") != cache_key:
        return False

    previous_paths = {
        "metadata_path": metadata_path,
        "raw_asr_path": raw_asr_path,
        "transcript_path": transcript_path,
    }
    for record_key, target in previous_paths.items():
        previous_value = previous_record.get(record_key)
        if not previous_value:
            return False
        previous_path = Path(previous_value)
        if not previous_path.is_absolute():
            previous_path = root_dir / previous_path
        if not previous_path.exists():
            return False
        target.parent.mkdir(parents=True, exist_ok=True)
        if previous_path.resolve() != target.resolve():
            shutil.copy2(previous_path, target)
    return True


def run_video_asr(
    *,
    url: str,
    raw_path: Path,
    metadata_path: Path,
    raw_asr_path: Path,
    transcript_path: Path,
    asr_model: str,
) -> None:
    metadata = fetch_video_metadata(url)
    metadata_path.write_text(json.dumps(metadata, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")

    with tempfile.TemporaryDirectory(prefix="ontic-video-") as temp_dir:
        temp_path = Path(temp_dir)
        audio_dir = temp_path / "audio"
        audio_dir.mkdir(parents=True, exist_ok=True)
        downloaded_audio = download_audio(url, audio_dir)
        probe = probe_media(downloaded_audio)
        if not probe.get("has_audio", True):
            raise VideoMaterializationError(f"downloaded media has no audio track: {raw_path}")

        normalized_audio = temp_path / "filetrans.webm"
        normalize_audio(downloaded_audio, normalized_audio)
        object_key = oss_object_key(raw_path=raw_path, audio_path=normalized_audio)
        audio_uri = upload_to_oss(normalized_audio, object_key)
        file_url = presign_oss_url(object_key)

        config = DashScopeFiletransConfig(
            api_key=os.getenv("DASHSCOPE_API_KEY", "").strip(),
            api_base=os.getenv("DASHSCOPE_API_BASE", "https://dashscope.aliyuncs.com/api/v1").strip(),
            model=asr_model,
            timeout_seconds=int(os.getenv("ASR_TASK_TIMEOUT_MS", "2700000")) // 1000,
            poll_interval_seconds=int(os.getenv("ASR_POLL_INTERVAL_SECONDS", "5")),
        )
        result = DashScopeFiletransClient(config).transcribe(file_url)
        raw_asr_path.write_text(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
        text = extract_transcript_text(result, asr_model)
        if not text:
            raise DashScopeTranscriptionError("DashScope result contained no transcript text")
        transcript_path.write_text(
            render_transcript_markdown(
                url=url,
                title=str(metadata.get("title") or ""),
                asr_model=asr_model,
                duration_seconds=probe.get("duration_seconds"),
                audio_source=audio_uri,
                text=text,
            ),
            encoding="utf-8",
        )


def fetch_video_metadata(url: str) -> dict[str, Any]:
    args = ["yt-dlp", "--dump-json", "--skip-download"]
    cookies = os.getenv("YTDLP_COOKIES_PATH", "").strip()
    if cookies:
        args.extend(["--cookies", cookies])
    args.append(url)
    completed = run_command(args, "yt-dlp metadata fetch")
    try:
        return json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        raise VideoMaterializationError(f"yt-dlp metadata output was not JSON: {completed.stdout[:500]}") from exc


def download_audio(url: str, audio_dir: Path) -> Path:
    args = [
        "yt-dlp",
        "--extract-audio",
        "--audio-format",
        "webm",
        "--audio-quality",
        "0",
        "--output",
        str(audio_dir / "%(id)s.%(ext)s"),
    ]
    cookies = os.getenv("YTDLP_COOKIES_PATH", "").strip()
    if cookies:
        args.extend(["--cookies", cookies])
    args.append(url)
    run_command(args, "yt-dlp audio download")
    candidates = [path for path in audio_dir.iterdir() if path.is_file()]
    if not candidates:
        raise VideoMaterializationError("yt-dlp audio download produced no file")
    return max(candidates, key=lambda path: path.stat().st_mtime)


def probe_media(path: Path) -> dict[str, Any]:
    completed = run_command(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration,size:stream=codec_type",
            "-of",
            "json",
            str(path),
        ],
        "ffprobe media check",
    )
    try:
        payload = json.loads(completed.stdout or "{}")
    except json.JSONDecodeError as exc:
        raise VideoMaterializationError(f"ffprobe output was not JSON: {completed.stdout[:500]}") from exc
    streams = payload.get("streams") if isinstance(payload, dict) else []
    has_audio = any(isinstance(stream, dict) and stream.get("codec_type") == "audio" for stream in streams or [])
    media_format = payload.get("format") if isinstance(payload, dict) else {}
    duration_seconds = None
    if isinstance(media_format, dict) and media_format.get("duration"):
        duration_seconds = float(media_format["duration"])
    return {"has_audio": has_audio, "duration_seconds": duration_seconds}


def normalize_audio(source: Path, target: Path) -> None:
    run_command(
        [
            "ffmpeg",
            "-hide_banner",
            "-loglevel",
            "error",
            "-y",
            "-i",
            str(source),
            "-map",
            "0:a:0",
            "-vn",
            "-ac",
            "1",
            "-ar",
            "16000",
            "-c:a",
            "libopus",
            "-b:a",
            "32k",
            str(target),
        ],
        "ffmpeg audio normalization",
    )


def oss_object_key(*, raw_path: Path, audio_path: Path) -> str:
    prefix = os.getenv("OSS_PREFIX", "ontic-wiki/").strip().strip("/")
    digest = file_sha256(audio_path)[:16]
    safe_name = raw_path.stem.replace("/", "-")
    return f"{prefix}/audio/{safe_name}-{digest}.webm" if prefix else f"audio/{safe_name}-{digest}.webm"


def upload_to_oss(path: Path, object_key: str) -> str:
    bucket = os.getenv("OSS_BUCKET", "context-media").strip()
    if not bucket:
        raise VideoMaterializationError("OSS_BUCKET is required for video transcription")
    uri = f"oss://{bucket}/{object_key}"
    run_command(["ossutil", "cp", str(path), uri], "ossutil upload")
    return uri


def presign_oss_url(object_key: str) -> str:
    bucket = os.getenv("OSS_BUCKET", "context-media").strip()
    expires = os.getenv("OSS_SIGN_EXPIRES", "24h").strip() or "24h"
    completed = run_command(["ossutil", "presign", f"oss://{bucket}/{object_key}", "--expires-duration", expires], "ossutil presign")
    for line in completed.stdout.splitlines():
        stripped = line.strip()
        if stripped.startswith("http"):
            return stripped
    raise VideoMaterializationError("ossutil presign did not return a URL")


def render_transcript_markdown(
    *,
    url: str,
    title: str,
    asr_model: str,
    duration_seconds: float | None,
    audio_source: str,
    text: str,
) -> str:
    frontmatter: dict[str, Any] = {
        "source": url,
        "title": title,
        "asr_model": asr_model,
        "transcript_type": "raw_asr",
        "transcribed_at": utc_now(),
    }
    if duration_seconds is not None:
        frontmatter["duration_seconds"] = round(duration_seconds, 3)
    if audio_source:
        frontmatter["audio_source"] = audio_source
    return render_frontmatter(frontmatter, f"# Transcript\n\n{text.strip()}\n")


def render_full_markdown(
    path: Path,
    *,
    descriptor: dict[str, Any],
    body: str,
    metadata: dict[str, Any],
    transcript_text: str,
    asr_model: str,
    transcribed_at: str,
) -> None:
    merged = dict(descriptor)
    merged["source_type"] = "video"
    merged["parser"] = "asr"
    merged["asr_model"] = asr_model
    merged["transcript_type"] = "raw_asr"
    merged["transcribed_at"] = transcribed_at
    for key in ("title", "duration_seconds"):
        if not merged.get(key) and metadata.get(key):
            merged[key] = metadata[key]

    full_body = "\n".join(
        [
            "# User Notes",
            "",
            body.strip(),
            "",
            "# Transcript",
            "",
            transcript_text.strip(),
            "",
        ]
    )
    write_text_if_changed(path, render_frontmatter(merged, full_body))


def transcript_text_from_markdown(markdown: str) -> str:
    marker = "# Transcript"
    if marker not in markdown:
        return markdown.strip()
    return markdown.split(marker, 1)[1].strip()


def load_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return payload if isinstance(payload, dict) else {}


def write_text_if_changed(path: Path, content: str) -> None:
    try:
        if path.read_text(encoding="utf-8") == content:
            return
    except OSError:
        pass
    path.write_text(content, encoding="utf-8")


def run_command(args: list[str], context: str) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(args, check=True, capture_output=True, text=True)
    except FileNotFoundError as exc:
        raise VideoMaterializationError(f"{context} failed: command not found: {args[0]}") from exc
    except subprocess.CalledProcessError as exc:
        stderr = (exc.stderr or exc.stdout or "").strip()
        raise VideoMaterializationError(f"{context} failed: {stderr[:1000]}") from exc


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
