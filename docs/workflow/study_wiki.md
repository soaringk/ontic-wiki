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
- Supported in v1: `.md`, `.txt`, `.pdf`

### Machine state

- Path: `state/`
- `manifest.json` tracks file hashes and ingest state
- `extracted/` stores cached PDF-to-Markdown bundles, including `full.md` and extracted assets
- `reports/` stores the latest ingest and lint reports

### Wiki

- Path: `wiki/`
- Agent-maintained Markdown pages
- Main page types:
  - `source`
  - `topic`
  - `concept`
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
source_type: markdown|text|pdf
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

## Ingest workflow

The nightly reindex job does this:

1. scan `raw/`
2. detect new or changed supported files
3. refresh cached PDF Markdown bundles under `state/extracted/` only for PDFs
4. write a machine-readable and human-readable report under `state/reports/`
5. trigger an agentic ingest pass
6. update source/topic/concept pages
7. rebuild `wiki/index.md`
8. append an entry to `wiki/log.md`
9. mark successfully processed hashes in `state/manifest.json`

## Query workflow

- Search the local wiki first
- Read the most relevant pages
- Answer in prose with local citations
- Use source `published` metadata for chronology-sensitive analysis when available
- If the answer is durable, save it as a `synthesis` page and update the index/log

## Lint workflow

The weekly lint pass checks for:

- orphan pages
- broken links
- stale or conflicting claims
- repeated concepts lacking their own page
- source pages with weak or missing connections

The lint pass should repair the wiki directly when safe and log what changed.

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
