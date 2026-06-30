#!/usr/bin/env python3
"""Live connection preflight for the Jira-to-PR demo.

This script performs read-only checks against the live services used by the
demo. It intentionally does not create Jira issues, labels, PRs, or automation
runs.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.error import HTTPError
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen


REPO_ROOT = Path(__file__).resolve().parents[1]
REQUIRED_GITHUB_LABELS = {
    "openhands-qa",
    "openhands:in-progress",
    "openhands:done",
}
DEFAULTS = {
    "OPENHANDS_HOST": "https://app.replicated.rajistics.com",
    "JIRA_DEMO_PROJECT_KEY": "KAN",
    "GITHUB_DEMO_REPOSITORY": "rajshah4/sdlc-automation-github-demo",
    "GITHUB_DEMO_REPO_URL": "https://github.com/rajshah4/sdlc-automation-github-demo",
}


@dataclass(frozen=True)
class AutomationIds:
    jira_main: str
    jira_control: str
    jira_sidekick: str
    jira_sidekick_v2: str
    github_qa: str


DEFAULT_AUTOMATION_IDS = AutomationIds(
    jira_main="a22f4cfd-d194-4566-b773-89fc903fd9d6",
    jira_control="b12d471e-797b-4010-bef7-c02fbb3c8bed",
    jira_sidekick="0aad5e83-1b19-49f8-a985-da459b0c4112",
    jira_sidekick_v2="add32647-efc4-42ef-adc1-93c5db211991",
    github_qa="b3192e16-171a-4ec3-8028-9514a7f372fe",
)


def load_env_file(path: Path) -> None:
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        if key and key.replace("_", "").isalnum():
            os.environ.setdefault(key, value.strip().strip("'").strip('"'))


def env_first(*names: str) -> str:
    return next((os.getenv(name, "") for name in names if os.getenv(name)), "")


def apply_defaults() -> None:
    for key, value in DEFAULTS.items():
        os.environ.setdefault(key, value)


def fail(failures: list[str], message: str) -> None:
    failures.append(message)
    print(f"FAIL: {message}")


def ok(message: str) -> None:
    print(f"OK: {message}")


def http_json(url: str, headers: dict[str, str]) -> Any:
    request = Request(url, headers=headers, method="GET")
    try:
        with urlopen(request, timeout=60) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code} from {url}: {body[:500]}") from exc


def gh_json(path: str) -> Any:
    result = subprocess.run(
        ["gh", "api", path],
        check=False,
        text=True,
        capture_output=True,
    )
    if result.returncode != 0:
        detail = (result.stderr or result.stdout).strip()
        raise RuntimeError(detail or f"gh api {path} failed")
    return json.loads(result.stdout)


def automation_ids_from_env() -> AutomationIds:
    return AutomationIds(
        jira_main=os.getenv("JIRA_MAIN_AUTOMATION_ID", DEFAULT_AUTOMATION_IDS.jira_main),
        jira_control=os.getenv(
            "JIRA_CONTROL_AUTOMATION_ID", DEFAULT_AUTOMATION_IDS.jira_control
        ),
        jira_sidekick=os.getenv(
            "JIRA_SIDEKICK_AUTOMATION_ID", DEFAULT_AUTOMATION_IDS.jira_sidekick
        ),
        jira_sidekick_v2=os.getenv(
            "JIRA_SIDEKICK_V2_AUTOMATION_ID",
            DEFAULT_AUTOMATION_IDS.jira_sidekick_v2,
        ),
        github_qa=os.getenv("GITHUB_QA_AUTOMATION_ID", DEFAULT_AUTOMATION_IDS.github_qa),
    )


def expected_automation_states(mode: str, ids: AutomationIds) -> dict[str, bool]:
    if mode == "main":
        return {
            ids.jira_main: True,
            ids.jira_control: False,
            ids.jira_sidekick: False,
            ids.jira_sidekick_v2: True,
            ids.github_qa: True,
        }
    if mode == "sidekick-experiment":
        return {
            ids.jira_main: False,
            ids.jira_control: True,
            ids.jira_sidekick: True,
            ids.jira_sidekick_v2: False,
            ids.github_qa: True,
        }
    if mode == "sidekick-v2":
        return {
            ids.jira_main: True,
            ids.jira_control: False,
            ids.jira_sidekick: False,
            ids.jira_sidekick_v2: True,
            ids.github_qa: True,
        }
    raise ValueError(f"unsupported mode: {mode}")


def expected_models(ids: AutomationIds) -> dict[str, str]:
    return {
        ids.jira_main: "Bedrock-Claude-Sonnet-4-5-fast",
        ids.jira_control: "Bedrock-Claude-Sonnet-4-5",
        ids.jira_sidekick: "Bedrock-Claude-Sonnet-4-5",
        ids.jira_sidekick_v2: "Bedrock-Claude-Sonnet-4-5-fast",
        ids.github_qa: "Bedrock-Claude-Sonnet-4-5-fast",
    }


def extract_automations(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        return payload
    if not isinstance(payload, dict):
        return []
    for key in ("items", "data", "automations"):
        items = payload.get(key)
        if isinstance(items, list):
            return items
    return []


def validate_automation_states(
    automations: list[dict[str, Any]], mode: str, ids: AutomationIds
) -> list[str]:
    failures: list[str] = []
    by_id = {automation.get("id"): automation for automation in automations}
    for automation_id, enabled in expected_automation_states(mode, ids).items():
        automation = by_id.get(automation_id)
        if not automation:
            failures.append(f"missing automation {automation_id}")
            continue
        if bool(automation.get("enabled")) != enabled:
            state = "enabled" if enabled else "disabled"
            failures.append(f"{automation.get('name') or automation_id} should be {state}")
    for automation_id, model in expected_models(ids).items():
        automation = by_id.get(automation_id)
        if automation and automation.get("model") != model:
            failures.append(
                f"{automation.get('name') or automation_id} model is "
                f"{automation.get('model')!r}, expected {model!r}"
            )
    return failures


def validate_jira_permissions(payload: dict[str, Any]) -> list[str]:
    required = {
        "BROWSE_PROJECTS": "browse Jira project",
        "CREATE_ISSUES": "create Jira demo tickets",
        "ADD_COMMENTS": "post PR/status comments back to Jira",
    }
    permissions = payload.get("permissions", {})
    failures = []
    for key, description in required.items():
        if not permissions.get(key, {}).get("havePermission"):
            failures.append(f"Jira token cannot {description} ({key})")
    return failures


def check_env(failures: list[str]) -> None:
    required_groups = [
        ("OPENHANDS_HOST_GITHUB", "OPENHANDS_HOST_RAJISTICS", "OPENHANDS_HOST"),
        (
            "OPENHANDS_API_KEY_ORG",
            "OPENHANDS_API_KEY_GITHUB",
            "OPENHANDS_API_KEY_RAJISTICS",
            "OPENHANDS_API_KEY",
        ),
        ("JIRA_API_BASE_URL",),
        ("JIRA_API_TOKEN",),
        ("JIRA_SITE_URL",),
        ("JIRA_DEMO_PROJECT_KEY",),
        ("GITHUB_DEMO_REPOSITORY",),
        ("GITHUB_DEMO_REPO_URL",),
    ]
    missing = [" or ".join(group) for group in required_groups if not env_first(*group)]
    if missing:
        fail(failures, f"missing env names: {', '.join(missing)}")
    else:
        ok("required env names are set; values were not printed")


def check_jira(failures: list[str]) -> None:
    base = os.environ["JIRA_API_BASE_URL"].rstrip("/")
    project_key = os.environ["JIRA_DEMO_PROJECT_KEY"]
    headers = {
        "Authorization": f"Bearer {os.environ['JIRA_API_TOKEN']}",
        "Accept": "application/json",
    }
    project = http_json(
        f"{base}/rest/api/3/project/{quote(project_key)}",
        headers,
    )
    if project.get("key") != project_key:
        fail(failures, f"Jira project lookup returned {project.get('key')!r}")
    else:
        ok(f"Jira project {project_key} is reachable")

    query = urlencode(
        {
            "projectKey": project_key,
            "permissions": "BROWSE_PROJECTS,CREATE_ISSUES,ADD_COMMENTS",
        }
    )
    permissions = http_json(f"{base}/rest/api/3/mypermissions?{query}", headers)
    permission_failures = validate_jira_permissions(permissions)
    if permission_failures:
        for message in permission_failures:
            fail(failures, message)
    else:
        ok("Jira token can browse, create issues, and add comments")


def check_github(failures: list[str]) -> None:
    repo = os.environ["GITHUB_DEMO_REPOSITORY"]
    repository = gh_json(f"repos/{repo}")
    if repository.get("full_name") != repo:
        fail(failures, f"GitHub repo lookup returned {repository.get('full_name')!r}")
    else:
        ok(f"GitHub CLI can access {repo}")

    labels = gh_json(f"repos/{repo}/labels?per_page=100")
    names = {label.get("name") for label in labels if isinstance(label, dict)}
    missing = REQUIRED_GITHUB_LABELS - names
    if missing:
        fail(failures, f"missing GitHub labels: {', '.join(sorted(missing))}")
    else:
        ok("required GitHub labels exist")


def check_openhands(failures: list[str], mode: str) -> None:
    host = env_first("OPENHANDS_HOST_GITHUB", "OPENHANDS_HOST_RAJISTICS", "OPENHANDS_HOST").rstrip("/")
    api_key = env_first(
        "OPENHANDS_API_KEY_ORG",
        "OPENHANDS_API_KEY_GITHUB",
        "OPENHANDS_API_KEY_RAJISTICS",
        "OPENHANDS_API_KEY",
    )
    headers = {"Authorization": f"Bearer {api_key}"}
    server_info = http_json(f"{host}/server_info", headers)
    if not isinstance(server_info, dict):
        fail(failures, "OpenHands /server_info did not return JSON")
    else:
        ok("OpenHands app API is reachable")

    automations = extract_automations(
        http_json(f"{host}/api/automation/v1?limit=100", headers)
    )
    automation_failures = validate_automation_states(
        automations,
        mode,
        automation_ids_from_env(),
    )
    if automation_failures:
        for message in automation_failures:
            fail(failures, message)
    else:
        ok(f"OpenHands automation state matches mode={mode}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--env-file", type=Path, help="load KEY=value entries")
    parser.add_argument(
        "--mode",
        choices=("main", "sidekick-experiment", "sidekick-v2"),
        default="main",
        help="expected live automation state",
    )
    parser.add_argument("--skip-github", action="store_true")
    parser.add_argument("--skip-jira", action="store_true")
    parser.add_argument("--skip-openhands", action="store_true")
    args = parser.parse_args()

    if args.env_file:
        load_env_file(args.env_file)
    apply_defaults()

    failures: list[str] = []
    check_env(failures)
    if failures:
        print(f"Live preflight failed with {len(failures)} issue(s).", file=sys.stderr)
        return 1

    for name, check, skip in [
        ("Jira", check_jira, args.skip_jira),
        ("GitHub", check_github, args.skip_github),
        ("OpenHands", lambda collected: check_openhands(collected, args.mode), args.skip_openhands),
    ]:
        if skip:
            ok(f"{name} live check skipped")
            continue
        try:
            check(failures)
        except Exception as exc:  # noqa: BLE001 - preflight should report all failures concisely.
            fail(failures, f"{name} live check failed: {exc}")

    if failures:
        print(f"Live preflight failed with {len(failures)} issue(s).", file=sys.stderr)
        return 1
    print("Live preflight passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
