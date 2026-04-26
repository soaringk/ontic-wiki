# Ontic Wiki

Autonomous study wiki for papers, notes, articles, and textbooks.

## How it works

1. Drop study materials into [`raw/`](./raw/).
2. A nightly cron job scans the repo, extracts text, and triggers an agentic reindex pass.
3. The agent updates [`wiki/`](./wiki/) directly.
4. You query the knowledge base through the agent, not through a separate UI.

## Setup

```bash
cp .env.example .env
uv sync
```

Then review `.env` and add the cron jobs from [`docs/workflow/crontab.md`](./docs/workflow/crontab.md). If your OpenCode server does not require auth, `OPENCODE_PASSWORD` may stay empty.
If you want PDF parsing, set `MINERU_API_TOKEN` as well. The default `MINERU_OCR_ENABLE=auto` policy will choose OCR for scanned PDFs and keep it off for normal digital PDFs.

## Daily use

- Put `.md`, `.txt`, or `.pdf` files into [`raw/`](./raw/).
- Add videos with `uv run python src/cron/add_video.py "<video-url>" --note "optional notes"`.
- Wait for the nightly reindex run.
- Ask the agent questions against the wiki.
- If an answer is worth keeping, ask the agent to save it into [`wiki/synthesis/`](./wiki/synthesis/).

## Video sources

Video URLs are stored as Markdown descriptors under `raw/videos/` with `source_type: video` and `parser: asr`.
The scanner downloads audio, transcribes it with DashScope Filetrans, and caches the generated transcript under `state/extracted/`.
The default ASR model is `fun-asr` so speaker diarization is available for conversations and interviews.

Video ingest requires `yt-dlp`, `ffmpeg`, `ffprobe`, `ossutil`, `DASHSCOPE_API_KEY`, and OSS settings in `.env`.
