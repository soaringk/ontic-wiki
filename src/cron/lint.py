#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

SRC_ROOT = Path(__file__).resolve().parents[1]
if str(SRC_ROOT) not in sys.path:
    sys.path.append(str(SRC_ROOT))

from client.opencode import OpenCodeClient
from wiki_agent.config import AGENTS_PATH, DEFAULT_LINT_MODEL, ROOT_DIR, WORKFLOW_PATH
from wiki_agent.repository import utc_now, write_lint_report


PROMPT_TEMPLATE = """
Role: Study Wiki Lint Maintainer
Goal: Audit and repair the local wiki.
Latest report: {report_path}
Repo guide: {agents_path}
Workflow guide: {workflow_path}

Execution requirements:
1. Read the repo guide and workflow guide first.
2. Read the latest lint report before editing.
3. Audit the wiki for orphan pages, broken links, stale claims, weak source connections, and obvious duplicate pages.
4. Repair safe issues directly.
5. Rebuild `wiki/index.md` if page inventory or summaries change.
6. Append a new `wiki/log.md` entry using `## [YYYY-MM-DD] lint | ...`.

Constraints:
- Do not modify files under `raw/`.
- Keep the wiki English-first.
- Prefer compact maintenance changes over broad rewrites.
""".strip()


def main() -> int:
    parser = argparse.ArgumentParser(description="Weekly autonomous lint pass for the study wiki.")
    parser.add_argument("--model", default=DEFAULT_LINT_MODEL, help="Model ID to use")
    parser.add_argument("--scan-only", action="store_true", help="Only refresh the lint report")
    parser.add_argument("--delete", action="store_true", help="Delete the OpenCode session after completion")
    args = parser.parse_args()

    report_path = write_lint_report(utc_now())
    relative_report_path = report_path.relative_to(ROOT_DIR).as_posix()
    print(f"report={relative_report_path}")
    if args.scan_only:
        return 0

    client = OpenCodeClient()
    session_id = client.create_session("Ontic Wiki Lint")
    prompt = PROMPT_TEMPLATE.format(
        report_path=relative_report_path,
        agents_path=AGENTS_PATH,
        workflow_path=WORKFLOW_PATH,
    )
    client.send_message(session_id, prompt, model_id=args.model)
    completed = client.wait_for_session_complete(session_id)
    if not completed:
        print("lint session did not complete before timeout", file=sys.stderr)
        return 1

    if args.delete:
        client.delete_session(session_id)
    print(f"session={session_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
