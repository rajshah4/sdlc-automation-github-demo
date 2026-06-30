#!/usr/bin/env python3
"""Disable OpenHands automations by ID without printing secrets."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from urllib.error import HTTPError
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


def patch_enabled(host: str, api_key: str, automation_id: str, enabled: bool) -> dict:
    endpoint = host.rstrip("/") + f"/api/automation/v1/{automation_id}"
    request = Request(
        endpoint,
        data=json.dumps({"enabled": enabled}).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="PATCH",
    )
    try:
        with urlopen(request, timeout=60) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"OpenHands API returned {exc.code}: {body}") from exc


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--env-file", type=Path, help="load KEY=value entries without printing values")
    parser.add_argument("--enable", action="store_true", help="enable instead of disable")
    parser.add_argument("automation_ids", nargs="+")
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

    enabled = bool(args.enable)
    for automation_id in args.automation_ids:
        patch_enabled(host, api_key, automation_id, enabled)
        state = "enabled" if enabled else "disabled"
        print(f"{state} {automation_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
