#!/usr/bin/env python3
"""Classify a GitHub webhook fixture using the demo provider adapter."""

from __future__ import annotations

import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT))

from providers.github.adapter import (  # noqa: E402
    normalize_issue_comment,
    normalize_issues_event,
    normalize_pull_request_event,
)


def main() -> int:
    payload = json.load(sys.stdin)
    event_name = payload.get("_event_name")
    if event_name == "issue_comment":
        event = normalize_issue_comment(payload)
    elif event_name == "issues":
        event = normalize_issues_event(payload)
    elif event_name == "pull_request":
        event = normalize_pull_request_event(payload)
    else:
        raise SystemExit(f"Unsupported _event_name: {event_name}")
    print(json.dumps(event.to_dict(), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
