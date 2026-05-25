# AGENTS.md - Ontic Wiki

This repository is a self-maintaining study wiki.

## Canonical workflow

[`docs/workflow/study_wiki.md`](./docs/workflow/study_wiki.md) is the canonical workflow for capture, query, index, lint, parser behavior, page placement, and source metadata rules. Read it before acting in this repository.

## Core boundaries

- `raw/` contains source material captured for later automation; do not place agent-written summaries or parser outputs there.
- `wiki/` is the maintained knowledge layer.
- `state/` contains machine state, extracted text, and reindex reports used by automation.
- Read [`wiki/index.md`](./wiki/index.md) before answering from or changing the wiki.
- If the task is a reindex or cron-triggered maintenance run, read the latest report under [`state/reports/`](./state/reports/).
