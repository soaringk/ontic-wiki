# AGENTS.md - Ontic Wiki

This repository is a self-maintaining study wiki.

## Core contract

- `raw/` contains user-provided source material. Never modify files there.
- `wiki/` is the maintained knowledge layer. This is where summaries, topic pages, concept pages, and synthesis pages live.
- `state/` contains machine state, extracted text, and ingest reports used by automation.

## Every session

Before changing the wiki:

1. Read [`docs/workflow/study_wiki.md`](./docs/workflow/study_wiki.md).
2. Read [`wiki/index.md`](./wiki/index.md) to understand existing pages.
3. If the task is an ingest or cron-triggered maintenance run, read the latest report under [`state/reports/`](./state/reports/).

## Query behavior

- Answer from the local wiki first.
- Use citations to local wiki pages when possible.
- Valuable query answers/conversation may be filed into `wiki/synthesis/`.
- Every answer is based on facts and logic, not sycophancy.

## Timeliness

- Timeliness-sensitive analysis must use each source's actual `published` field when it is present in the raw material.
- Do not substitute local ingest dates such as wiki `created`, wiki `updated`, or raw `created` for the source's publication time.
- When creating or updating `wiki/sources/` pages, carry the raw `published` value into source-page frontmatter when it is present and meaningful.
- If the raw `published` field is blank, missing, or ambiguous, preserve that uncertainty explicitly instead of inventing a date.

## Page placement

- Source pages: `wiki/sources/`
- Topic pages: `wiki/topics/`
- Concept pages: `wiki/concepts/`
- Query-derived durable analyses: `wiki/synthesis/`

## Constraints

- Preserve the raw/wiki boundary.
- Keep the wiki English-first.
- Prefer updating existing pages over creating near-duplicates.
- Rebuild `wiki/index.md` and append `wiki/log.md` whenever an ingest or lint run changes the wiki.
