#!/usr/bin/env python3
"""Launch visible sidekick scout conversations for the Jira-to-PR demo.

This is the SDK-style side-agent orchestration for the demo, implemented with
OpenHands app-conversation APIs. The Jira automation itself only starts Step 0;
this launcher then creates the visible side-agent conversations through
`POST /api/v1/app-conversations` and watches them with the corresponding
conversation/status APIs.

The goal is to make the sidekick architecture visible to a customer:

- docs-scout top-level conversation
- logs-scout top-level conversation
- repo-scout top-level conversation
- optional main Jira-to-PR implementation top-level conversation

The scouts are intentionally normal top-level conversations, not hidden child
conversation records, because they are easier to find and explain in the UI.

It never prints secret values. Live mode requires an OpenHands API key in the
environment or an env file.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed, wait
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen


DEFAULT_HOST = "https://app.replicated.rajistics.com"
DEFAULT_REPOSITORY = "rajshah4/sdlc-automation-github-demo"
DEFAULT_BRANCH = "main"
DEFAULT_LITELLM_MODEL = "litellm_proxy/us.anthropic.claude-sonnet-4-5-20250929-v1:0"
DEFAULT_SCOUT_MODEL = "litellm_proxy/us.anthropic.claude-haiku-4-5-20251001-v1:0"
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


@dataclass(frozen=True)
class StartedScout:
    spec: ScoutSpec
    title: str
    start_task: dict[str, Any]
    ready_task: dict[str, Any]
    ready_started_at: str
    conversation_id: str


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

SCOUT_DEMO_STEPS = {
    "docs-scout": ("2A", "Docs Context Scout"),
    "logs-scout": ("2B", "Logs Context Scout"),
    "repo-scout": ("2C", "Repo Context Scout"),
}


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


def secret_wait_seconds() -> float:
    raw_value = os.getenv("SIDEKICK_SECRET_WAIT_SECONDS", "120")
    try:
        return max(0.0, float(raw_value))
    except ValueError:
        return 120.0


def env_first_wait(*names: str) -> str:
    """Wait briefly for runtime-injected secrets to appear in fresh sandboxes."""
    value = env_first(*names)
    if value:
        return value

    deadline = time.monotonic() + secret_wait_seconds()
    while time.monotonic() < deadline:
        time.sleep(1)
        value = env_first(*names)
        if value:
            return value
    return ""


def host() -> str:
    return (
        env_first("OPENHANDS_HOST_GITHUB", "OPENHANDS_HOST_RAJISTICS", "OPENHANDS_HOST")
        or DEFAULT_HOST
    ).rstrip("/")


def openhands_api_key() -> str:
    value = env_first_wait(
        "OPENHANDS_API_KEY_ORG",
        "OPENHANDS_API_KEY_GITHUB",
        "OPENHANDS_API_KEY_RAJISTICS",
        "OPENHANDS_API_KEY",
    )
    if not value:
        raise SystemExit("OpenHands API key env is required")
    return value


def github_token() -> str:
    value = env_first_wait("GITHUB_TOKEN")
    if not value:
        raise SystemExit("Missing required setting: GITHUB_TOKEN")
    return value


def app_headers() -> dict[str, str]:
    return {
        "X-Access-Token": openhands_api_key(),
        "Accept": "application/json",
    }


def http_json(
    method: str,
    path: str,
    *,
    body: dict[str, Any] | None = None,
    headers: dict[str, str] | None = None,
    timeout: int = 60,
) -> Any:
    request_headers = app_headers()
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


def verify_github_token(repository: str) -> None:
    token = github_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    checks = [
        ("GitHub /user", "https://api.github.com/user"),
        (
            "GitHub repository access",
            f"https://api.github.com/repos/{quote(repository, safe='/')}",
        ),
    ]
    for label, url in checks:
        request = Request(url, headers=headers, method="GET")
        try:
            with urlopen(request, timeout=30) as response:
                response.read()
        except HTTPError as exc:
            exc.read()
            raise SystemExit(
                f"Invalid required setting: GITHUB_TOKEN ({label} HTTP {exc.code})"
            ) from exc


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


def scout_step(scout_name: str) -> tuple[str, str]:
    return SCOUT_DEMO_STEPS[scout_name]


def scout_title(ticket: Ticket, scout: ScoutSpec) -> str:
    step, label = scout_step(scout.name)
    return f"Step {step} - {label} ({ticket.key})"


def main_title(ticket: Ticket) -> str:
    return f"Step 3 - Implement Fix and Open PR ({ticket.key})"


def scout_prompt(scout: ScoutSpec, ticket: Ticket) -> str:
    roots = ", ".join(scout.allowed_roots)
    step, label = scout_step(scout.name)
    return f"""DEMO_STEP {step}: {label}

You are {scout.name}, a visible read-only side agent for a customer demo.

Ticket: {ticket.key}
Title: {ticket.title}
Description: {ticket.body or "No description provided."}

Purpose: {scout.purpose}.
Viewer cue: this conversation should make it obvious that a small side agent is
only gathering one slice of context before the main implementation agent edits code.

Rules:
- Read only. Do not change files or external systems.
- Search only these roots: {roots}
- Use at most four search/read commands total.
- Do not load workflow skills or implementation playbooks.
- Do not wait for other agents.

Return exactly this shape and then stop:

DEMO_STEP {step} COMPLETE: {label}
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


def main_prompt(ticket: Ticket, scout_results: list[ConversationResult]) -> str:
    scout_links = "\n".join(
        f"- {result.name}: {result.conversation_url}" for result in scout_results
    )
    scout_briefs = "\n\n".join(
        f"## {result.name}\n{result.output.strip() or 'No SCOUT_RESULT extracted.'}"
        for result in scout_results
    )
    return f"""DEMO_STEP 3: Implement Fix, Add Tests, Open PR

You are the main Jira-to-PR implementation agent in a sidekick demo.

The read-only side agents are searching context in separate conversations. Some
may already have returned briefs; others may still be running. Do not repeat a
broad docs/logs/project search. Use completed scout results first, follow any
linked scout conversations when useful, then inspect only likely implementation
and test files before editing.
Viewer cue: this conversation should show the handoff from sidekick context to
actual code change, tests, PR creation, and QA handoff.

Ticket: {ticket.key}
Ticket URL: {ticket.url}
Title: {ticket.title}
Description: {ticket.body or "No description provided."}

Visible side-agent conversations:
{scout_links}

Scout results:
{scout_briefs}

Workflow:
Step 3.1 - Load and follow skills/sdlc-story/SKILL.md for the implementation workflow.
Step 3.2 - Create the implementation branch from origin/main before editing. The
           initial checkout is only the launcher/context scaffold; the
           customer-facing PR must diff cleanly against main.
           Before opening the PR, verify `git log --oneline origin/main..HEAD`
           contains only your implementation commits.
Step 3.3 - Fix the bug indicated by the ticket and scout results.
Step 3.4 - Add or update tests that would have caught the bug.
Step 3.5 - Run the relevant tests.
Step 3.6 - Use runtime secret GITHUB_TOKEN for GitHub auth. Do not use GITHUB
           or GH_TOKEN. Open a GitHub pull request for review and include the
           Jira key in the title/body.
           Preserve useful ticket title prefixes such as [UI] in the PR title.
Step 3.7 - Add the openhands-qa label to the pull request so the separate QA agent runs.
Step 3.8 - If essential context is missing, stop and ask for human input instead of guessing.

Final response shape:
DEMO_STEP 3 COMPLETE: PR ready for human review
- PR: link
- Tests: commands and result
- QA handoff: whether openhands-qa was added
- Human review: what remains for the reviewer
"""


def start_payload(
    *,
    title: str,
    message: str,
    run: bool,
    repository: str | None,
    branch: str | None,
    model: str | None,
) -> dict[str, Any]:
    # This payload is the OpenHands app-conversation API contract. It mirrors
    # what a user would start in the UI: title, initial user message, selected
    # GitHub repository/branch, and optional model profile. Keeping scouts as
    # top-level app conversations makes the multi-agent handoff visible instead
    # of burying it inside one parent conversation.
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
    return payload


def start_conversation(payload: dict[str, Any]) -> dict[str, Any]:
    # POST /api/v1/app-conversations returns a start task first; the actual
    # conversation id appears after the start task reaches READY.
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
    # OpenHands provisions a sandbox and repository checkout asynchronously.
    # Poll the start-task endpoint until the conversation is ready to run.
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


def normalized_marker_text(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


def is_scout_result_text(text: str, scout_name: str) -> bool:
    normalized = normalized_marker_text(text)
    normalized_scout = normalized_marker_text(scout_name)
    return (
        f"scout result {normalized_scout}" in normalized
        or ("scout result" in normalized and normalized_scout in normalized)
    )


def extract_scout_result(events: list[dict[str, Any]], scout_name: str) -> str:
    candidates: list[str] = []
    for event in events:
        if event.get("kind") != "MessageEvent" or event.get("source") != "agent":
            continue
        for text in event_strings(event):
            if is_scout_result_text(text, scout_name):
                candidates.append(text)
    return candidates[-1].strip() if candidates else ""


def fetch_scout_result_with_retries(
    conversation_id: str,
    scout_name: str,
    *,
    attempts: int = 5,
    sleep_seconds: int = 2,
) -> str:
    for attempt in range(attempts):
        result = extract_scout_result(fetch_events(conversation_id), scout_name)
        if result:
            return result
        if attempt < attempts - 1:
            time.sleep(sleep_seconds)
    return ""


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
    args: argparse.Namespace,
) -> ConversationResult:
    started = start_one_scout(scout, ticket, args)
    return finish_scout(started, args.scout_timeout_seconds)


def start_one_scout(
    scout: ScoutSpec,
    ticket: Ticket,
    args: argparse.Namespace,
) -> StartedScout:
    start_at = utc_now()
    title = scout_title(ticket, scout)
    payload = start_payload(
        title=title,
        message=scout_prompt(scout, ticket),
        run=True,
        repository=args.repository,
        branch=args.branch,
        model=args.scout_model,
    )
    start_task = start_conversation(payload)
    ready_task, ready_started_at = wait_for_ready(start_task, args.start_timeout_seconds)
    conversation_id = ready_task["app_conversation_id"]
    update_conversation_title(conversation_id, title)
    return StartedScout(
        spec=scout,
        title=title,
        start_task=start_task,
        ready_task=ready_task,
        ready_started_at=ready_started_at or start_at,
        conversation_id=conversation_id,
    )


def finish_scout(started: StartedScout, timeout_seconds: int) -> ConversationResult:
    conversation = wait_for_terminal(started.conversation_id, timeout_seconds)
    update_conversation_title(started.conversation_id, started.title)
    conversation = get_conversation(started.conversation_id)
    finished_at = utc_now()
    output = fetch_scout_result_with_retries(started.conversation_id, started.spec.name)
    return conversation_result(
        started.spec.name,
        started.start_task,
        started.ready_task,
        started.ready_started_at,
        conversation,
        finished_at,
        output=output,
    )


def pending_scout_result(started: StartedScout) -> ConversationResult:
    conversation = get_conversation(started.conversation_id)
    step, label = scout_step(started.spec.name)
    output = f"""SCOUT_RESULT {started.spec.name}
DEMO_STEP {step} PENDING: {label}
FILES_CHECKED:
- pending: scout was still running when the main implementation started
EVIDENCE:
- pending: use the scout conversation link if additional evidence is needed
LIKELY_NEXT_FILES:
- pending
MISSING_INFO:
- scout result pending at main-start barrier
CONFIDENCE:
- pending; main should use completed scout briefs first and inspect likely files
"""
    return conversation_result(
        started.spec.name,
        started.start_task,
        started.ready_task,
        started.ready_started_at,
        conversation,
        None,
        output=output,
    )


def max_elapsed(values: list[float | None]) -> float | None:
    numeric = [value for value in values if value is not None]
    return max(numeric) if numeric else None


def min_elapsed(values: list[float | None]) -> float | None:
    numeric = [value for value in values if value is not None]
    return min(numeric) if numeric else None


def timing_summary(
    *,
    started_at: str,
    finished_at: str,
    scout_results: list[ConversationResult],
    main_result: ConversationResult | None,
    main_start_barrier_seconds: int,
) -> dict[str, Any]:
    scout_finish_values = [result.elapsed_to_finished_seconds for result in scout_results]
    summary: dict[str, Any] = {
        "demo_timing_readme": (
            "Use these numbers to explain whether time was spent in launcher startup, "
            "sidekick context search, implementation, or QA handoff."
        ),
        "conversation_layout": "top-level",
        "index_note": (
            "Step 0 automation output is the index; scout and implementation "
            "conversations are created as normal top-level conversations."
        ),
        "total_launcher_elapsed_seconds": seconds_between(started_at, finished_at),
        "scout_count": len(scout_results),
        "scout_fastest_finished_seconds": min_elapsed(scout_finish_values),
        "scout_slowest_finished_seconds": max_elapsed(scout_finish_values),
        "main_start_barrier_seconds": main_start_barrier_seconds,
        "main_elapsed_seconds": main_result.elapsed_to_finished_seconds if main_result else None,
        "qa_timing_note": (
            "Review starts after the main agent adds openhands-review; review then "
            "adds openhands-qa for the separate QA automation."
        ),
    }
    if summary["total_launcher_elapsed_seconds"] and not main_result:
        summary["bottleneck_note"] = "Launcher ended before main implementation ran."
    elif main_result and main_result.elapsed_to_finished_seconds:
        summary["bottleneck_note"] = (
            "Compare main_elapsed_seconds with scout_slowest_finished_seconds to see "
            "whether implementation or context search dominated the visible run."
        )
    return summary


def dry_run_payloads(ticket: Ticket, args: argparse.Namespace) -> dict[str, Any]:
    scouts = [
        start_payload(
            title=scout_title(ticket, scout),
            message=scout_prompt(scout, ticket),
            run=True,
            repository=args.repository,
            branch=args.branch,
            model=args.scout_model,
        )
        for scout in SCOUTS
    ]
    main = start_payload(
        title=main_title(ticket),
        message=main_prompt(ticket, []),
        run=True,
        repository=args.repository,
        branch=args.branch,
        model=args.main_model,
    )
    return {"conversation_layout": "top-level", "scouts": scouts, "main": main}


def run_live(ticket: Ticket, args: argparse.Namespace) -> dict[str, Any]:
    started_at = utc_now()

    # Start all context scouts together. This is the "sidekick" part: small,
    # read-only agents search docs, logs, and repo files in parallel while the
    # launcher prepares the eventual main implementation handoff.
    with ThreadPoolExecutor(max_workers=len(SCOUTS)) as executor:
        start_futures = [
            executor.submit(start_one_scout, scout, ticket, args)
            for scout in SCOUTS
        ]
        started_scouts = [future.result() for future in as_completed(start_futures)]

    started_scouts.sort(key=lambda scout: scout.spec.name)
    scout_results: list[ConversationResult] = []
    scout_future_by_name: dict[Any, str] = {}
    with ThreadPoolExecutor(max_workers=len(started_scouts)) as executor:
        finish_futures = [
            executor.submit(finish_scout, started, args.scout_timeout_seconds)
            for started in started_scouts
        ]
        scout_future_by_name = {
            future: started.spec.name
            for future, started in zip(finish_futures, started_scouts, strict=True)
        }
        if args.full and args.main_start_barrier_seconds > 0:
            done, pending = wait(
                finish_futures,
                timeout=args.main_start_barrier_seconds,
            )
            scout_results.extend(future.result() for future in done)
            finished_names = {result.name for result in scout_results}
            scout_results.extend(
                pending_scout_result(started)
                for started in started_scouts
                if started.spec.name not in finished_names
            )
        else:
            pending = set()
            scout_results = [future.result() for future in as_completed(finish_futures)]
        scout_results.sort(key=lambda result: result.name)

        main_result = None
        if args.full:
            # The main implementation agent receives links to every scout plus
            # completed briefs when available. If a scout is still running after
            # the barrier, the main agent gets the link and a pending marker
            # instead of blocking the demo indefinitely.
            main_title_value = main_title(ticket)
            main_task = start_conversation(
                start_payload(
                    title=main_title_value,
                    message=main_prompt(ticket, scout_results),
                    run=True,
                    repository=args.repository,
                    branch=args.branch,
                    model=args.main_model,
                )
            )
            main_ready, main_started_at = wait_for_ready(main_task, args.start_timeout_seconds)
            main_id = main_ready["app_conversation_id"]
            update_conversation_title(main_id, main_title_value)
            main_conversation = wait_for_terminal(main_id, args.main_timeout_seconds)
            update_conversation_title(main_id, main_title_value)
            main_conversation = get_conversation(main_id)
            main_result = conversation_result(
                "main-jira-to-pr",
                main_task,
                main_ready,
                main_started_at,
                main_conversation,
                utc_now(),
            )

        if args.full and args.main_start_barrier_seconds > 0:
            completed_results = {
                result.name: result
                for result in scout_results
                if result.finished_at is not None
            }
            for future in as_completed(finish_futures):
                name = scout_future_by_name[future]
                completed_results[name] = future.result()
            scout_results = sorted(completed_results.values(), key=lambda result: result.name)

    finished_at = utc_now()
    return {
        "ticket": asdict(ticket),
        "conversation_layout": "top-level",
        "index_note": (
            "Step 0 automation output is the index; scouts and main implementation "
            "are normal top-level conversations."
        ),
        "started_at": started_at,
        "finished_at": finished_at,
        "elapsed_seconds": seconds_between(started_at, finished_at),
        "timing_summary": timing_summary(
            started_at=started_at,
            finished_at=finished_at,
            scout_results=scout_results,
            main_result=main_result,
            main_start_barrier_seconds=args.main_start_barrier_seconds,
        ),
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
    parser.add_argument(
        "--main-start-barrier-seconds",
        type=int,
        default=90,
        help="when --full is set, start main after this scout-result barrier; use 0 to wait for all scouts",
    )
    parser.add_argument("--main-timeout-seconds", type=int, default=900)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--full", action="store_true", help="launch main Jira-to-PR conversation after scouts")
    args = parser.parse_args()

    if args.env_file:
        load_env_file(args.env_file)
    ticket = ticket_from_args(args)
    if args.dry_run:
        print(json.dumps(dry_run_payloads(ticket, args), indent=2, sort_keys=True))
        return 0
    if args.full:
        verify_github_token(args.repository)
    result = run_live(ticket, args)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:  # noqa: BLE001 - command-line tool should report concise failures.
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
