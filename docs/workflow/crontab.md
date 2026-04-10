# Crontab

Use local time. The intended pattern is one quiet late-night reindex run and one weekly maintenance run.

## Suggested schedule

```cron
# Nightly autonomous reindex at 01:30
30 1 * * * WIKI_DIR="${WIKI_DIR:-$HOME/ontic-wiki}"; cd "$WIKI_DIR" && ./.venv/bin/python src/cron/reindex.py >> /tmp/ontic-wiki-reindex.log 2>&1

# Weekly lint every Sunday at 02:00
0 2 * * 0 WIKI_DIR="${WIKI_DIR:-$HOME/ontic-wiki}"; cd "$WIKI_DIR" && ./.venv/bin/python src/cron/lint.py >> /tmp/ontic-wiki-lint.log 2>&1
```

## Notes

- Run `uv sync` before enabling cron so `.venv/` exists.
- Copy `.env.example` to `.env`. Leave `OPENCODE_PASSWORD` empty if your OpenCode server does not require auth.
- Leave `OPENCODE_DIRECTORY` empty unless you need to override the repo root explicitly.
- Set `MINERU_API_TOKEN` if you want PDFs parsed during reindex.
- The cron examples use `WIKI_DIR` with a fallback to `$HOME/ontic-wiki` so the repo can be moved without rewriting every line.
- The reindex job assumes the repo is quiet at the scheduled time.
- Runtime logs are written to `/tmp/ontic-wiki-reindex.log` and `/tmp/ontic-wiki-lint.log`.
- If you want to test without calling the agent, run:

```bash
.venv/bin/python src/cron/reindex.py --scan-only
.venv/bin/python src/cron/lint.py --scan-only
```
