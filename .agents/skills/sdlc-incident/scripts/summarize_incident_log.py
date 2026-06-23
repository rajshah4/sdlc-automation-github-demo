#!/usr/bin/env python3
"""Summarize a Petstore incident log payload from stdin."""

from __future__ import annotations

import json
import sys


def main() -> int:
    payload = json.load(sys.stdin)
    incident = payload.get("incident") or {}
    summary = {
        "incident_type": incident.get("type"),
        "safe_to_remediate": bool(incident.get("safe_to_remediate")),
        "component": payload.get("component"),
        "operation": payload.get("operation"),
        "error_code": payload.get("error_code"),
        "pending_pet_ids": payload.get("pending_pet_ids", []),
    }
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

