#!/usr/bin/env python3
"""Run the Jira-triggered delegated SDLC flow on Rajistics Replicated."""

from __future__ import annotations

import argparse
import json
import os
import time
import urllib.request
from pathlib import Path
from typing import Any

import openhands_v1_delegate as oh


REPO_ROOT = Path(__file__).resolve().parents[1]
PROMPT_ROOT = REPO_ROOT / "automations" / "replicated-jira-delegated-factory" / "workcells"
ACTIVE_WORK_CELLS = ("story-to-pr", "code-review", "qa")
SUCCESS_STATUSES = {
    "story-to-pr": {"done"},
    "code-review": {"pass", "findings"},
    "qa": {"pass"},
}


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def adf_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    chunks: list[str] = []
    if isinstance(value, dict):
        if value.get("type") == "text" and value.get("text"):
            chunks.append(str(value["text"]))
        for child in value.get("content", []) or []:
            child_text = adf_text(child)
            if child_text:
                chunks.append(child_text)
    elif isinstance(value, list):
        for child in value:
            child_text = adf_text(child)
            if child_text:
                chunks.append(child_text)
    return "\n".join(chunks)


def jira_headers() -> dict[str, str]:
    token = os.getenv("JIRA_API_TOKEN")
    if not token:
        raise RuntimeError("JIRA_API_TOKEN is required to fetch or comment on Jira issues")
    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }


def jira_base_url() -> str:
    base = os.getenv("JIRA_API_BASE_URL")
    if not base:
        raise RuntimeError("JIRA_API_BASE_URL is required to fetch or comment on Jira issues")
    return base.rstrip("/")


def jira_request(method: str, path: str, payload: dict[str, Any] | None = None) -> Any:
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        jira_base_url() + path,
        data=data,
        method=method,
        headers=jira_headers(),
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        raw = response.read()
        if not raw:
            return None
        return json.loads(raw)


def fetch_jira_issue(issue_key: str) -> dict[str, str]:
    issue = jira_request(
        "GET",
        f"/rest/api/3/issue/{issue_key}?fields=summary,description,issuetype,project",
    )
    fields = issue.get("fields", {}) if isinstance(issue, dict) else {}
    summary = fields.get("summary") or issue_key
    description = adf_text(fields.get("description")).strip()
    site = os.getenv("JIRA_SITE_URL", "").rstrip("/")
    return {
        "issue_key": issue_key,
        "request_title": summary,
        "request_body": description or summary,
        "issue_url": f"{site}/browse/{issue_key}" if site else "",
    }


def jira_comment_body(text: str) -> dict[str, Any]:
    lines = text.splitlines() or [text]
    content = []
    for line in lines:
        content.append(
            {
                "type": "paragraph",
                "content": [{"type": "text", "text": line or " "}],
            }
        )
    return {"body": {"type": "doc", "version": 1, "content": content}}


def post_jira_comment(issue_key: str, text: str) -> None:
    jira_request("POST", f"/rest/api/3/issue/{issue_key}/comment", jira_comment_body(text))


def parse_status(final_text: str, fallback: str) -> str:
    for line in final_text.splitlines():
        if line.lower().startswith("status:"):
            return line.split(":", 1)[1].strip().split()[0].lower()
    return fallback


def parse_contract_field(final_text: str, field: str) -> str:
    prefix = field.lower() + ":"
    for line in final_text.splitlines():
        if line.lower().startswith(prefix):
            return line.split(":", 1)[1].strip().split()[0].lower()
    return ""


def cell_status(cell: str, final_text: str, _execution_status: str) -> str:
    contract_status = parse_status(final_text, "")
    if contract_status in SUCCESS_STATUSES[cell] or contract_status in {"needs-human", "failed"}:
        return contract_status
    return "needs-human"


def gate_allows_next_cell(cell: str, status: str, final_text: str = "") -> bool:
    if status not in SUCCESS_STATUSES[cell]:
        return False
    if cell == "code-review":
        blocking = parse_contract_field(final_text, "blocking")
        next_gate = parse_contract_field(final_text, "next_gate")
        if blocking == "yes" or next_gate == "stop":
            return False
        if status == "findings" and blocking != "no":
            return False
    return True


def variables_for_cell(args: argparse.Namespace, cell: str, prior_summary: str) -> dict[str, str]:
    return {
        "run_id": args.run_id,
        "repo_slug": args.repo_slug,
        "issue_key": args.issue_key,
        "issue_url": args.issue_url or "",
        "request_title": args.request_title,
        "request_body": args.request_body,
        "prior_summary": prior_summary,
        "parent_artifact_dir": f"factory_runs/{args.run_id}",
        "artifact_path": f"factory_runs/{args.run_id}/{cell}.md",
        "parent_final_artifact": f"factory_runs/{args.run_id}/{cell}.final.md",
    }


def start_and_wait_cell(
    *,
    args: argparse.Namespace,
    base: str,
    headers: dict[str, str],
    run_dir: Path,
    cell: str,
    prior_summary: str,
) -> dict[str, Any]:
    print(f"Starting delegated work cell: {cell}", flush=True)
    prompt = oh.render_prompt(PROMPT_ROOT / f"{cell}.md", variables_for_cell(args, cell, prior_summary))
    start = oh.start_app_conversation(
        base=base,
        headers=headers,
        prompt=prompt,
        title=f"{args.issue_key} delegated {cell}",
        repository=args.repo_slug,
        branch=args.branch,
        llm_model=args.child_llm_model,
        run=True,
    )
    start_task_id = start.get("id")
    entry: dict[str, Any] = {"name": cell, "start_task_id": start_task_id, "start_task": start}
    if not start_task_id:
        entry["status"] = "failed"
        entry["error"] = "OpenHands did not return a start task id"
        return entry

    start_task = oh.poll_start_task(
        base=base,
        headers=headers,
        task_id=start_task_id,
        timeout_seconds=args.start_timeout_seconds,
        poll_seconds=args.poll_seconds,
    )
    conversation_id = start_task.get("app_conversation_id")
    entry["start_task"] = start_task
    if not conversation_id:
        entry["status"] = "failed"
        entry["error"] = "OpenHands start task did not return an app conversation id"
        return entry

    entry.update(oh.conversation_summary(base, conversation_id))
    write_json(run_dir / f"{cell}.conversation.json", entry)

    try:
        terminal = oh.poll_conversation(
            base=base,
            headers=headers,
            conversation_id=conversation_id,
            timeout_seconds=args.cell_timeout_seconds,
            poll_seconds=args.poll_seconds,
        )
    except TimeoutError:
        entry["status"] = "needs-human"
        entry["final_text"] = ""
        entry["error"] = "Child conversation exceeded its bounded wait time."
        write_json(run_dir / f"{cell}.wait.json", entry)
        write_text(run_dir / f"{cell}.final.md", "")
        print(f"Delegated work cell timed out: {cell}", flush=True)
        return entry
    final_text = oh.wait_for_agent_text(
        base=base,
        headers=headers,
        conversation_id=conversation_id,
    )
    execution_status = str(terminal.get("execution_status", "unknown")).lower()
    status = cell_status(cell, final_text, execution_status)

    entry["wait"] = oh.conversation_summary(base, conversation_id, terminal)
    entry["status"] = status
    entry["final_text"] = final_text
    if not final_text:
        entry["error"] = (
            "Child conversation ended without the required final response; "
            "inspect the child link before continuing."
        )
    write_json(run_dir / f"{cell}.wait.json", entry["wait"])
    write_text(run_dir / f"{cell}.final.md", final_text + ("\n" if final_text else ""))
    print(f"Completed delegated work cell: {cell} status={status}", flush=True)
    return entry


def create_manifest(args: argparse.Namespace, run_dir: Path) -> None:
    lines = [
        "# Rajistics Delegated SDLC Run",
        "",
        f"- Run id: `{args.run_id}`",
        f"- Jira issue: `{args.issue_key}`",
        f"- Jira URL: {args.issue_url or 'unknown'}",
        f"- Repository: `{args.repo_slug}`",
        f"- Request: {args.request_title}",
        "",
        "## Work Cells",
        "",
        "| Work cell | Status | Conversation |",
        "| --- | --- | --- |",
    ]
    for cell in args.cells:
        lines.append(f"| `{cell}` | pending | - |")
    lines.append("")
    write_text(run_dir / "manifest.md", "\n".join(lines))


def lifecycle_report(args: argparse.Namespace, entries: list[dict[str, Any]]) -> str:
    lines = [
        "# Rajistics Delegated SDLC Lifecycle Report",
        "",
        f"- Jira issue: `{args.issue_key}`",
        f"- Jira URL: {args.issue_url or 'unknown'}",
        f"- Repository: `{args.repo_slug}`",
        f"- Request: {args.request_title}",
        "",
        "## Child Conversations",
        "",
        "| Work cell | Status | Conversation | Artifact |",
        "| --- | --- | --- | --- |",
    ]
    for entry in entries:
        url = entry.get("ui_url") or ""
        link = f"[{entry.get('id')}]({url})" if entry.get("id") and url else "-"
        artifact = f"`factory_runs/{args.run_id}/{entry['name']}.final.md`"
        lines.append(f"| `{entry['name']}` | {entry.get('status', 'unknown')} | {link} | {artifact} |")
    lines.extend(["", "## Gate Summary", ""])
    for entry in entries:
        lines.append(f"- `{entry['name']}`: {entry.get('status', 'unknown')}")
    lines.extend(
        [
            "",
            "## Human Next Step",
            "",
            "Review the child conversation outputs, inspect the PR or branch produced by story-to-pr, then decide whether review or merge is appropriate.",
            "",
        ]
    )
    return "\n".join(lines)


def jira_summary_comment(args: argparse.Namespace, entries: list[dict[str, Any]]) -> str:
    child_lines = []
    for entry in entries:
        url = entry.get("ui_url") or "no conversation URL"
        child_lines.append(f"- {entry['name']}: {entry.get('status', 'unknown')} - {url}")
    return "\n".join(
        [
            "OpenHands delegated SDLC run complete",
            f"Issue: {args.issue_key}",
            f"Run id: {args.run_id}",
            f"Repository: {args.repo_slug}",
            "Child conversations:",
            *child_lines,
            "Human next step: review the child outputs and any draft PR before merge.",
        ]
    )


def run_factory(args: argparse.Namespace) -> int:
    if args.env_file:
        oh.load_env_file(args.env_file)
    if args.issue_key and (not args.request_title or not args.request_body):
        issue = fetch_jira_issue(args.issue_key)
        args.request_title = args.request_title or issue["request_title"]
        args.request_body = args.request_body or issue["request_body"]
        args.issue_url = args.issue_url or issue["issue_url"]

    base = oh.base_url(args.base_url)
    headers = oh.build_headers(oh.read_api_key())
    run_dir = REPO_ROOT / "factory_runs" / args.run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    create_manifest(args, run_dir)

    entries: list[dict[str, Any]] = []
    prior_summary = ""
    for cell in args.cells:
        try:
            entry = start_and_wait_cell(
                args=args,
                base=base,
                headers=headers,
                run_dir=run_dir,
                cell=cell,
                prior_summary=prior_summary,
            )
        except Exception as exc:
            entry = {
                "name": cell,
                "status": "needs-human",
                "error": "The work cell could not be completed; inspect the parent conversation.",
                "error_type": type(exc).__name__,
                "final_text": "",
            }
            print(f"Delegated work cell could not complete: {cell} ({type(exc).__name__})", flush=True)
        entries.append(entry)
        write_json(run_dir / "children.json", entries)
        prior_summary += f"\n\n## {cell}\nstatus: {entry.get('status')}\nurl: {entry.get('ui_url')}\n{entry.get('final_text', '')}"
        if not gate_allows_next_cell(
            cell,
            str(entry.get("status", "unknown")),
            str(entry.get("final_text", "")),
        ):
            break

    report = lifecycle_report(args, entries)
    write_text(run_dir / "lifecycle-report.md", report)
    if args.post_jira_comment and args.issue_key:
        post_jira_comment(args.issue_key, jira_summary_comment(args, entries))
    print(json.dumps({"run_dir": str(run_dir), "entries": entries}, indent=2, sort_keys=True))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", help="OpenHands base URL")
    parser.add_argument("--env-file", type=Path)
    parser.add_argument("--repo-slug", required=True)
    parser.add_argument("--branch", default="main")
    parser.add_argument("--run-id", default=time.strftime("replicated-factory-%Y%m%d-%H%M%S"))
    parser.add_argument("--issue-key", required=True)
    parser.add_argument("--issue-url")
    parser.add_argument("--request-title")
    parser.add_argument("--request-body")
    parser.add_argument("--cells", nargs="+", choices=ACTIVE_WORK_CELLS, default=list(ACTIVE_WORK_CELLS))
    parser.add_argument("--child-llm-model")
    parser.add_argument("--start-timeout-seconds", type=int, default=600)
    parser.add_argument("--cell-timeout-seconds", type=int, default=900)
    parser.add_argument("--poll-seconds", type=int, default=20)
    parser.add_argument("--post-jira-comment", action="store_true")
    return parser


def main() -> int:
    return run_factory(build_parser().parse_args())


if __name__ == "__main__":
    raise SystemExit(main())
