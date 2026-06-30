#!/usr/bin/env python3
"""Validate a label-only GitHub event fixture and report the OpenHands trigger."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

AUTOMATION_LABELS = {
    "openhands-context",
    "openhands-build",
    "openhands-review",
    "openhands-qa",
    "openhands-incident",
}


def summarize(payload: dict) -> dict:
    event_name = payload.get("_event_name")
    label = (payload.get("label") or {}).get("name", "")
    repo = payload.get("repository") or {}
    if event_name == "issues":
        issue = payload.get("issue") or {}
        return {
            "event_type": f"issues.{payload.get('action', 'unknown')}",
            "repository": repo.get("full_name"),
            "trigger": label,
            "issue": {
                "number": issue.get("number"),
                "title": issue.get("title"),
                "labels": [item.get("name") for item in issue.get("labels", [])],
            },
        }
    if event_name == "pull_request":
        pr = payload.get("pull_request") or {}
        return {
            "event_type": f"pull_request.{payload.get('action', 'unknown')}",
            "repository": repo.get("full_name"),
            "trigger": label,
            "pull_request": {
                "number": pr.get("number"),
                "title": pr.get("title"),
                "source_branch": (pr.get("head") or {}).get("ref"),
                "target_branch": (pr.get("base") or {}).get("ref"),
            },
        }
    raise ValueError(f"Unsupported fixture _event_name: {event_name}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixture", required=True)
    args = parser.parse_args()

    payload = json.loads(Path(args.fixture).read_text(encoding="utf-8"))
    data = summarize(payload)
    print(json.dumps(data, indent=2, sort_keys=True))
    trigger = data["trigger"]
    if trigger not in AUTOMATION_LABELS:
        print(f"No automation trigger found: {trigger}", file=sys.stderr)
        return 1
    print(f"Matched automation trigger: {trigger}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
