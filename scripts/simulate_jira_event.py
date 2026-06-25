#!/usr/bin/env python3
"""Validate a Jira event fixture and report the OpenHands trigger."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def summarize(payload: dict) -> dict:
    event_name = payload.get("webhookEvent")
    issue = payload.get("issue") or {}
    fields = issue.get("fields") or {}
    project_key = payload.get("projectKey") or ((fields.get("project") or {}).get("key"))
    issue_type = (fields.get("issuetype") or {}).get("name")
    issue_key = payload.get("issueKey") or issue.get("key")
    comment_id = payload.get("commentId") or (payload.get("comment") or {}).get("id")
    trigger = ""
    if event_name == "comment_created" and project_key == "KAN":
        trigger = "openhands-build"
    if event_name == "jira:issue_created" and project_key == "KAN" and issue_type == "Task":
        trigger = "openhands-build-direct"
    return {
        "event_type": event_name,
        "project_key": project_key,
        "issue_type": issue_type,
        "issue_key": issue_key,
        "comment_id": comment_id,
        "summary": fields.get("summary"),
        "trigger": trigger,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixture", required=True)
    args = parser.parse_args()

    payload = json.loads(Path(args.fixture).read_text(encoding="utf-8"))
    data = summarize(payload)
    print(json.dumps(data, indent=2, sort_keys=True))
    if data["trigger"] not in {"openhands-build", "openhands-build-direct"}:
        print("No Jira automation trigger found", file=sys.stderr)
        return 1
    print(f"Matched Jira automation trigger: {data['trigger']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
