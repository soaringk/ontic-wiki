# Study Wiki Workflow

## Goal

Turn raw learning materials into a maintained, queryable wiki with minimal user effort.

The user workflow is intentionally small:

1. put source files into `raw/`
2. let nightly automation process them
3. query the wiki through the agent

## Layers

### Raw sources

- Path: `raw/`
- Immutable inputs
- Supported in v1: `.md`, `.txt`, `.pdf`, and video descriptors with `source_type: video`

### Machine state

- Path: `state/`
- `manifest.json` tracks file hashes and ingest state
- `extracted/` stores cached parser bundles, including PDF `full.md` files and video ASR transcripts
- `reports/` stores the latest ingest and lint reports

### Wiki

- Path: `wiki/`
- Agent-maintained Markdown pages
- Main page types:
  - `source`
  - `topic`
  - `concept`
  - `debate`
  - `synthesis`

## Source page shape

Every source page should include concise frontmatter:

```yaml
kind: source
title: ...
slug: ...
source_ids:
  - ...
status: active
raw_path: ...
source_type: markdown|text|pdf|video
parser: ...
published: ...
created: ...
updated: ...
```

- `published` should come from the source's actual raw metadata when available.
- `created` and `updated` are local wiki maintenance timestamps and must not be used as substitutes for publication time.
- If the raw `published` field is blank, missing, or ambiguous, leave it unknown rather than inferring it from ingest time.

Recommended sections:

1. Summary
2. Key Claims
3. Why It Matters
4. Connections
5. Open Questions

## Topic and concept pages

- Prefer one durable page per real concept or study area
- Merge overlapping ideas into existing pages instead of cloning them
- Add links back to relevant source pages
- Keep pages compact and cumulative

## Debate pages

- Path: `wiki/debates/`
- Debate pages are curated argument-validation records for contested interpretation across sources.
- They are a workbench for claims, objections, axioms, hypotheses, and agent recommendations; they are not source pages and should not become parallel topic or synthesis pages.
- Use debate pages when multiple sources appear to conflict, when a synthesis rests on contested interpretation, or when a topic/concept update needs adversarial validation.
- Debate pages should cite local source pages, identify competing interpretations, classify claims as facts, axioms, hypotheses, interpretations, or recommendations, and end with agent recommendations plus a user decision area.
- In the current workflow, only the user adjudicates contested debates. Agents may recommend promotion, but must not mark debates decided or promote conclusions unless the user explicitly accepts the outcome.
- User-accepted conclusions should be distilled into `wiki/synthesis/`; topic pages should link to debates only as live or recently user-adjudicated tensions.
- Follow [`debate_protocol.md`](./debate_protocol.md) for multi-agent debate roles, rounds, evidence rules, and promotion criteria.

## Ingest workflow

The nightly reindex job does this:

1. scan `raw/`
2. detect new or changed supported files
3. refresh cached PDF Markdown bundles under `state/extracted/` only for PDFs
4. write a machine-readable and human-readable report under `state/reports/`
5. trigger an agentic ingest pass
6. update source/topic/concept pages
7. open or update debate pages when the ingest raises contested cross-source interpretation; promote contested conclusions only after user acceptance
8. rebuild `wiki/index.md`
9. append an entry to `wiki/log.md`
10. mark successfully processed hashes in `state/manifest.json`

## Query workflow

- Search the local wiki first
- Read the most relevant pages
- Answer in prose with local citations
- Use source `published` metadata for chronology-sensitive analysis when available
- If the answer is durable, save it as a `synthesis` page and update the index/log
- If the answer depends on disputed interpretation across curated sources, create or update a `debate` page first. Promote only after the user accepts the conclusion or explicitly asks for promotion.

## Lint workflow

The weekly lint pass checks for:

- orphan pages
- broken links
- stale or conflicting claims
- repeated concepts lacking their own page
- source pages with weak or missing connections
- debate pages that duplicate synthesis pages without clear workbench/promoted status

The lint pass should repair the wiki directly when safe and log what changed. For now, lint may flag debates that appear ready for decision, but must not close, delete, archive, or promote debate conclusions without explicit user instruction.

## PDF parsing

- PDFs are parsed through MinerU Precision Extract, not by local text extraction.
- The integration uses the local-file upload flow: request upload URLs, upload the file, poll the batch result, then download the returned zip and cache `full.md` with its referenced assets.
- Cached PDF markdown is reused when the file hash has not changed.
- Markdown and text sources are read directly from `raw/` and do not get sidecars.
- Precision Extract currently supports up to 200 MB and 600 pages per file, and requires `MINERU_API_TOKEN`.
- `MINERU_OCR_ENABLE=auto` is the default policy:
  - if the PDF appears to have a healthy text layer, parse with OCR disabled
  - if the PDF looks scanned or image-only, parse with OCR enabled
  - if a non-OCR parse fails or returns very weak output, retry once with OCR enabled

## Video parsing

- Video sources are Markdown descriptors under `raw/videos/`.
- A video descriptor must use `source_type: video` and currently uses `parser: asr`.
- The descriptor body is user-provided study context and should be included in downstream wiki ingest.
- `src/cron/add_video.py` creates descriptors from a URL and fills frontmatter from `yt-dlp` metadata.
- The scanner downloads audio with `yt-dlp`, normalizes it with `ffmpeg`, uploads the normalized audio through OSS, and transcribes it through DashScope Filetrans.
- The default ASR model is `fun-asr`, with diarization enabled for multi-speaker material.
- Generated video parser artifacts live under `state/extracted/`, including `yt_dlp_metadata.json`, `asr_result.json`, `transcript.md`, `materialization.json`, and `full.md`.
- Video parser output is not actively chunked; large transcript segmented reading is the ingest agent's responsibility.
