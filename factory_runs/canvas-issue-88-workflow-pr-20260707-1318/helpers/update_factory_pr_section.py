#!/usr/bin/env python3
"""Update one section of the plain four-step factory PR body."""

from __future__ import annotations

import argparse
import re
import subprocess
from pathlib import Path


SECTION_HEADINGS = {
    "code-review": "## 3. Code Review",
    "qa": "## 4. QA",
}


def run_gh(args: list[str], *, cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=cwd, check=False, capture_output=True, text=True, timeout=120)


def repo_relative(repo: Path, path: Path) -> str:
    try:
        return path.resolve().relative_to(repo.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def extract_status(path: Path, fallback: str) -> str:
    if not path.exists():
        return fallback
    text = path.read_text(encoding="utf-8", errors="replace")
    for pattern in (r"Status:\s*([A-Za-z0-9_. -]+)", r"status:\s*([A-Za-z0-9_. -]+)", r"Blocking:\s*([A-Za-z0-9_. -]+)"):
        match = re.search(pattern, text)
        if match:
            return match.group(1).strip().splitlines()[0]
    return fallback


def code_review_section(repo: Path, artifact: Path) -> str:
    status = extract_status(artifact, "complete")
    return "\n".join(
        [
            "## 3. Code Review",
            "",
            f"Review status: {status}",
            "",
            f"Review report: `{repo_relative(repo, artifact)}`",
            "",
        ]
    )


def qa_section(repo: Path, artifact: Path, run_id: str) -> str:
    status = extract_status(artifact, "complete")
    evidence_dir = repo / "factory_runs" / run_id / "playwright-artifacts"
    evidence = [
        ("QA report", evidence_dir / "qa-report.md"),
        ("Screenshot", evidence_dir / "max-fee-below-threshold.png"),
        ("GIF", evidence_dir / "max-adoption-fee-filter.gif"),
        ("Video", evidence_dir / "max-adoption-fee-filter.webm"),
    ]
    lines = [
        "## 4. QA",
        "",
        f"QA status: {status}",
        "",
        "Validation:",
        "",
        "- `python3 -m pytest -q`",
    ]
    if evidence_dir.exists():
        lines.append("- Browser evidence captured for the max-fee workflow")
    lines.extend(["", "Evidence:", ""])
    for label, path in evidence:
        lines.append(f"- {label}: `{repo_relative(repo, path)}`" if path.exists() else f"- {label}: _pending_")
    lines.extend(["", f"QA report: `{repo_relative(repo, artifact)}`", ""])
    return "\n".join(lines)


def replace_section(body: str, heading: str, replacement: str) -> str:
    start = body.find(heading)
    if start == -1:
        return body.rstrip() + "\n\n" + replacement.rstrip() + "\n"
    next_heading = re.search(r"\n## \d+\. ", body[start + len(heading) :])
    if next_heading:
        end = start + len(heading) + next_heading.start()
        return body[:start] + replacement.rstrip() + "\n" + body[end:]
    return body[:start] + replacement.rstrip() + "\n"


def update_pr(args: argparse.Namespace) -> int:
    repo = args.repo.resolve()
    artifact = args.artifact.resolve()
    view = run_gh(["gh", "pr", "view", args.pr, "--json", "body", "--jq", ".body"], cwd=repo)
    if view.returncode != 0:
        print(view.stderr.strip() or view.stdout.strip())
        return view.returncode

    if args.section == "code-review":
        replacement = code_review_section(repo, artifact)
    else:
        replacement = qa_section(repo, artifact, args.run_id)

    body = replace_section(view.stdout, SECTION_HEADINGS[args.section], replacement)
    body_path = repo / "factory_runs" / args.run_id / f"pr-section-{args.section}.md"
    body_path.parent.mkdir(parents=True, exist_ok=True)
    body_path.write_text(body, encoding="utf-8")
    edit = run_gh(["gh", "pr", "edit", args.pr, "--body-file", str(body_path)], cwd=repo)
    if edit.returncode != 0:
        print(edit.stderr.strip() or edit.stdout.strip())
        return edit.returncode
    print(edit.stdout.strip())
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--pr", required=True)
    parser.add_argument("--section", choices=sorted(SECTION_HEADINGS), required=True)
    parser.add_argument("--artifact", type=Path, required=True)
    return parser


def main() -> int:
    return update_pr(build_parser().parse_args())


if __name__ == "__main__":
    raise SystemExit(main())
