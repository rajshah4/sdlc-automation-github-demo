#!/usr/bin/env python3
"""List OpenHands automations without printing prompts or secrets."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any
from urllib.request import Request, urlopen


def load_env_file(path: Path) -> None:
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        if not key or not key.replace("_", "").isalnum():
            continue
        os.environ.setdefault(key, value.strip().strip("'").strip('"'))


def api_get(host: str, api_key: str, path: str) -> dict[str, Any]:
    request = Request(
        host.rstrip("/") + path,
        headers={"Authorization": f"Bearer {api_key}"},
        method="GET",
    )
    with urlopen(request, timeout=60) as response:
        return json.loads(response.read().decode("utf-8"))


def extract_items(payload: dict[str, Any]) -> list[dict[str, Any]]:
    for key in ("items", "data", "automations"):
        value = payload.get(key)
        if isinstance(value, list):
            return value
    if isinstance(payload, list):
        return payload
    return []


def summarize(automation: dict[str, Any]) -> dict[str, Any]:
    trigger = automation.get("trigger") or {}
    return {
        "id": automation.get("id"),
        "name": automation.get("name"),
        "enabled": automation.get("enabled"),
        "keep_alive": automation.get("keep_alive"),
        "model": automation.get("model"),
        "timeout": automation.get("timeout"),
        "trigger": {
            "type": trigger.get("type"),
            "source": trigger.get("source"),
            "on": trigger.get("on"),
            "filter": trigger.get("filter"),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--env-file", type=Path, help="load KEY=value entries without printing values")
    parser.add_argument("--limit", type=int, default=100)
    parser.add_argument("--details", action="store_true", help="fetch each automation by id before summarizing")
    args = parser.parse_args()

    if args.env_file:
        load_env_file(args.env_file)

    host = (
        os.getenv("OPENHANDS_HOST_GITHUB")
        or os.getenv("OPENHANDS_HOST_RAJISTICS")
        or os.getenv("OPENHANDS_HOST")
        or "https://app.replicated.rajistics.com"
    )
    api_key = (
        os.getenv("OPENHANDS_API_KEY_ORG")
        or os.getenv("OPENHANDS_API_KEY_GITHUB")
        or os.getenv("OPENHANDS_API_KEY_RAJISTICS")
        or os.getenv("OPENHANDS_API_KEY")
    )
    if not api_key:
        raise SystemExit("OPENHANDS_API_KEY_ORG, OPENHANDS_API_KEY_GITHUB, OPENHANDS_API_KEY_RAJISTICS, or OPENHANDS_API_KEY is required")

    payload = api_get(host, api_key, f"/api/automation/v1?limit={args.limit}")
    items = extract_items(payload)
    if args.details:
        items = [api_get(host, api_key, f"/api/automation/v1/{item['id']}") for item in items if item.get("id")]

    print(json.dumps([summarize(item) for item in items], indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
