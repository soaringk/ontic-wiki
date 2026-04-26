from __future__ import annotations

import json
from collections.abc import Mapping
from typing import Any


def parse_frontmatter(markdown: str) -> tuple[dict[str, Any], str]:
    if not markdown.startswith("---\n"):
        return {}, markdown

    lines = markdown.splitlines()
    if not lines or lines[0] != "---":
        return {}, markdown

    end_index: int | None = None
    for index, line in enumerate(lines[1:], start=1):
        if line == "---":
            end_index = index
            break

    if end_index is None:
        return {}, markdown

    metadata: dict[str, Any] = {}
    for line in lines[1:end_index]:
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or ":" not in stripped:
            continue
        key, raw_value = stripped.split(":", 1)
        key = key.strip()
        if not key:
            continue
        metadata[key] = parse_frontmatter_value(raw_value.strip())

    body = "\n".join(lines[end_index + 1 :])
    if markdown.endswith("\n"):
        body += "\n"
    return metadata, body


def parse_frontmatter_value(raw_value: str) -> Any:
    if raw_value == "":
        return ""
    if raw_value in {"true", "True"}:
        return True
    if raw_value in {"false", "False"}:
        return False
    if raw_value in {"null", "None", "~"}:
        return None
    if raw_value.startswith(('"', "'")):
        try:
            return json.loads(raw_value)
        except json.JSONDecodeError:
            return raw_value.strip("\"'")
    try:
        return int(raw_value)
    except ValueError:
        pass
    try:
        return float(raw_value)
    except ValueError:
        return raw_value


def render_frontmatter(metadata: Mapping[str, Any], body: str) -> str:
    lines = ["---"]
    for key, value in metadata.items():
        lines.append(f"{key}: {format_frontmatter_value(value)}")
    lines.extend(["---", ""])
    lines.append(body.rstrip())
    return "\n".join(lines).rstrip() + "\n"


def format_frontmatter_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int | float):
        return str(value)
    return json.dumps(str(value), ensure_ascii=False)

