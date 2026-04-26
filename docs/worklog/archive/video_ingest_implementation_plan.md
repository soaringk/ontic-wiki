# Video Ingest Implementation Plan

## Goal

Extend Ontic Wiki so a YouTube or Bilibili video can be added as study material by providing a video URL plus optional body notes. The system should fetch video metadata, transcribe the full spoken content through ASR, cache machine-generated artifacts under `state/`, and feed the resulting text into the existing wiki reindex workflow.

This plan is implementation guidance only. It does not change the current runtime behavior until the listed code changes are made.

## Product Contract

The user-facing workflow should be:

```bash
uv run python src/cron/add_video.py "https://www.youtube.com/watch?v=..." --note "Optional personal note."
```

The script creates a raw descriptor under `raw/videos/`. The user may later edit the Markdown body of that descriptor to add more notes, insights, questions, or emphasis.

The raw descriptor is the user-provided source. Downloaded audio, ASR JSON, transcripts, and merged parser output are machine state and must live under `state/`, not under `raw/`.

## Source Descriptor Format

Use Markdown with frontmatter. The important fields are `source_type: video` and `parser: asr`.

Example:

```markdown
---
source_type: video
parser: asr
url: "https://www.bilibili.com/video/BV..."
platform: bilibili
video_id: "BV..."
title: "Video title from yt-dlp"
channel: "Creator or uploader name"
channel_url: "https://..."
published: "2026-04-20"
duration_seconds: 1234
language: ""
metadata_fetched_at: "2026-04-25T12:00:00Z"
---

# Notes

User-provided observations go here. These notes are part of the raw source and must be included by the downstream wiki ingest.
```

Rules:

- `source_type` must be `video`.
- `parser` must initially be `asr`.
- `parser` is required so future `multimodal` support can be added without changing the descriptor contract.
- Do not add a `must_include` field. User-provided notes live in the Markdown body.
- `published` must come from actual video metadata when `yt-dlp` provides it. If no reliable publication date is available, leave it blank or omit it. Do not substitute local ingest time.
- Body notes must be copied into the generated `full.md` parser output before the transcript so the agent sees user context and the complete transcript together.

## add_video.py

Add `src/cron/add_video.py`.

Responsibilities:

1. Accept a URL and optional note input.
2. Run `yt-dlp --dump-json --skip-download <url>` to fetch metadata.
3. Normalize metadata into descriptor frontmatter.
4. Write a Markdown descriptor into `raw/videos/`.
5. Print the created path.

Suggested CLI:

```bash
uv run python src/cron/add_video.py URL
uv run python src/cron/add_video.py URL --note "..."
uv run python src/cron/add_video.py URL --note-file notes.md
uv run python src/cron/add_video.py URL --cookies /path/to/cookies.txt
```

Naming:

```text
raw/videos/YYYYMMDD_<platform>_<video_id>_<slug>.video.md
```

Metadata mapping:

- `url`: original URL passed by the user.
- `platform`: infer from yt-dlp extractor key or webpage URL.
- `video_id`: yt-dlp `id`.
- `title`: yt-dlp `title`.
- `channel`: prefer `channel`, then `uploader`.
- `channel_url`: prefer `channel_url`, then `uploader_url`.
- `published`: prefer `release_date`, then `upload_date`; format as `YYYY-MM-DD` when possible.
- `duration_seconds`: yt-dlp `duration`.
- `language`: yt-dlp language if present, otherwise empty.
- `metadata_fetched_at`: local UTC timestamp.

Failure behavior:

- If metadata fetch fails, the script should fail without writing a descriptor by default. This avoids creating misleading source pages with poor metadata.
- A later `--allow-partial-metadata` option can create a minimal descriptor with `url`, `source_type`, and `parser`, but that should not be the default.
- If a descriptor with the same platform and video ID already exists, print the existing path and do not create a duplicate unless an explicit overwrite or append option is added later.

## Scanner Changes

Update `src/wiki_agent/repository.py` so source type detection is not based only on file suffix.

Required behavior:

- Markdown files with frontmatter `source_type: video` are treated as `video`, even though their suffix is `.md`.
- `.video.md` descriptors should also be treated as video descriptors, but frontmatter is the authoritative signal.
- Existing `.md`, `.txt`, and `.pdf` behavior must remain backward compatible.
- Unsupported `parser` values should block the source with a clear `text_error`.

Update `src/wiki_agent/config.py`:

```python
SUPPORTED_EXTENSIONS = {
    ".md": "markdown",
    ".txt": "text",
    ".pdf": "pdf",
}

SUPPORTED_VIDEO_PARSERS = {"asr"}
DEFAULT_VIDEO_PARSER = "asr"
DEFAULT_ASR_MODEL = os.getenv("DASHSCOPE_ASR_MODEL", "fun-asr")
```

The scanner should report video records with:

- `source_type: video`
- `parser: asr`
- `text_status`
- `text_path`
- `metadata_path`
- `raw_asr_path`
- `transcript_path`
- `asr_model`

## Video Materialization

Add a small video materializer, for example `src/wiki_agent/video_materializer.py`.

Inputs:

- raw descriptor path
- parsed descriptor frontmatter
- descriptor body notes
- output bundle directory under `state/extracted/`

Outputs:

```text
state/extracted/<source-id>-<hash>/
  yt_dlp_metadata.json
  asr_result.json
  transcript.md
  full.md
  materialization.json
```

`full.md` should contain:

```markdown
---
source_type: video
parser: asr
url: ...
title: ...
platform: ...
video_id: ...
channel: ...
published: ...
duration_seconds: ...
asr_model: fun-asr
transcript_type: raw_asr
transcribed_at: ...
---

# User Notes

<descriptor body>

# Transcript

<complete ASR transcript>
```

Important caching rule:

- User notes and video transcription have different cache boundaries.
- Changing only the descriptor body should regenerate `full.md` and mark the source pending for wiki ingest, but it should not force audio download and ASR again.
- Re-run audio download and ASR only when the media cache key changes.

Suggested media cache key:

```text
sha256(url + parser + asr_model + audio_normalization_version)
```

The raw descriptor file hash should still control whether the source is pending for wiki ingest.

## ASR Implementation

Default ASR model:

```text
fun-asr
```

Reason:

- `fun-asr` supports speaker diarization and is better for interviews, conversations, panels, and podcast-like videos.
- The local `trade-bot` implementation already tests the important payload and extraction differences for `fun-asr`.

Environment variables:

```dotenv
DASHSCOPE_API_KEY=
DASHSCOPE_API_BASE=https://dashscope.aliyuncs.com/api/v1
DASHSCOPE_ASR_MODEL=fun-asr
OSS_BUCKET=context-media
OSS_PREFIX=ontic-wiki/
OSS_SIGN_EXPIRES=24h
ASR_TASK_TIMEOUT_MS=2700000
YTDLP_COOKIES_PATH=
```

Payload behavior:

- For `fun-asr`, DashScope Filetrans uses `input.file_urls`, not `input.file_url`.
- Enable diarization by default.
- Normalize audio to mono and use `channel_id: [0]`.

Expected `fun-asr` payload:

```json
{
  "model": "fun-asr",
  "input": {
    "file_urls": ["https://signed-oss-url"]
  },
  "parameters": {
    "channel_id": [0],
    "diarization_enabled": true
  }
}
```

Transcript extraction:

- Prefer sentence-level transcript data.
- Preserve speaker labels when `speaker_id` is present.
- Preserve timestamps when `begin_time` is present.
- Sort sentence records chronologically when speaker diarization causes grouped or out-of-order output.
- Fall back to whole-transcript text only when sentence arrays are missing.

Example transcript formatting:

```text
[00:00] Speaker 1: Welcome to the show.

[00:05] Speaker 2: Thanks for having me.
```

Do not actively chunk transcripts in the parser. Reading a large transcript in segments is the downstream ingest agent's responsibility.

## Download And Audio Flow

Use `yt-dlp` and `ffmpeg`.

Flow:

1. Fetch metadata through `yt-dlp --dump-json --skip-download`.
2. Download audio through `yt-dlp --extract-audio`.
3. Verify duration and file size with `ffprobe`.
4. Normalize audio:

```bash
ffmpeg -hide_banner -loglevel error -y \
  -i "<source>" \
  -map 0:a:0 -vn -ac 1 -ar 16000 \
  -c:a libopus -b:a 32k \
  "<normalized>.webm"
```

5. Upload normalized audio to OSS.
6. Generate a presigned URL.
7. Submit DashScope Filetrans.
8. Poll task status until success or timeout.
9. Download raw ASR JSON.
10. Extract transcript text.
11. Write `transcript.md` and `full.md`.

Temporary audio files may live under `tmp/` during materialization. Long-term artifacts should be the ASR JSON, transcript, and materialization metadata. The normalized audio may be deleted locally after upload unless explicit debug retention is enabled.

## Reindex Prompt Changes

Update `src/cron/reindex.py` prompt so the agent understands video sources.

Add requirements:

- For video sources, read the generated `text_path`, not only the raw descriptor.
- Treat the raw descriptor body as user-provided notes. Incorporate these notes into the source page and any affected topic or concept pages when relevant.
- Treat the ASR transcript as raw spoken content. It may contain recognition errors and colloquial phrasing.
- Use actual `published` metadata from the descriptor when present.
- Do not invent a publication date when video metadata is missing.
- Do not require parser-time transcript chunking.

The source page frontmatter should propagate:

```yaml
source_type: video
parser: asr
published: ...
raw_path: ...
```

## Manifest And Report Changes

The manifest should keep source-level and parser-level state separate enough to avoid unnecessary ASR reruns.

Suggested record fields:

```json
{
  "raw_path": "raw/videos/...",
  "source_type": "video",
  "parser": "asr",
  "current_hash": "...",
  "last_ingested_hash": "...",
  "media_cache_key": "...",
  "last_materialized_media_cache_key": "...",
  "text_status": "ready",
  "text_path": "state/extracted/.../full.md",
  "metadata_path": "state/extracted/.../yt_dlp_metadata.json",
  "raw_asr_path": "state/extracted/.../asr_result.json",
  "transcript_path": "state/extracted/.../transcript.md",
  "asr_model": "fun-asr",
  "text_error": null
}
```

The latest reindex report should include:

- `source_type`
- `parser`
- `asr_model`
- `text_path`
- `transcript_path`
- `raw_asr_path`
- `text_error` when blocked

## Tests

Add focused tests before relying on cron.

Repository tests:

- Detect `source_type: video` frontmatter in a `.video.md` file.
- Detect `source_type: video` frontmatter in a normal `.md` file.
- Block unknown video parser values.
- Reuse cached transcript when only body notes change.
- Mark the source pending when descriptor body changes.
- Preserve existing Markdown, text, and PDF behavior.

add_video tests:

- Mock `yt-dlp --dump-json` and verify descriptor frontmatter.
- Verify `upload_date` or `release_date` becomes `YYYY-MM-DD`.
- Verify duplicate video ID does not create a second descriptor.
- Verify metadata failure does not write a descriptor by default.

ASR tests:

- Build `fun-asr` Filetrans payload with `file_urls` and diarization enabled.
- Extract speaker-labeled timestamped transcript.
- Sort diarized sentence records chronologically.
- Fall back to `transcripts[].text` when sentence arrays are absent.

Materializer tests:

- Mock `yt-dlp`, `ffprobe`, `ffmpeg`, OSS upload, presign, DashScope submit, poll, and download.
- Verify `asr_result.json`, `transcript.md`, `full.md`, and `materialization.json` are written.
- Verify `full.md` contains user notes before transcript.
- Verify no parser-time transcript chunks are created.

CLI smoke test:

```bash
uv run python src/cron/add_video.py "https://example.invalid/watch?v=test" --note "demo"
uv run python src/cron/reindex.py --scan-only
```

Use mocks or a small local fixture for automated tests. Do not require network access in unit tests.

## Documentation Updates

Update:

- `README.md`: add video URL workflow.
- `.env.example`: add DashScope, OSS, and yt-dlp cookie variables.
- `docs/workflow/study_wiki.md`: add `video` to supported source types and document parser sidecars.
- `docs/workflow/crontab.md`: mention `yt-dlp`, `ffmpeg`, `ffprobe`, `ossutil`, and DashScope credentials as runtime prerequisites for video ingest.

## Acceptance Criteria

The implementation is complete when:

1. A user can add a video URL through `src/cron/add_video.py`.
2. The created raw descriptor uses `source_type: video` and `parser: asr`.
3. The descriptor frontmatter is populated from `yt-dlp` metadata.
4. Video materialization uses `fun-asr` by default.
5. The ASR transcript is complete and stored under `state/extracted/`.
6. User body notes are included in `full.md`.
7. No active parser-time chunking is introduced.
8. Existing Markdown, text, and PDF ingest behavior remains compatible.
9. Reindex reports include enough paths and errors to debug blocked video sources.
10. Unit tests cover metadata extraction, source detection, ASR payload/extraction, caching, and materializer output.

