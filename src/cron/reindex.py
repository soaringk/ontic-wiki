#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

SRC_ROOT = Path(__file__).resolve().parents[1]
if str(SRC_ROOT) not in sys.path:
    sys.path.append(str(SRC_ROOT))

from client.opencode import OpenCodeClient
from wiki_agent.config import AGENTS_PATH, DEFAULT_REINDEX_MODEL, ROOT_DIR, WORKFLOW_PATH
from wiki_agent.repository import mark_paths_ingested, scan_sources, utc_now


PROMPT_TEMPLATE = """
Role: Study Wiki Reindexer
Goal: Turn newly discovered study materials into updated wiki knowledge.
Latest report: {report_path}
Repo guide: {agents_path}
Workflow guide: {workflow_path}

Execution requirements:
1. Read the repo guide and workflow guide before changing files.
2. Read the latest report and process every pending source listed there.
3. For each pending source:
   - read the raw file directly for markdown/text sources
   - read the extracted PDF markdown sidecar when `text_path` exists
   - read the generated video parser output when `source_type` is `video` and `text_path` exists
   - create or update one source page under `wiki/sources/`
   - update any affected topic and concept pages under `wiki/topics/` and `wiki/concepts/`
4. Rebuild `wiki/index.md` so it reflects the current wiki contents.
5. Append a new `wiki/log.md` entry using `## [YYYY-MM-DD] reindex | ...`.
6. If the report lists blocked or unsupported files, log them briefly in `wiki/log.md`.
7. Keep the wiki English-first and avoid duplicate pages.

Important constraints:
- Never modify files under `raw/`.
- Prefer updating existing pages over creating near-duplicates.
- The wiki is the durable artifact. The chat response can stay brief.
- For video sources, treat descriptor body content as user-provided notes and incorporate it when relevant.
- For video sources, treat transcripts as raw ASR that may contain recognition errors and colloquial phrasing.
- Preserve `source_type: video`, `parser: asr`, and real `published` metadata in source-page frontmatter when available.
""".strip()


def main() -> int:
    parser = argparse.ArgumentParser(description="Nightly autonomous reindex for the study wiki.")
    parser.add_argument("--model", default=DEFAULT_REINDEX_MODEL, help="Model ID to use")
    parser.add_argument("--scan-only", action="store_true", help="Only refresh manifest and reports")
    parser.add_argument("--delete", action="store_true", help="Delete the OpenCode session after completion")
    args = parser.parse_args()

    summary = scan_sources()
    actionable = bool(summary.pending_paths or summary.blocked_paths or summary.unsupported_paths)
    relative_report_path = summary.report_path.relative_to(ROOT_DIR).as_posix()
    print(f"scan_time={summary.scan_time}")
    print(f"pending={len(summary.pending_paths)} blocked={len(summary.blocked_paths)} unsupported={len(summary.unsupported_paths)}")
    print(f"report={relative_report_path}")

    if args.scan_only or not actionable:
        return 0

    client = OpenCodeClient()
    session_id = client.create_session(f"Ontic Wiki Reindex {summary.scan_time}")
    prompt = PROMPT_TEMPLATE.format(
        report_path=relative_report_path,
        agents_path=AGENTS_PATH,
        workflow_path=WORKFLOW_PATH,
    )
    client.send_message(session_id, prompt, model_id=args.model)
    completed = client.wait_for_session_complete(session_id)
    if not completed:
        print("reindex session did not complete before timeout", file=sys.stderr)
        return 1

    mark_paths_ingested(summary.pending_paths, utc_now())
    if args.delete:
        client.delete_session(session_id)
    print(f"session={session_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
