#!/usr/bin/env python3
"""Launch visible sidekick scout conversations for the Jira-to-PR demo.

This script is intentionally API-first so the demo shows separate conversations:

- a lightweight parent orchestrator conversation
- docs-scout child conversation
- logs-scout child conversation
- repo-scout child conversation
- optional main Jira-to-PR implementation child conversation

It never prints secret values. Live mode requires an OpenHands API key in the
environment or an env file.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen


DEFAULT_HOST = "https://app.replicated.rajistics.com"
DEFAULT_REPOSITORY = "rajshah4/sdlc-automation-github-demo"
DEFAULT_BRANCH = "sidekick-context-experiment"
DEFAULT_LITELLM_MODEL = "litellm_proxy/us.anthropic.claude-sonnet-4-5-20250929-v1:0"
DEFAULT_SCOUT_MODEL = DEFAULT_LITELLM_MODEL
DEFAULT_MAIN_MODEL = DEFAULT_LITELLM_MODEL
TERMINAL_EXECUTION_STATUSES = {"idle", "finished", "error", "stuck", "paused"}
TERMINAL_START_STATUSES = {"READY", "ERROR"}


@dataclass(frozen=True)
class Ticket:
    key: str
    url: str
    title: str
    body: str


@dataclass(frozen=True)
class ScoutSpec:
    name: str
    allowed_roots: tuple[str, ...]
    purpose: str


@dataclass
class ConversationResult:
    name: str
    conversation_id: str
    conversation_url: str
    start_task_id: str
    start_status: str
    execution_status: str | None
    started_at: str | None
    ready_at: str | None
    finished_at: str | None
    elapsed_to_ready_seconds: float | None
    elapsed_to_finished_seconds: float | None
    output: str = ""


SCOUTS = (
    ScoutSpec(
        name="docs-scout",
        allowed_roots=("README.md", "AGENTS.md", "docs/wiki/", "openspec/project.md"),
        purpose="find product wording, architecture hints, and acceptance clues",
    ),
    ScoutSpec(
        name="logs-scout",
        allowed_roots=("docs/logs/",),
        purpose="find symptom evidence, request traces, and error markers",
    ),
    ScoutSpec(
        name="repo-scout",
        allowed_roots=("app/", "tests/"),
        purpose="find likely implementation and test files",
    ),
)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def parse_time(value: str | None) -> datetime | None:
    if not value:
        return None
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)


def seconds_between(start: str | None, end: str | None) -> float | None:
    start_at = parse_time(start)
    end_at = parse_time(end)
    if not start_at or not end_at:
        return None
    return round((end_at - start_at).total_seconds(), 2)


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


def host() -> str:
    return (
        env_first("OPENHANDS_HOST_GITHUB", "OPENHANDS_HOST_RAJISTICS", "OPENHANDS_HOST")
        or DEFAULT_HOST
    ).rstrip("/")


def openhands_api_key() -> str:
    value = env_first(
        "OPENHANDS_API_KEY_ORG",
        "OPENHANDS_API_KEY_GITHUB",
        "OPENHANDS_API_KEY_RAJISTICS",
        "OPENHANDS_API_KEY",
    )
    if not value:
        raise SystemExit("OpenHands API key env is required")
    return value


def http_json(
    method: str,
    path: str,
    *,
    body: dict[str, Any] | None = None,
    headers: dict[str, str] | None = None,
    timeout: int = 60,
) -> Any:
    request_headers = {
        "Authorization": f"Bearer {openhands_api_key()}",
        "Accept": "application/json",
    }
    if body is not None:
        request_headers["Content-Type"] = "application/json"
    if headers:
        request_headers.update(headers)
    request = Request(
        host() + path,
        data=json.dumps(body).encode("utf-8") if body is not None else None,
        headers=request_headers,
        method=method,
    )
    for attempt in range(5):
        try:
            with urlopen(request, timeout=timeout) as response:
                return json.loads(response.read().decode("utf-8"))
        except HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            if exc.code in {401, 429} and attempt < 4 and "BearerTokenError" in detail:
                time.sleep(1 + attempt)
                continue
            if exc.code == 429 and attempt < 4:
                time.sleep(1 + attempt)
                continue
            raise RuntimeError(f"{method} {path} returned HTTP {exc.code}: {detail[:500]}") from exc
    raise RuntimeError(f"{method} {path} failed after retries")


def jira_headers() -> dict[str, str]:
    token = os.getenv("JIRA_API_TOKEN", "")
    if not token:
        raise SystemExit("JIRA_API_TOKEN env is required to fetch Jira tickets")
    return {"Authorization": f"Bearer {token}", "Accept": "application/json"}


def adf_text(node: Any) -> str:
    if isinstance(node, dict):
        if node.get("type") == "text":
            return str(node.get("text", ""))
        return "".join(adf_text(value) for value in node.values())
    if isinstance(node, list):
        return "".join(adf_text(value) for value in node)
    return ""


def fetch_jira_ticket(key: str) -> Ticket:
    base = os.getenv("JIRA_API_BASE_URL", "").rstrip("/")
    site = (os.getenv("JIRA_SITE_URL") or base).rstrip("/")
    if not base:
        raise SystemExit("JIRA_API_BASE_URL env is required to fetch Jira tickets")
    request = Request(
        f"{base}/rest/api/3/issue/{quote(key)}?fields=summary,description,labels",
        headers=jira_headers(),
        method="GET",
    )
    try:
        with urlopen(request, timeout=60) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Jira issue fetch returned HTTP {exc.code}: {detail[:500]}") from exc
    fields = payload.get("fields", {})
    description = fields.get("description")
    body = adf_text(description) if isinstance(description, dict) else str(description or "")
    return Ticket(
        key=payload.get("key", key),
        url=f"{site}/browse/{payload.get('key', key)}",
        title=str(fields.get("summary") or key),
        body=body.strip(),
    )


def text_message(text: str, *, run: bool = True) -> dict[str, Any]:
    return {
        "role": "user",
        "content": [{"type": "text", "text": text}],
        "run": run,
    }


def scout_prompt(scout: ScoutSpec, ticket: Ticket) -> str:
    roots = ", ".join(scout.allowed_roots)
    return f"""You are {scout.name}, a visible read-only side agent for a customer demo.

Ticket: {ticket.key}
Title: {ticket.title}
Description: {ticket.body or "No description provided."}

Purpose: {scout.purpose}.

Rules:
- Read only. Do not change files or external systems.
- Search only these roots: {roots}
- Use at most four search/read commands total.
- Do not load workflow skills or implementation playbooks.
- Do not wait for other agents.

Return exactly this shape and then stop:

SCOUT_RESULT {scout.name}
FILES_CHECKED:
- path: one short reason
EVIDENCE:
- path: one short quoted or paraphrased clue
LIKELY_NEXT_FILES:
- path
MISSING_INFO:
- none, or the smallest human question needed
CONFIDENCE:
- high, medium, low, or NEEDS_HUMAN plus one short rationale
"""


def parent_prompt(ticket: Ticket) -> str:
    return f"""Sidekick V2 orchestration parent for {ticket.key}.

This parent groups the visible context scout child conversations for the demo.
The parent itself should not perform implementation work.

Ticket: {ticket.url}
Title: {ticket.title}
"""


def main_prompt(ticket: Ticket, scout_results: list[ConversationResult]) -> str:
    scout_links = "\n".join(
        f"- {result.name}: {result.conversation_url}" for result in scout_results
    )
    scout_briefs = "\n\n".join(
        f"## {result.name}\n{result.output.strip() or 'No SCOUT_RESULT extracted.'}"
        for result in scout_results
    )
    return f"""You are the main Jira-to-PR implementation agent in a sidekick demo.

The read-only side agents have already searched context. Do not repeat a broad
docs/logs/project search. Use the scout results first, then inspect only likely
implementation and test files before editing.

Ticket: {ticket.key}
Ticket URL: {ticket.url}
Title: {ticket.title}
Description: {ticket.body or "No description provided."}

Visible side-agent conversations:
{scout_links}

Scout results:
{scout_briefs}

Workflow:
1. Load and follow skills/sdlc-story/SKILL.md for the implementation workflow.
2. Fix the bug indicated by the ticket and scout results.
3. Add or update tests that would have caught the bug.
4. Run the relevant tests.
5. Open a GitHub pull request for review and include the Jira key in the title/body.
6. Add the openhands-qa label to the pull request so the separate QA agent runs.
7. If essential context is missing, stop and ask for human input instead of guessing.
"""


def start_payload(
    *,
    title: str,
    message: str,
    run: bool,
    repository: str | None,
    branch: str | None,
    model: str | None,
    parent_id: str | None = None,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "title": title,
        "initial_message": text_message(message, run=run),
        "agent_type": "default",
        "public": False,
        "plugins": [],
        "system_message_suffix": (
            "For this demo, keep the conversation scoped and concise. "
            "Never reveal secrets or environment values."
        ),
    }
    if repository:
        payload["selected_repository"] = repository
        payload["git_provider"] = "github"
    if branch:
        payload["selected_branch"] = branch
    if model:
        payload["llm_model"] = model
    if parent_id:
        payload["parent_conversation_id"] = parent_id
    return payload


def start_conversation(payload: dict[str, Any]) -> dict[str, Any]:
    return http_json("POST", "/api/v1/app-conversations", body=payload)


def get_start_task(task_id: str) -> dict[str, Any]:
    query = urlencode({"ids": task_id})
    payload = http_json("GET", f"/api/v1/app-conversations/start-tasks?{query}")
    if not payload or not payload[0]:
        raise RuntimeError(f"start task {task_id} was not found")
    return payload[0]


def get_conversation(conversation_id: str) -> dict[str, Any]:
    query = urlencode({"ids": conversation_id})
    payload = http_json("GET", f"/api/v1/app-conversations?{query}")
    if not payload or not payload[0]:
        raise RuntimeError(f"conversation {conversation_id} was not found")
    return payload[0]


def update_conversation_title(conversation_id: str, title: str) -> None:
    http_json("PATCH", f"/api/v1/app-conversations/{conversation_id}", body={"title": title})


def wait_for_ready(task: dict[str, Any], timeout_seconds: int) -> tuple[dict[str, Any], str]:
    task_id = task["id"]
    started_at = utc_now()
    deadline = time.monotonic() + timeout_seconds
    latest = task
    while time.monotonic() < deadline:
        latest = get_start_task(task_id)
        status = latest.get("status")
        if status in TERMINAL_START_STATUSES:
            if status == "ERROR":
                raise RuntimeError(f"conversation start task failed: {latest.get('detail')}")
            return latest, started_at
        time.sleep(2)
    raise TimeoutError(f"conversation start task {task_id} did not become READY")


def wait_for_terminal(conversation_id: str, timeout_seconds: int) -> dict[str, Any]:
    deadline = time.monotonic() + timeout_seconds
    latest = get_conversation(conversation_id)
    while time.monotonic() < deadline:
        latest = get_conversation(conversation_id)
        status = latest.get("execution_status")
        if status in TERMINAL_EXECUTION_STATUSES:
            return latest
        time.sleep(5)
    return latest


def event_strings(node: Any) -> list[str]:
    if isinstance(node, dict):
        values: list[str] = []
        for key, value in node.items():
            if key in {"text", "message", "content"}:
                values.extend(event_strings(value))
            elif isinstance(value, (dict, list)):
                values.extend(event_strings(value))
        return values
    if isinstance(node, list):
        values: list[str] = []
        for item in node:
            values.extend(event_strings(item))
        return values
    if isinstance(node, str):
        return [node]
    return []


def fetch_events(conversation_id: str, limit: int = 100) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    page_id = ""
    while True:
        params = {"limit": min(limit, 100), "sort_order": "TIMESTAMP"}
        if page_id:
            params["page_id"] = page_id
        payload = http_json(
            "GET",
            f"/api/v1/conversation/{conversation_id}/events/search?{urlencode(params)}",
        )
        batch = payload.get("items") or payload.get("events") or []
        events.extend(batch)
        page_id = payload.get("next_page_id") or ""
        if not page_id or len(batch) < min(limit, 100):
            break
    return events


def extract_scout_result(events: list[dict[str, Any]], scout_name: str) -> str:
    marker = f"SCOUT_RESULT {scout_name}"
    candidates: list[str] = []
    for event in events:
        if event.get("kind") != "MessageEvent" or event.get("source") != "agent":
            continue
        for text in event_strings(event):
            if marker in text:
                candidates.append(text)
    return candidates[-1].strip() if candidates else ""


def conversation_result(
    name: str,
    start_task: dict[str, Any],
    ready_task: dict[str, Any],
    ready_started_at: str,
    conversation: dict[str, Any],
    finished_at: str | None,
    output: str = "",
) -> ConversationResult:
    conversation_id = ready_task.get("app_conversation_id") or conversation.get("id")
    return ConversationResult(
        name=name,
        conversation_id=conversation_id,
        conversation_url=f"{host()}/conversations/{conversation_id}",
        start_task_id=start_task["id"],
        start_status=ready_task.get("status", ""),
        execution_status=conversation.get("execution_status"),
        started_at=ready_started_at,
        ready_at=ready_task.get("updated_at"),
        finished_at=finished_at,
        elapsed_to_ready_seconds=seconds_between(ready_started_at, ready_task.get("updated_at")),
        elapsed_to_finished_seconds=seconds_between(ready_started_at, finished_at),
        output=output,
    )


def launch_one_scout(
    scout: ScoutSpec,
    ticket: Ticket,
    parent_id: str,
    args: argparse.Namespace,
) -> ConversationResult:
    start_at = utc_now()
    title = f"Sidekick V2 {ticket.key} {scout.name}"
    payload = start_payload(
        title=title,
        message=scout_prompt(scout, ticket),
        run=True,
        repository=args.repository,
        branch=args.branch,
        model=args.scout_model,
        parent_id=parent_id,
    )
    start_task = start_conversation(payload)
    ready_task, ready_started_at = wait_for_ready(start_task, args.start_timeout_seconds)
    conversation_id = ready_task["app_conversation_id"]
    update_conversation_title(conversation_id, title)
    conversation = wait_for_terminal(conversation_id, args.scout_timeout_seconds)
    update_conversation_title(conversation_id, title)
    conversation = get_conversation(conversation_id)
    finished_at = utc_now()
    return conversation_result(
        scout.name,
        start_task,
        ready_task,
        ready_started_at or start_at,
        conversation,
        finished_at,
        output="",
    )


def dry_run_payloads(ticket: Ticket, args: argparse.Namespace) -> dict[str, Any]:
    parent = start_payload(
        title=f"Sidekick V2 {ticket.key} orchestrator",
        message=parent_prompt(ticket),
        run=False,
        repository=None,
        branch=None,
        model=None,
    )
    scouts = [
        start_payload(
            title=f"Sidekick V2 {ticket.key} {scout.name}",
            message=scout_prompt(scout, ticket),
            run=True,
            repository=args.repository,
            branch=args.branch,
            model=args.scout_model,
            parent_id="<parent-conversation-id>",
        )
        for scout in SCOUTS
    ]
    main = start_payload(
        title=f"Sidekick V2 {ticket.key} main Jira-to-PR",
        message=main_prompt(ticket, []),
        run=True,
        repository=args.repository,
        branch=args.branch,
        model=args.main_model,
        parent_id="<parent-conversation-id>",
    )
    return {"parent": parent, "scouts": scouts, "main": main}


def run_live(ticket: Ticket, args: argparse.Namespace) -> dict[str, Any]:
    started_at = utc_now()
    parent_title = f"Sidekick V2 {ticket.key} orchestrator"
    parent_task = start_conversation(
        start_payload(
            title=parent_title,
            message=parent_prompt(ticket),
            run=False,
            repository=None,
            branch=None,
            model=None,
        )
    )
    parent_ready, parent_started_at = wait_for_ready(parent_task, args.start_timeout_seconds)
    parent_id = parent_ready["app_conversation_id"]
    update_conversation_title(parent_id, parent_title)
    parent_conversation = get_conversation(parent_id)
    update_conversation_title(parent_id, parent_title)
    parent_conversation = get_conversation(parent_id)
    parent = conversation_result(
        "orchestrator",
        parent_task,
        parent_ready,
        parent_started_at,
        parent_conversation,
        parent_ready.get("updated_at"),
    )

    with ThreadPoolExecutor(max_workers=len(SCOUTS)) as executor:
        futures = [
            executor.submit(launch_one_scout, scout, ticket, parent_id, args)
            for scout in SCOUTS
        ]
        scout_results = [future.result() for future in as_completed(futures)]
    scout_results.sort(key=lambda result: result.name)
    for result in scout_results:
        result.output = extract_scout_result(fetch_events(result.conversation_id), result.name)
        time.sleep(1)

    main_result = None
    if args.full:
        main_title = f"Sidekick V2 {ticket.key} main Jira-to-PR"
        main_task = start_conversation(
            start_payload(
                title=main_title,
                message=main_prompt(ticket, scout_results),
                run=True,
                repository=args.repository,
                branch=args.branch,
                model=args.main_model,
                parent_id=parent_id,
            )
        )
        main_ready, main_started_at = wait_for_ready(main_task, args.start_timeout_seconds)
        main_id = main_ready["app_conversation_id"]
        update_conversation_title(main_id, main_title)
        main_conversation = wait_for_terminal(main_id, args.main_timeout_seconds)
        update_conversation_title(main_id, main_title)
        main_conversation = get_conversation(main_id)
        main_result = conversation_result(
            "main-jira-to-pr",
            main_task,
            main_ready,
            main_started_at,
            main_conversation,
            utc_now(),
        )

    finished_at = utc_now()
    return {
        "ticket": asdict(ticket),
        "started_at": started_at,
        "finished_at": finished_at,
        "elapsed_seconds": seconds_between(started_at, finished_at),
        "parent": asdict(parent),
        "scouts": [asdict(result) for result in scout_results],
        "main": asdict(main_result) if main_result else None,
    }


def ticket_from_args(args: argparse.Namespace) -> Ticket:
    if args.fetch_jira:
        if not args.jira_key:
            raise SystemExit("--jira-key is required with --fetch-jira")
        return fetch_jira_ticket(args.jira_key)
    key = args.jira_key or "KAN-DRY-RUN"
    site = (os.getenv("JIRA_SITE_URL") or "https://rajiv-shah.atlassian.net").rstrip("/")
    return Ticket(
        key=key,
        url=f"{site}/browse/{key}",
        title=args.title or "Available pets list still shows unavailable animals",
        body=args.body
        or "Customers say the available pets page includes animals that should not be adoptable.",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--env-file", type=Path)
    parser.add_argument("--jira-key")
    parser.add_argument("--fetch-jira", action="store_true")
    parser.add_argument("--title")
    parser.add_argument("--body", default="")
    parser.add_argument("--repository", default=os.getenv("GITHUB_DEMO_REPOSITORY", DEFAULT_REPOSITORY))
    parser.add_argument("--branch", default=DEFAULT_BRANCH)
    parser.add_argument("--scout-model", default=os.getenv("OPENHANDS_SCOUT_LLM_MODEL", DEFAULT_SCOUT_MODEL))
    parser.add_argument("--main-model", default=os.getenv("OPENHANDS_MAIN_LLM_MODEL", DEFAULT_MAIN_MODEL))
    parser.add_argument("--start-timeout-seconds", type=int, default=240)
    parser.add_argument("--scout-timeout-seconds", type=int, default=180)
    parser.add_argument("--main-timeout-seconds", type=int, default=900)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--full", action="store_true", help="launch main Jira-to-PR child after scouts")
    args = parser.parse_args()

    if args.env_file:
        load_env_file(args.env_file)
    ticket = ticket_from_args(args)
    if args.dry_run:
        print(json.dumps(dry_run_payloads(ticket, args), indent=2, sort_keys=True))
        return 0
    result = run_live(ticket, args)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:  # noqa: BLE001 - command-line tool should report concise failures.
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
