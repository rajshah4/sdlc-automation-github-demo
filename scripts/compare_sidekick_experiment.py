#!/usr/bin/env python3
"""Compare control and sidekick Jira-to-PR experiment runs.

Input is an offline JSON file so the comparison can include token/cost numbers
from whichever observability surface is available.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def parse_time(value: str | None) -> datetime | None:
    if not value:
        return None
    normalized = value.replace("Z", "+00:00")
    return datetime.fromisoformat(normalized).astimezone(timezone.utc)


def minutes_between(start: str | None, end: str | None) -> float | None:
    start_at = parse_time(start)
    end_at = parse_time(end)
    if not start_at or not end_at:
        return None
    return round((end_at - start_at).total_seconds() / 60, 2)


def money(value: Any) -> str:
    if value is None:
        return "n/a"
    return f"${float(value):.4f}"


def duration(value: float | None) -> str:
    return "n/a" if value is None else f"{value:.2f} min"


def row(run: dict[str, Any]) -> list[str]:
    time_to_pr = minutes_between(run.get("created_at"), run.get("pr_opened_at") or run.get("completed_at"))
    success = "yes" if run.get("success") else "no"
    return [
        str(run.get("variant", "")),
        str(run.get("jira_key", "")),
        duration(time_to_pr),
        str(run.get("model", "")),
        money(run.get("cost_usd")),
        str(run.get("readability_score", "n/a")),
        success,
        str(run.get("conversation_url", "")),
        str(run.get("pr_url", "")),
    ]


def render_markdown(payload: dict[str, Any]) -> str:
    runs = payload.get("runs", [])
    headers = [
        "Variant",
        "Jira",
        "Time to PR",
        "Model",
        "Cost",
        "Readability",
        "Success",
        "Conversation",
        "PR",
    ]
    lines = [
        "# Sidekick Experiment Comparison",
        "",
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for run in runs:
        lines.append("| " + " | ".join(row(run)) + " |")

    notes = payload.get("notes")
    if notes:
        lines.extend(["", "## Notes", "", str(notes)])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input_json", type=Path)
    args = parser.parse_args()
    payload = json.loads(args.input_json.read_text(encoding="utf-8"))
    print(render_markdown(payload))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
