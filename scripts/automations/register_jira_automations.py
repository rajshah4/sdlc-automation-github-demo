#!/usr/bin/env python3
"""Register Jira OpenHands automations with the prompt preset API."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any
from urllib.error import HTTPError
from urllib.request import Request, urlopen


REPO_ROOT = Path(__file__).resolve().parents[2]
AUTOMATION_ROOT = REPO_ROOT / "automations" / "jira"
DEFAULTS = {
    "JIRA_DEMO_PROJECT_KEY": "KAN",
    "GITHUB_DEMO_REPO_URL": "https://github.com/rajshah4/sdlc-automation-github-demo",
    "GITHUB_DEMO_REF": "main",
}


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
        "name": expand_env(spec["name"]),
        "prompt": prompt_path.read_text(encoding="utf-8"),
        "trigger": expand_env(spec["trigger"]),
    }
    for optional in ("timeout", "keep_alive", "repos", "model"):
        if optional in spec:
            request[optional] = expand_env(spec[optional])
    return request


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


def automation_specs(include: set[str] | None) -> list[Path]:
    specs = sorted(AUTOMATION_ROOT.glob("jira-to-story*/automation.prompt-preset.json"))
    if include:
        specs = [path for path in specs if path.parent.name in include]
    return specs


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true", help="print requests without creating automations")
    mode.add_argument("--apply", action="store_true", help="create automations through OpenHands API")
    parser.add_argument("--env-file", type=Path, help="load KEY=value entries without printing values")
    parser.add_argument("--include", action="append", help="automation folder to include; repeatable")
    parser.add_argument("--project-key", help="set JIRA_DEMO_PROJECT_KEY for this run")
    parser.add_argument("--repo-url", help="set GITHUB_DEMO_REPO_URL for this run")
    parser.add_argument("--ref", help="set GITHUB_DEMO_REF for the cloned repository")
    args = parser.parse_args()

    if args.env_file:
        load_env_file(args.env_file)
    for key, value in DEFAULTS.items():
        os.environ.setdefault(key, value)
    if args.project_key:
        os.environ["JIRA_DEMO_PROJECT_KEY"] = args.project_key
    if args.repo_url:
        os.environ["GITHUB_DEMO_REPO_URL"] = args.repo_url
    if args.ref:
        os.environ["GITHUB_DEMO_REF"] = args.ref

    dry_run = not args.apply
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

    results: list[dict[str, Any]] = []
    for spec_path in automation_specs(set(args.include or [])):
        payload = load_request(spec_path)
        if dry_run:
            print(
                json.dumps(
                    {
                        "spec": str(spec_path.relative_to(REPO_ROOT)),
                        "request": payload,
                    },
                    indent=2,
                )
            )
            continue
        if not api_key:
            print("An OpenHands API key is required for --apply", file=sys.stderr)
            return 2
        result = post_prompt_preset(host, api_key, payload)
        results.append({"spec": str(spec_path.relative_to(REPO_ROOT)), "result": result})
        print(f"Registered {payload['name']}: {result.get('id', 'unknown-id')}")

    if results:
        output_path = REPO_ROOT / "jira-automation-registration-results.json"
        output_path.write_text(json.dumps(results, indent=2, sort_keys=True), encoding="utf-8")
        print(f"Wrote {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
