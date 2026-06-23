#!/usr/bin/env python3
"""Register GitHub OpenHands automations with the prompt preset API."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any
from urllib.error import HTTPError
from urllib.request import Request, urlopen


REPO_ROOT = Path(__file__).resolve().parents[1]
AUTOMATION_ROOT = REPO_ROOT / "automations" / "github"


def expand_env(value: Any) -> Any:
    if isinstance(value, str):
        return os.path.expandvars(value)
    if isinstance(value, list):
        return [expand_env(item) for item in value]
    if isinstance(value, dict):
        return {key: expand_env(item) for key, item in value.items()}
    return value


def load_request(spec_path: Path) -> dict[str, Any]:
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    prompt_path = spec_path.parent / spec["prompt_file"]
    request: dict[str, Any] = {
        "name": spec["name"],
        "prompt": prompt_path.read_text(encoding="utf-8"),
        "trigger": spec["trigger"],
    }
    if "timeout" in spec:
        request["timeout"] = spec["timeout"]
    if "repos" in spec:
        request["repos"] = spec["repos"]
    return expand_env(request)


def post_prompt_preset(host: str, api_key: str, payload: dict[str, Any]) -> dict[str, Any]:
    endpoint = host.rstrip("/") + "/api/automation/v1/preset/prompt"
    request = Request(
        endpoint,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urlopen(request, timeout=60) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"OpenHands API returned {exc.code}: {body}") from exc


def automation_specs() -> list[Path]:
    return sorted(AUTOMATION_ROOT.glob("openhands-*/automation.prompt-preset.json"))


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true", help="print requests without creating automations")
    mode.add_argument("--apply", action="store_true", help="create automations through OpenHands API")
    args = parser.parse_args()

    dry_run = not args.apply
    host = os.getenv("OPENHANDS_HOST_GITHUB") or os.getenv("OPENHANDS_HOST") or "https://app.all-hands.dev"
    api_key = os.getenv("OPENHANDS_API_KEY_GITHUB") or os.getenv("OPENHANDS_API_KEY")

    results: list[dict[str, Any]] = []
    for spec_path in automation_specs():
        payload = load_request(spec_path)
        if dry_run:
            print(json.dumps({"spec": str(spec_path.relative_to(REPO_ROOT)), "request": payload}, indent=2))
            continue
        if not api_key:
            print("OPENHANDS_API_KEY_GITHUB or OPENHANDS_API_KEY is required for --apply", file=sys.stderr)
            return 2
        result = post_prompt_preset(host, api_key, payload)
        results.append({"spec": str(spec_path.relative_to(REPO_ROOT)), "result": result})
        print(f"Registered {payload['name']}: {result.get('id', 'unknown-id')}")

    if results:
        output_path = REPO_ROOT / "automation-registration-results.json"
        output_path.write_text(json.dumps(results, indent=2, sort_keys=True), encoding="utf-8")
        print(f"Wrote {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

