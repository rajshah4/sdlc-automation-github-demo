#!/usr/bin/env python3
"""Register the opt-in Replicated Jira delegated factory automation."""

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
SPEC_PATH = REPO_ROOT / "automations" / "replicated-jira-delegated-factory" / "automation.prompt-preset.json"


def load_env_file(path: Path) -> None:
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        if key and key.replace("_", "").isalnum():
            os.environ.setdefault(key, value.strip().strip("'").strip('"'))


def expand_env(value: Any) -> Any:
    if isinstance(value, str):
        return os.path.expandvars(value)
    if isinstance(value, list):
        return [expand_env(item) for item in value]
    if isinstance(value, dict):
        return {key: expand_env(item) for key, item in value.items()}
    return value


def load_request() -> dict[str, Any]:
    spec = json.loads(SPEC_PATH.read_text(encoding="utf-8"))
    prompt = (SPEC_PATH.parent / spec["prompt_file"]).read_text(encoding="utf-8")
    payload: dict[str, Any] = {
        "name": spec["name"],
        "prompt": prompt,
        "trigger": spec["trigger"],
        "repos": spec["repos"],
    }
    for optional in ("timeout", "model", "keep_alive"):
        if optional in spec:
            payload[optional] = spec[optional]
    if "llm_profile" in spec:
        if "model" in payload:
            raise ValueError("Use either model or llm_profile in the automation spec, not both")
        payload["model"] = spec["llm_profile"]
    return expand_env(payload)


def post_prompt_preset(host: str, api_key: str, payload: dict[str, Any]) -> dict[str, Any]:
    request = Request(
        host.rstrip("/") + "/api/automation/v1/preset/prompt",
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


def automation_api_key() -> str | None:
    return (
        os.getenv("OPENHANDS_API_KEY_ORG")
        or os.getenv("OPENHANDS_API_KEY_JIRA")
        or os.getenv("OPENHANDS_API_KEY_RAJISTICS")
        or os.getenv("OPENHANDS_API_KEY")
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true")
    mode.add_argument("--apply", action="store_true")
    parser.add_argument("--env-file", type=Path)
    parser.add_argument("--project-key", default="KAN")
    parser.add_argument("--repo-url", default="https://github.com/rajshah4/sdlc-automation-github-demo")
    parser.add_argument("--ref", default="main", help="Git ref cloned by the automation and used by child conversations")
    args = parser.parse_args()

    if args.env_file:
        load_env_file(args.env_file)
    os.environ["JIRA_DEMO_PROJECT_KEY"] = args.project_key
    os.environ["GITHUB_DEMO_REPO_URL"] = args.repo_url
    os.environ["GITHUB_DEMO_REF"] = args.ref

    payload = load_request()
    if not args.apply:
        print(json.dumps({"spec": str(SPEC_PATH.relative_to(REPO_ROOT)), "request": payload}, indent=2))
        return 0

    host = (
        os.getenv("OPENHANDS_HOST_JIRA")
        or os.getenv("OPENHANDS_HOST_RAJISTICS")
        or os.getenv("OPENHANDS_HOST")
        or "https://app.replicated.rajistics.com"
    )
    api_key = automation_api_key()
    if not api_key:
        print("OPENHANDS_API_KEY_RAJISTICS or OPENHANDS_API_KEY is required for --apply", file=sys.stderr)
        return 2

    result = post_prompt_preset(host, api_key, payload)
    print(json.dumps({"spec": str(SPEC_PATH.relative_to(REPO_ROOT)), "result": result}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
