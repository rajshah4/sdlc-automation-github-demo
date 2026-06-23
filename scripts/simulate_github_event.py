#!/usr/bin/env python3
"""Normalize a GitHub event fixture and report the OpenHands trigger."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from providers.github.adapter import (  # noqa: E402
    AUTOMATION_LABELS,
    normalize_issue_comment,
    normalize_issues_event,
    normalize_pull_request_event,
)


def normalize(payload: dict) -> object:
    event_name = payload.get("_event_name")
    if event_name == "issue_comment":
        return normalize_issue_comment(payload)
    if event_name == "issues":
        return normalize_issues_event(payload)
    if event_name == "pull_request":
        return normalize_pull_request_event(payload)
    raise ValueError(f"Unsupported fixture _event_name: {event_name}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixture", required=True)
    args = parser.parse_args()

    payload = json.loads(Path(args.fixture).read_text(encoding="utf-8"))
    event = normalize(payload)
    data = event.to_dict()
    print(json.dumps(data, indent=2, sort_keys=True))
    trigger = data["trigger"]["name"]
    if trigger not in AUTOMATION_LABELS:
        print(f"No automation trigger found: {trigger}", file=sys.stderr)
        return 1
    print(f"Matched automation trigger: {trigger}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

