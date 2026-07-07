#!/usr/bin/env python3
# Runs the parent-side workflow that delegates story, review, and QA workcells.
"""Run the delegated Agent Canvas SDLC factory from a supervisor conversation."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import shutil
import subprocess
import time
from pathlib import Path
from typing import Any
from urllib.parse import quote

import agent_canvas_delegate as canvas


SCRIPT_ROOT = Path(__file__).resolve().parent
REPO_ROOT = Path(__file__).resolve().parents[2]
ACTIVE_WORK_CELLS = ("story-to-pr", "code-review", "qa")
WORK_CELLS = ACTIVE_WORK_CELLS
PR_URL_RE = re.compile(r"https://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+/pull/\d+")


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def run_command(args: list[str], *, cwd: Path, timeout: int = 120) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        cwd=cwd,
        check=False,
        capture_output=True,
        text=True,
        timeout=timeout,
    )


def repo_relative(repo: Path, path: Path) -> str:
    try:
        return path.resolve().relative_to(repo.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def find_pr_url(args: argparse.Namespace, run_dir: Path) -> str | None:
    candidates = [
        run_dir / "story-to-pr.md",
        run_dir / "code-review.md",
        run_dir / "qa.md",
        run_dir / "story-to-pr.final.json",
        run_dir / "children.json",
    ]
    for path in candidates:
        if path.exists():
            match = PR_URL_RE.search(path.read_text(encoding="utf-8", errors="replace"))
            if match:
                return match.group(0)

    try:
        result = run_command(["gh", "pr", "view", "--json", "state,url"], cwd=args.repo)
    except (OSError, subprocess.TimeoutExpired):
        return None
    if result.returncode == 0:
        try:
            data = json.loads(result.stdout)
        except json.JSONDecodeError:
            return None
        url = str(data.get("url") or "").strip()
        if data.get("state") == "OPEN" and PR_URL_RE.fullmatch(url):
            return url
    return None


def report_status(path: Path) -> str:
    if not path.exists():
        return "pending"
    text = path.read_text(encoding="utf-8", errors="replace")
    for pattern in (
        r"Status:\s*([A-Za-z0-9_. -]+)",
        r"status:\s*([A-Za-z0-9_. -]+)",
        r"Blocking:\s*([A-Za-z0-9_. -]+)",
    ):
        match = re.search(pattern, text)
        if match:
            return match.group(1).strip().splitlines()[0]
    return "complete"


def artifact_ref(args: argparse.Namespace, path: Path) -> str:
    return f"`{repo_relative(args.repo, path)}`" if path.exists() else "_pending_"


def existing_key_files(repo: Path) -> list[str]:
    candidates = [
        "app/petstore_app/catalog.py",
        "app/tests/test_pet_catalog.py",
        "app/web/index.html",
        "app/web/app.js",
        "app/web/tests/max-adoption-fee-filter.playwright.mjs",
        "app/web/tests/catalog-search.playwright.mjs",
    ]
    return [path for path in candidates if (repo / path).exists()]


def playwright_validation_command(repo: Path) -> str:
    if (repo / "agent-canvas" / "scripts" / "run_petstore_playwright_qa.py").exists():
        return "`python3 agent-canvas/scripts/run_petstore_playwright_qa.py --artifact-dir factory_runs/<run-id>/playwright-artifacts --playwright-node-path <playwright-node-path>`"
    return "`NODE_PATH=<playwright-node-path> node app/web/tests/catalog-search.playwright.mjs --artifact-dir factory_runs/<run-id>/playwright-artifacts`"


def compose_plain_pr_body(args: argparse.Namespace, run_dir: Path) -> str:
    story_report = run_dir / "story-to-pr.md"
    review_report = run_dir / "code-review.md"
    qa_report = run_dir / "qa.md"
    browser_report = run_dir / "playwright-artifacts" / "qa-report.md"
    screenshot = run_dir / "playwright-artifacts" / "max-fee-below-threshold.png"
    gif = run_dir / "playwright-artifacts" / "max-adoption-fee-filter.gif"
    video = run_dir / "playwright-artifacts" / "max-adoption-fee-filter.webm"

    review_status = report_status(review_report)
    qa_status = report_status(qa_report)

    lines = [
            "## 1. Story",
            "",
            f"Closes #{args.issue_number}",
            "",
            f"{args.request_title}",
            "",
            args.request_body,
            "",
            "Acceptance focus:",
            "",
            "- Blank max-fee input keeps the existing catalog behavior.",
            "- Max-fee filtering is inclusive at the threshold.",
            "- Pending pets remain hidden.",
            "- Negative backend max-fee values are rejected.",
            "",
            "## 2. Code",
            "",
            "Built the max adoption fee filter across the backend catalog and static Petstore UI.",
            "",
            "Key files:",
            "",
    ]
    lines.extend(f"- `{path}`" for path in existing_key_files(args.repo))
    lines.extend(
        [
            "",
            f"Implementation report: {artifact_ref(args, story_report)}",
            "",
            "## 3. Code Review",
            "",
            f"Review status: {review_status}",
            "",
            f"Review report: {artifact_ref(args, review_report)}",
            "",
            "## 4. QA",
            "",
            f"QA status: {qa_status}",
            "",
            "Validation:",
            "",
            "- `python3 -m pytest -q`",
            f"- {playwright_validation_command(args.repo)}",
            "",
            "Evidence:",
            "",
            f"- QA report: {artifact_ref(args, browser_report)}",
            f"- Screenshot: {artifact_ref(args, screenshot)}",
            f"- GIF: {artifact_ref(args, gif)}",
            f"- Video: {artifact_ref(args, video)}",
            "",
            f"QA report: {artifact_ref(args, qa_report)}",
            "",
        ]
    )
    return "\n".join(lines)


def curated_run_artifacts(run_dir: Path) -> list[Path]:
    artifacts = [
        run_dir / "story-to-pr.md",
        run_dir / "code-review.md",
        run_dir / "qa.md",
        run_dir / "children-summary.md",
        run_dir / "lifecycle-report.md",
        run_dir / "pr-body.md",
        run_dir / "pr-body-sync.md",
        run_dir / "artifact-publish.md",
    ]
    evidence_dir = run_dir / "playwright-artifacts"
    if evidence_dir.exists():
        artifacts.extend(sorted(path for path in evidence_dir.iterdir() if path.is_file()))
    return [path for path in artifacts if path.exists()]


def publish_run_artifacts(args: argparse.Namespace, run_dir: Path) -> None:
    if args.no_publish_run_artifacts:
        return

    log_path = run_dir / "artifact-publish.md"
    artifacts = curated_run_artifacts(run_dir)
    if not artifacts:
        log_path.write_text("No curated run artifacts were available to publish.\n", encoding="utf-8")
        return

    lines = ["# Artifact Publish", ""]
    rel_paths = [repo_relative(args.repo, path) for path in artifacts]
    add_result = run_command(["git", "add", *rel_paths], cwd=args.repo)
    lines.append(f"- git add: exit {add_result.returncode}")
    if add_result.stderr.strip():
        lines.append(f"- git add stderr: `{add_result.stderr.strip()}`")

    diff_result = run_command(["git", "diff", "--cached", "--quiet"], cwd=args.repo)
    if diff_result.returncode == 0:
        lines.append("- No staged artifact changes to commit.")
        log_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return

    commit_result = run_command(
        ["git", "commit", "-m", f"chore: add factory evidence for {args.run_id}"],
        cwd=args.repo,
        timeout=180,
    )
    lines.append(f"- git commit: exit {commit_result.returncode}")
    if commit_result.stdout.strip():
        lines.append("```text")
        lines.append(commit_result.stdout.strip())
        lines.append("```")
    if commit_result.stderr.strip():
        lines.append(f"- git commit stderr: `{commit_result.stderr.strip()}`")

    if commit_result.returncode == 0:
        push_result = run_command(["git", "push"], cwd=args.repo, timeout=180)
        lines.append(f"- git push: exit {push_result.returncode}")
        if push_result.stderr.strip():
            lines.append(f"- git push stderr: `{push_result.stderr.strip()}`")

    log_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def sync_plain_pr_body(args: argparse.Namespace, run_dir: Path) -> None:
    if args.no_pr_body_sync:
        return

    body_path = run_dir / "pr-body.md"
    sync_path = run_dir / "pr-body-sync.md"
    body_path.write_text(compose_plain_pr_body(args, run_dir), encoding="utf-8")
    pr_url = find_pr_url(args, run_dir)
    if not pr_url:
        sync_path.write_text(
            "No PR URL was available yet, so the automation did not update a PR body.\n",
            encoding="utf-8",
        )
        return

    try:
        result = run_command(["gh", "pr", "edit", pr_url, "--body-file", str(body_path)], cwd=args.repo)
    except (OSError, subprocess.TimeoutExpired) as exc:
        sync_path.write_text(f"Unable to update PR body: {exc}\n", encoding="utf-8")
        return

    lines = [
        "# PR Body Sync",
        "",
        f"- PR: {pr_url}",
        f"- Body file: `{repo_relative(args.repo, body_path)}`",
        f"- Command: `gh pr edit <pr-url> --body-file {repo_relative(args.repo, body_path)}`",
        f"- Exit code: {result.returncode}",
    ]
    if result.stdout.strip():
        lines.extend(["", "```text", result.stdout.strip(), "```"])
    if result.stderr.strip():
        lines.extend(["", "```text", result.stderr.strip(), "```"])
    sync_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def should_wait_for_cell(args: argparse.Namespace, cell: str) -> bool:
    if args.no_wait:
        return False
    if args.handoff_after_story and cell != "story-to-pr":
        return False
    return True


def prompt_snapshot_dir(run_dir: Path) -> Path:
    return run_dir / "prompt-snapshot"


def snapshot_prompts(run_dir: Path) -> Path:
    source = REPO_ROOT / "agent-canvas" / "prompts"
    target = prompt_snapshot_dir(run_dir)
    shutil.copytree(source, target, dirs_exist_ok=True)
    return target


def snapshot_helpers(run_dir: Path) -> Path:
    target = run_dir / "helpers"
    target.mkdir(parents=True, exist_ok=True)
    for name in ("update_factory_pr_section.py",):
        shutil.copy2(SCRIPT_ROOT / name, target / name)
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
    snapshot_helpers(run_dir)
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

        if should_wait_for_cell(args, cell):
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
            sync_plain_pr_body(args, run_dir)
            publish_run_artifacts(args, run_dir)
        elif args.handoff_after_story and cell != "story-to-pr":
            entry["handoff"] = True
            update_summary(run_dir, entries)
            write_children(run_dir, entries)

    write_children(run_dir, entries)
    sync_plain_pr_body(args, run_dir)
    publish_run_artifacts(args, run_dir)
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
    parser.add_argument(
        "--handoff-after-story",
        action="store_true",
        help="Wait for story-to-pr, then launch later delegates without holding the parent terminal open",
    )
    parser.add_argument("--require-playwright-qa", action="store_true", help="Require QA to run Playwright UI evidence instead of falling back silently")
    parser.add_argument("--playwright-node-path", help="NODE_PATH pointing at an existing node_modules with Playwright")
    parser.add_argument("--no-pr-body-sync", action="store_true", help="Do not update the automation-created PR body from run artifacts")
    parser.add_argument("--no-publish-run-artifacts", action="store_true", help="Do not commit and push curated factory run artifacts")
    return parser


def main() -> int:
    return run_factory(build_parser().parse_args())


if __name__ == "__main__":
    raise SystemExit(main())
