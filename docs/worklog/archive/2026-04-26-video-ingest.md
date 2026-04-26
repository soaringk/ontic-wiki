# Video Ingest Worklog

## Task

Implement video URL ingest for Ontic Wiki based on `docs/workflow/video_ingest_implementation_plan.md`.

## Assumptions

- Existing raw/wiki/state boundaries remain authoritative.
- Video raw inputs are Markdown descriptors with `source_type: video` and `parser: asr`.
- `fun-asr` is the default ASR model.
- Parser-time transcript chunking is intentionally out of scope.

## Discoveries

- `scan_sources()` is the right integration point for video materialization because PDFs already use the same pre-agent `text_path` sidecar pattern.
- Video note edits and media ASR cache need separate keys: the raw descriptor hash controls wiki reingest, while `media_cache_key` controls whether audio download and ASR can be reused.
- `fun-asr` uses DashScope `input.file_urls` and `output.results[].transcription_url`, unlike qwen ASR models.

## Validation

- `UV_CACHE_DIR=/tmp/uv-cache uv run python -m unittest discover tests`
- Result: 30 tests passed.

## Promotion Candidates

- Already promoted into `docs/workflow/study_wiki.md` as the durable video parsing workflow. No additional durable doc needed.
