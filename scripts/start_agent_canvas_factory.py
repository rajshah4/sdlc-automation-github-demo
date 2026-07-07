#!/usr/bin/env python3
"""Start the parent Agent Canvas conversation for the SDLC factory demo."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import subprocess
import time
from pathlib import Path
from typing import Any

import agent_canvas_delegate as canvas


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SUPERVISOR_PROMPT = REPO_ROOT / "agent-canvas" / "prompts" / "supervisor.md"


def git_remote_slug(repo: Path) -> str:
    try:
        result = subprocess.run(
            ["git", "-C", str(repo), "config", "--get", "remote.origin.url"],
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError:
        return "rajshah4/sdlc-automation-github-demo"

    remote = result.stdout.strip()
    if not remote:
        return "rajshah4/sdlc-automation-github-demo"
    if remote.startswith("git@github.com:"):
        remote = remote.removeprefix("git@github.com:").removesuffix(".git")
    if remote.startswith("https://github.com/"):
        remote = remote.removeprefix("https://github.com/").removesuffix(".git")
    return remote


def build_variables(args: argparse.Namespace, run_id: str, repo: Path) -> dict[str, str]:
    code_review_profile_arg = ""
    if args.code_review_profile:
        code_review_profile_arg = f'--code-review-profile "{args.code_review_profile}"'
    qa_playwright_arg = ""
    if args.require_playwright_qa:
        qa_playwright_arg = "--require-playwright-qa"
        if args.playwright_node_path:
            qa_playwright_arg += f' --playwright-node-path "{args.playwright_node_path}"'
    return {
        "run_id": run_id,
        "run_date": args.run_date,
        "repo_path": str(repo.resolve()),
        "repo_slug": args.repo_slug or git_remote_slug(repo),
        "request_title": args.request_title,
        "request_body": args.request_body,
        "issue_number": str(args.issue_number),
        "code_review_profile_arg": code_review_profile_arg,
        "qa_playwright_arg": qa_playwright_arg,
    }


def start_supervisor(args: argparse.Namespace) -> dict[str, Any]:
    repo = args.repo.resolve()
    run_id = args.run_id or time.strftime("canvas-factory-%Y%m%d-%H%M%S")
    prompt = canvas.render_prompt(args.prompt_file, build_variables(args, run_id, repo))

    if args.render_only:
        return {"run_id": run_id, "prompt": prompt}

    key = canvas.read_session_key()
    base = canvas.discover_base(args.base, key)
    settings_response = canvas.http_json(
        "GET",
        f"{base}/api/settings",
        key=key,
        expose_encrypted_secrets=True,
    )

    response = canvas.create_conversation(
        base=base,
        key=key,
        settings_response=settings_response,
        prompt=prompt,
        workspace=repo,
        max_iterations=args.max_iterations,
        include_task_tools=True,
        run=not args.no_run,
    )
    summary = canvas.conversation_summary(base, args.ui_base, response)
    summary.update({"run_id": run_id, "role": "factory-supervisor"})
    run_dir = repo / "factory_runs" / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "parent.conversation.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return summary


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", help="Agent Canvas API base URL")
    parser.add_argument("--ui-base", default=canvas.DEFAULT_UI_BASE, help="Agent Canvas UI base URL")
    parser.add_argument("--repo", type=Path, default=REPO_ROOT, help="local repository path")
    parser.add_argument("--repo-slug", help="GitHub owner/name, default from git remote")
    parser.add_argument("--prompt-file", type=Path, default=DEFAULT_SUPERVISOR_PROMPT)
    parser.add_argument("--run-id", help="stable run id; defaults to timestamp")
    parser.add_argument("--run-date", default=dt.date.today().isoformat(), help="date to use in generated reports")
    parser.add_argument("--issue-number", type=int, default=88)
    parser.add_argument("--request-title", default="Filter pets by max adoption fee")
    parser.add_argument(
        "--request-body",
        default=(
            "As an adoption coordinator, I want to filter available pets by maximum adoption fee "
            "so families can find pets that fit their budget."
        ),
    )
    parser.add_argument("--max-iterations", type=int, default=1000)
    parser.add_argument("--code-review-profile", help="Agent Canvas profile name to use only for the code-review child")
    parser.add_argument("--require-playwright-qa", action="store_true", help="Require QA child to run Playwright UI evidence")
    parser.add_argument("--playwright-node-path", help="NODE_PATH pointing at an existing node_modules with Playwright")
    parser.add_argument("--no-run", action="store_true", help="create the supervisor without starting it")
    parser.add_argument("--render-only", action="store_true", help="print the supervisor prompt instead of creating a conversation")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    summary = start_supervisor(args)
    if args.render_only:
        print(summary["prompt"])
    else:
        print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
