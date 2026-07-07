#!/usr/bin/env python3
"""Run the delegated Agent Canvas SDLC factory from a supervisor conversation."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import shutil
import time
from pathlib import Path
from typing import Any
from urllib.parse import quote

import agent_canvas_delegate as canvas


REPO_ROOT = Path(__file__).resolve().parents[1]
ACTIVE_WORK_CELLS = ("story-to-pr", "code-review", "qa")
WORK_CELLS = ACTIVE_WORK_CELLS


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def prompt_snapshot_dir(run_dir: Path) -> Path:
    return run_dir / "prompt-snapshot"


def snapshot_prompts(run_dir: Path) -> Path:
    source = REPO_ROOT / "agent-canvas" / "prompts"
    target = prompt_snapshot_dir(run_dir)
    shutil.copytree(source, target, dirs_exist_ok=True)
    return target


def cell_prompt_path(prompt_root: Path, cell: str) -> Path:
    return prompt_root / "workcells" / f"{cell}.md"


def variables_for_cell(args: argparse.Namespace, cell: str) -> dict[str, str]:
    values = {
        "run_id": args.run_id,
        "run_date": args.run_date,
        "repo_path": str(args.repo.resolve()),
        "repo_slug": args.repo_slug,
        "issue_number": str(args.issue_number),
        "request_title": args.request_title,
        "request_body": args.request_body,
        "qa_playwright_requirement": (
            "Playwright UI evidence is REQUIRED for this stress run. QA must run or update a Playwright script that covers the changed UI behavior. Do not use BrowserToolSet-only screenshots as a substitute. If Playwright cannot run, return status: fail or needs-human and explain the missing runtime capability."
            if args.require_playwright_qa
            else "Playwright UI evidence is preferred when available. BrowserToolSet or static UI fallback is acceptable if Playwright is unavailable and the report says so explicitly."
        ),
        "playwright_node_path": args.playwright_node_path or "",
    }
    return values


def create_manifest(args: argparse.Namespace, run_dir: Path, parent_url: str | None) -> None:
    lines = [
        "# SDLC Factory Run Manifest",
        "",
        "## Run Metadata",
        "",
        "| Field | Value |",
        "| --- | --- |",
        f"| Run ID | `{args.run_id}` |",
        f"| Run Date | `{args.run_date}` |",
        f"| Repository | `{args.repo_slug}` |",
        f"| Local Repo Path | `{args.repo.resolve()}` |",
        f"| Parent Conversation | {parent_url or 'unknown'} |",
        "",
        "## Story Request",
        "",
        f"- Issue: `#{args.issue_number}`",
        f"- Title: {args.request_title}",
        f"- Body: {args.request_body}",
        "",
        "## Planned Work Cells",
        "",
        "| Work Cell | Status | Child ID | Artifact |",
        "| --- | --- | --- | --- |",
    ]
    for cell in args.cells:
        lines.append(f"| `{cell}` | pending | - | - |")
    lines.append("")
    (run_dir / "manifest.md").write_text("\n".join(lines), encoding="utf-8")


def update_summary(run_dir: Path, entries: list[dict[str, Any]]) -> None:
    lines = [
        "# Agent Canvas Factory Summary",
        "",
        "| Work Cell | Status | Child Conversation | Artifact |",
        "| --- | --- | --- | --- |",
    ]
    for entry in entries:
        url = entry.get("ui_url") or ""
        link = f"[{entry.get('id')}]({url})" if url and entry.get("id") else entry.get("id", "")
        status = entry.get("wait", {}).get("execution_status") or entry.get("execution_status") or "unknown"
        if status == "idle" and "wait" not in entry:
            status = "created"
        artifact = entry.get("artifact") or ""
        lines.append(f"| `{entry['name']}` | {status} | {link} | `{artifact}` |")
    lines.append("")
    (run_dir / "children-summary.md").write_text("\n".join(lines), encoding="utf-8")


def write_children(run_dir: Path, entries: list[dict[str, Any]]) -> None:
    write_json(run_dir / "children.json", entries)


def write_missing_artifact_report(
    *,
    args: argparse.Namespace,
    cell: str,
    entry: dict[str, Any],
    status_response: dict[str, Any],
    final_response: dict[str, Any],
) -> Path | None:
    artifact = args.repo / entry["artifact"]
    if artifact.exists():
        return None

    status = status_response.get("execution_status") or "unknown"
    timeout = bool(status_response.get("wait_timeout"))
    response = final_response.get("response") or ""
    lines = [
        f"# {cell} Work Cell Report",
        "",
        "Status: needs-human",
        "",
        "This artifact was written by the Agent Canvas factory orchestrator because",
        f"the `{cell}` child did not write its expected report before reaching a",
        "terminal or timeout state.",
        "",
        "## Run Metadata",
        "",
        f"- Run ID: `{args.run_id}`",
        f"- Run date: `{args.run_date}`",
        f"- Child conversation: {entry.get('ui_url') or entry.get('id') or 'unknown'}",
        f"- Execution status: `{status}`",
        f"- Wait timeout: `{str(timeout).lower()}`",
        "",
        "## Child Final Response",
        "",
        response.strip() or "_No final response was available from the child conversation._",
        "",
        "## Required Human Action",
        "",
        "- Open the child conversation and inspect the terminal error or timeout.",
        "- Rerun this workcell after resolving the missing capability or prompt issue.",
        "- Do not treat this gate as passed until the workcell writes its normal report.",
        "",
    ]
    artifact.parent.mkdir(parents=True, exist_ok=True)
    artifact.write_text("\n".join(lines), encoding="utf-8")
    return artifact


def start_cell(
    *,
    args: argparse.Namespace,
    base: str,
    key: str,
    settings_response: dict[str, Any],
    run_dir: Path,
    prompt_root: Path,
    cell: str,
) -> dict[str, Any]:
    prompt = canvas.render_prompt(cell_prompt_path(prompt_root, cell), variables_for_cell(args, cell))
    cell_settings_response = settings_response
    if cell == "code-review" and args.code_review_profile:
        profile = canvas.http_json(
            "GET",
            f"{base}/api/profiles/{quote(args.code_review_profile)}",
            key=key,
            expose_encrypted_secrets=True,
        )
        cell_settings_response = dict(settings_response)
        agent_settings = dict(settings_response.get("agent_settings") or {})
        agent_settings["llm"] = {
            **(profile.get("config") or {}),
            "stream": True,
            "usage_id": f"profile:{args.code_review_profile}:{int(time.time())}",
        }
        cell_settings_response["agent_settings"] = agent_settings

    response = canvas.create_conversation(
        base=base,
        key=key,
        settings_response=cell_settings_response,
        prompt=prompt,
        workspace=args.repo,
        max_iterations=args.child_max_iterations,
        include_task_tools=args.include_task_tools,
        run=True,
    )
    summary = canvas.conversation_summary(base, args.ui_base, response)
    summary["name"] = cell
    summary["artifact"] = f"factory_runs/{args.run_id}/{cell}.md"
    if cell == "code-review" and args.code_review_profile:
        summary["profile"] = args.code_review_profile
    write_json(run_dir / f"{cell}.conversation.json", summary)
    return summary


def wait_for_cell(
    *,
    base: str,
    key: str,
    run_dir: Path,
    cell: str,
    conversation_id: str,
    timeout_seconds: int,
    poll_seconds: int,
) -> tuple[dict[str, Any], dict[str, Any]]:
    deadline = time.monotonic() + timeout_seconds
    status_response: dict[str, Any] = {}
    while True:
        status_response = canvas.http_json("GET", f"{base}/api/conversations/{conversation_id}", key=key)
        status = status_response.get("execution_status")
        if status in canvas.TERMINAL_STATUSES and status not in canvas.RUNNING_STATUSES:
            break
        if time.monotonic() >= deadline:
            status_response["wait_timeout"] = True
            break
        time.sleep(poll_seconds)

    final_response = canvas.http_json(
        "GET",
        f"{base}/api/conversations/{conversation_id}/agent_final_response",
        key=key,
    )
    write_json(run_dir / f"{cell}.wait.json", canvas.conversation_summary(base, canvas.DEFAULT_UI_BASE, status_response))
    write_json(run_dir / f"{cell}.final.json", final_response)
    return status_response, final_response


def run_factory(args: argparse.Namespace) -> int:
    args.repo = args.repo.resolve()
    run_dir = args.repo / "factory_runs" / args.run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    prompt_root = snapshot_prompts(run_dir)
    create_manifest(args, run_dir, args.parent_url)

    key = canvas.read_session_key()
    base = canvas.discover_base(args.base, key)
    settings_response = canvas.http_json(
        "GET",
        f"{base}/api/settings",
        key=key,
        expose_encrypted_secrets=True,
    )

    entries: list[dict[str, Any]] = []
    for cell in args.cells:
        entry = start_cell(
            args=args,
            base=base,
            key=key,
            settings_response=settings_response,
            run_dir=run_dir,
            prompt_root=prompt_root,
            cell=cell,
        )
        entries.append(entry)
        update_summary(run_dir, entries)
        write_children(run_dir, entries)

        if not args.no_wait:
            status_response, final_response = wait_for_cell(
                base=base,
                key=key,
                run_dir=run_dir,
                cell=cell,
                conversation_id=entry["id"],
                timeout_seconds=args.cell_timeout_seconds,
                poll_seconds=args.poll_seconds,
            )
            entry["wait"] = canvas.conversation_summary(base, args.ui_base, status_response)
            entry["final_response_present"] = bool(final_response.get("response"))
            if status_response.get("wait_timeout") or status_response.get("execution_status") in {
                "error",
                "stuck",
                "stopped",
            }:
                write_missing_artifact_report(
                    args=args,
                    cell=cell,
                    entry=entry,
                    status_response=status_response,
                    final_response=final_response,
                )
            update_summary(run_dir, entries)
            write_children(run_dir, entries)
            if status_response.get("execution_status") in {"error", "stuck", "stopped"}:
                break

    write_children(run_dir, entries)
    print(json.dumps({"run_dir": str(run_dir), "children": entries}, indent=2, sort_keys=True))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", default="http://localhost:8000")
    parser.add_argument("--ui-base", default=canvas.DEFAULT_UI_BASE)
    parser.add_argument("--repo", type=Path, default=REPO_ROOT)
    parser.add_argument("--repo-slug", required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--run-date", default=dt.date.today().isoformat())
    parser.add_argument("--parent-url")
    parser.add_argument("--issue-number", type=int, default=88)
    parser.add_argument("--request-title", required=True)
    parser.add_argument("--request-body", required=True)
    parser.add_argument("--cells", nargs="+", choices=WORK_CELLS, default=list(ACTIVE_WORK_CELLS))
    parser.add_argument("--code-review-profile", help="Agent Canvas profile name to use only for the code-review child")
    parser.add_argument("--child-max-iterations", type=int, default=100)
    parser.add_argument("--cell-timeout-seconds", type=int, default=1800)
    parser.add_argument("--poll-seconds", type=int, default=20)
    parser.add_argument("--include-task-tools", action="store_true")
    parser.add_argument("--no-wait", action="store_true")
    parser.add_argument("--require-playwright-qa", action="store_true", help="Require QA to run Playwright UI evidence instead of falling back silently")
    parser.add_argument("--playwright-node-path", help="NODE_PATH pointing at an existing node_modules with Playwright")
    return parser


def main() -> int:
    return run_factory(build_parser().parse_args())


if __name__ == "__main__":
    raise SystemExit(main())
