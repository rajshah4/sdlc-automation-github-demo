#!/usr/bin/env python3
"""Create and monitor delegated Agent Canvas conversations.

This helper is intentionally dependency-free so a supervisor conversation can
run it inside a freshly cloned demo repo.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


DEFAULT_BASE_CANDIDATES = (
    "http://localhost:8000",
    "http://localhost:8001",
    "http://127.0.0.1:18000",
)
DEFAULT_UI_BASE = "http://localhost:8000"
TERMINAL_STATUSES = {"finished", "error", "stuck", "stopped", "idle"}
RUNNING_STATUSES = {"running", "starting"}
DEFAULT_TOOLS = [
    {"name": "terminal", "params": {}},
    {"name": "file_editor", "params": {}},
    {"name": "task_tracker", "params": {}},
    {"name": "browser_tool_set", "params": {}},
    {"name": "canvas_ui", "params": {}},
]
TASK_TOOL = {"name": "task_tool_set", "params": {}}


class CanvasAPIError(RuntimeError):
    """Raised when the local Canvas API cannot satisfy a request."""


def read_session_key() -> str:
    for env_name in ("SESSION_API_KEY", "OH_SESSION_API_KEYS_0", "LOCAL_BACKEND_API_KEY"):
        value = os.getenv(env_name)
        if value:
            return value.strip()

    for key_file in (
        Path.home() / ".openhands" / "agent-canvas" / "api-key.txt",
        Path.home() / ".openhands" / "agent-canvas" / "session-api-key.txt",
    ):
        if key_file.exists():
            value = key_file.read_text(encoding="utf-8").strip()
            if value:
                return value

    raise CanvasAPIError("No Agent Canvas session API key found")


def base_candidates(explicit_base: str | None = None) -> list[str]:
    candidates = []
    for value in (
        explicit_base,
        os.getenv("AGENT_CANVAS_BACKEND"),
        os.getenv("AGENT_CANVAS_BASE"),
        *DEFAULT_BASE_CANDIDATES,
    ):
        if value and value not in candidates:
            candidates.append(value.rstrip("/"))
    return candidates


def http_json(
    method: str,
    url: str,
    *,
    key: str | None = None,
    payload: dict[str, Any] | None = None,
    expose_encrypted_secrets: bool = False,
    timeout: int = 60,
) -> dict[str, Any]:
    headers = {"Accept": "application/json"}
    data = None
    if key:
        headers["X-Session-API-Key"] = key
    if expose_encrypted_secrets:
        headers["X-Expose-Secrets"] = "encrypted"
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"

    request = Request(url, data=data, headers=headers, method=method)
    try:
        with urlopen(request, timeout=timeout) as response:
            body = response.read().decode("utf-8")
    except HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise CanvasAPIError(f"{method} {url} returned HTTP {exc.code}: {body}") from exc
    except URLError as exc:
        raise CanvasAPIError(f"{method} {url} failed: {exc.reason}") from exc

    if not body:
        return {}
    try:
        return json.loads(body)
    except json.JSONDecodeError as exc:
        raise CanvasAPIError(f"{method} {url} returned non-JSON response") from exc


def discover_base(explicit_base: str | None, key: str) -> str:
    errors: list[str] = []
    for candidate in base_candidates(explicit_base):
        try:
            http_json("GET", f"{candidate}/server_info", timeout=10)
            http_json("GET", f"{candidate}/api/settings", key=key, timeout=10)
            return candidate
        except CanvasAPIError as exc:
            errors.append(f"{candidate}: {exc}")
    raise CanvasAPIError("No reachable Agent Canvas API found. Tried: " + "; ".join(errors))


def unique_tools(tools: list[dict[str, Any]]) -> list[dict[str, Any]]:
    merged: dict[str, dict[str, Any]] = {}
    for tool in tools:
        name = tool.get("name")
        if name:
            merged[name] = tool
    return list(merged.values())


def build_agent_settings(settings_response: dict[str, Any], *, include_task_tools: bool) -> dict[str, Any]:
    agent_settings = dict(settings_response.get("agent_settings") or {})
    agent_settings.pop("schema_version", None)
    agent_settings.pop("mcp_config", None)

    tools = list(agent_settings.get("tools") or [])
    tools.extend(DEFAULT_TOOLS)
    if include_task_tools:
        tools.append(TASK_TOOL)
    agent_settings["tools"] = unique_tools(tools)

    agent_context = dict(agent_settings.get("agent_context") or {})
    agent_context.update(
        {
            "load_public_skills": True,
            "load_user_skills": True,
            "load_project_skills": True,
        }
    )
    agent_settings["agent_context"] = agent_context
    return agent_settings


def parse_vars(raw_vars: list[str]) -> dict[str, str]:
    values: dict[str, str] = {}
    for item in raw_vars:
        if "=" not in item:
            raise CanvasAPIError(f"--var must be KEY=VALUE, got {item!r}")
        key, value = item.split("=", 1)
        if not key:
            raise CanvasAPIError("--var keys cannot be empty")
        values[key] = value
    return values


def render_prompt(path: Path, variables: dict[str, str]) -> str:
    text = path.read_text(encoding="utf-8")
    for key, value in variables.items():
        text = text.replace("{{" + key + "}}", value)
    return text


def build_conversation_payload(
    *,
    settings_response: dict[str, Any],
    prompt: str,
    workspace: Path,
    max_iterations: int | None,
    include_task_tools: bool,
    run: bool,
) -> dict[str, Any]:
    conversation_settings = settings_response.get("conversation_settings") or {}
    resolved_max_iterations = max_iterations or conversation_settings.get("max_iterations") or 1000
    return {
        "secrets_encrypted": True,
        "agent_settings": build_agent_settings(settings_response, include_task_tools=include_task_tools),
        "tool_module_qualnames": {"canvas_ui": "canvas_ui_tool"},
        "workspace": {"kind": "LocalWorkspace", "working_dir": str(workspace.resolve())},
        "confirmation_policy": {"kind": "NeverConfirm"},
        "max_iterations": resolved_max_iterations,
        "stuck_detection": True,
        "autotitle": True,
        "worktree": False,
        "initial_message": {
            "role": "user",
            "content": [{"type": "text", "text": prompt}],
            "run": run,
        },
    }


def create_conversation(
    *,
    base: str,
    key: str,
    settings_response: dict[str, Any],
    prompt: str,
    workspace: Path,
    max_iterations: int | None,
    include_task_tools: bool,
    run: bool,
) -> dict[str, Any]:
    payload = build_conversation_payload(
        settings_response=settings_response,
        prompt=prompt,
        workspace=workspace,
        max_iterations=max_iterations,
        include_task_tools=include_task_tools,
        run=run,
    )
    return http_json("POST", f"{base}/api/conversations", key=key, payload=payload)


def conversation_summary(base: str, ui_base: str, response: dict[str, Any]) -> dict[str, Any]:
    conversation_id = response.get("id")
    summary = {
        "id": conversation_id,
        "title": response.get("title"),
        "execution_status": response.get("execution_status"),
        "workspace": response.get("workspace"),
    }
    if conversation_id:
        summary["ui_url"] = f"{ui_base.rstrip('/')}/conversations/{conversation_id}"
        summary["api_url"] = f"{base.rstrip('/')}/api/conversations/{conversation_id}"
    return summary


def load_registry(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))


def append_registry(path: Path, entry: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    registry = load_registry(path)
    registry.append(entry)
    path.write_text(json.dumps(registry, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def command_start(args: argparse.Namespace) -> int:
    key = read_session_key()
    base = discover_base(args.base, key)
    settings_response = http_json(
        "GET",
        f"{base}/api/settings",
        key=key,
        expose_encrypted_secrets=True,
    )
    variables = parse_vars(args.var)
    prompt = render_prompt(args.prompt_file, variables)
    response = create_conversation(
        base=base,
        key=key,
        settings_response=settings_response,
        prompt=prompt,
        workspace=args.workspace,
        max_iterations=args.max_iterations,
        include_task_tools=args.include_task_tools,
        run=not args.no_run,
    )
    summary = conversation_summary(base, args.ui_base, response)
    if args.name:
        summary["name"] = args.name
    if args.registry:
        append_registry(args.registry, summary)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


def command_status(args: argparse.Namespace) -> int:
    key = read_session_key()
    base = discover_base(args.base, key)
    response = http_json("GET", f"{base}/api/conversations/{args.conversation_id}", key=key)
    print(json.dumps(conversation_summary(base, args.ui_base, response), indent=2, sort_keys=True))
    return 0


def command_final(args: argparse.Namespace) -> int:
    key = read_session_key()
    base = discover_base(args.base, key)
    response = http_json("GET", f"{base}/api/conversations/{args.conversation_id}/agent_final_response", key=key)
    print(json.dumps(response, indent=2, sort_keys=True))
    return 0


def command_events(args: argparse.Namespace) -> int:
    key = read_session_key()
    base = discover_base(args.base, key)
    path = f"{base}/api/conversations/{args.conversation_id}/events/search?limit={args.limit}&sort_order=TIMESTAMP_DESC"
    response = http_json("GET", path, key=key)
    print(json.dumps(response, indent=2, sort_keys=True))
    return 0


def command_wait(args: argparse.Namespace) -> int:
    key = read_session_key()
    base = discover_base(args.base, key)
    deadline = time.monotonic() + args.timeout_seconds
    last_status = None
    while True:
        response = http_json("GET", f"{base}/api/conversations/{args.conversation_id}", key=key)
        last_status = response.get("execution_status")
        if last_status in TERMINAL_STATUSES and last_status not in RUNNING_STATUSES:
            print(json.dumps(conversation_summary(base, args.ui_base, response), indent=2, sort_keys=True))
            return 0 if last_status in {"finished", "idle"} else 1
        if time.monotonic() >= deadline:
            print(json.dumps(conversation_summary(base, args.ui_base, response), indent=2, sort_keys=True))
            print(f"Timed out waiting for {args.conversation_id}; last status: {last_status}", file=sys.stderr)
            return 2
        time.sleep(args.poll_seconds)


def command_render(args: argparse.Namespace) -> int:
    print(render_prompt(args.prompt_file, parse_vars(args.var)))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", help="Agent Canvas API base URL")
    parser.add_argument("--ui-base", default=DEFAULT_UI_BASE, help="Agent Canvas UI base URL")
    subparsers = parser.add_subparsers(dest="command", required=True)

    start = subparsers.add_parser("start", help="start a delegated conversation")
    start.add_argument("--name", help="human-readable work-cell name")
    start.add_argument("--prompt-file", type=Path, required=True)
    start.add_argument("--workspace", type=Path, default=Path.cwd())
    start.add_argument("--registry", type=Path, help="append conversation summary to this JSON registry")
    start.add_argument("--max-iterations", type=int)
    start.add_argument("--include-task-tools", action="store_true")
    start.add_argument("--no-run", action="store_true", help="create the conversation without starting the agent loop")
    start.add_argument("--var", action="append", default=[], help="template substitution in KEY=VALUE form")
    start.set_defaults(func=command_start)

    for name, func in (("status", command_status), ("final", command_final), ("events", command_events), ("wait", command_wait)):
        sub = subparsers.add_parser(name)
        sub.add_argument("conversation_id")
        sub.set_defaults(func=func)
        if name == "events":
            sub.add_argument("--limit", type=int, default=20)
        if name == "wait":
            sub.add_argument("--timeout-seconds", type=int, default=3600)
            sub.add_argument("--poll-seconds", type=int, default=30)

    render = subparsers.add_parser("render", help="render a prompt template locally")
    render.add_argument("--prompt-file", type=Path, required=True)
    render.add_argument("--var", action="append", default=[])
    render.set_defaults(func=command_render)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except CanvasAPIError as exc:
        print(f"agent_canvas_delegate: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
