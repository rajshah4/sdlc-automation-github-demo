#!/usr/bin/env python3
"""Build a read-only SDLC context sidekick brief.

The script searches only demo-safe repo paths and writes a compact Markdown
brief to stdout. It does not modify files or call external services.
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
ALLOWED_ROOTS = [
    REPO_ROOT / "README.md",
    REPO_ROOT / "AGENTS.md",
    REPO_ROOT / "docs" / "wiki",
    REPO_ROOT / "docs" / "logs",
    REPO_ROOT / "app",
    REPO_ROOT / "tests",
    REPO_ROOT / "skills",
    REPO_ROOT / "openspec",
]


@dataclass
class Match:
    path: Path
    term: str
    line: str


def read_body(args: argparse.Namespace) -> str:
    if args.body_file:
        return Path(args.body_file).read_text(encoding="utf-8")
    if args.body:
        return args.body
    if not sys.stdin.isatty():
        return sys.stdin.read()
    return ""


def allowed_files() -> list[Path]:
    files: list[Path] = []
    for root in ALLOWED_ROOTS:
        if root.is_file():
            files.append(root)
        elif root.is_dir():
            files.extend(path for path in root.rglob("*") if path.is_file())
    return sorted(
        path
        for path in files
        if ".env" not in path.parts
        and "__pycache__" not in path.parts
        and path.suffix not in {".pyc", ".png", ".gif", ".jpg", ".jpeg", ".mp4"}
    )


def search_terms(title: str, body: str) -> list[str]:
    text = f"{title}\n{body}".lower()
    terms = {"catalog", "available", "pending", "pet", "test"}
    if "nova" in text:
        terms.update({"nova", "pet-103"})
    if "not available" in text or "unavailable" in text or "adoptable" in text:
        terms.update({"PENDING_PET_VISIBLE", "status", "available-only"})
    if "fee" in text or "price" in text or "cost" in text:
        terms.update({"fee", "adoption_fee", "max_fee"})
    if "age" in text:
        terms.update({"age", "min_age", "max_age"})
    return sorted(terms, key=str.lower)


def find_matches(terms: list[str], limit_per_term: int = 4) -> list[Match]:
    matches: list[Match] = []
    files = allowed_files()
    for term in terms:
        found = 0
        needle = term.lower()
        for path in files:
            try:
                lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
            except OSError:
                continue
            for line in lines:
                if needle in line.lower():
                    matches.append(Match(path=path, term=term, line=line.strip()))
                    found += 1
                    break
            if found >= limit_per_term:
                break
    return matches


def rel(path: Path) -> str:
    return str(path.relative_to(REPO_ROOT))


def first_by_prefix(matches: list[Match], prefix: str, limit: int = 3) -> list[Match]:
    selected: list[Match] = []
    seen: set[Path] = set()
    for match in matches:
        if rel(match.path).startswith(prefix) and match.path not in seen:
            selected.append(match)
            seen.add(match.path)
        if len(selected) >= limit:
            break
    return selected


def likely_files(matches: list[Match]) -> list[str]:
    candidates = [
        "app/petstore_app/catalog.py",
        "app/tests/test_pet_catalog.py",
        "app/petstore_app/cloud_run_app.py",
        "tests/fixtures/github_issue_labeled_build.json",
    ]
    found = {rel(match.path) for match in matches}
    ordered = [path for path in candidates if path in found or (REPO_ROOT / path).exists()]
    return ordered[:4]


def confidence(matches: list[Match], files: list[str]) -> tuple[str, str]:
    has_wiki = any(rel(match.path).startswith("docs/wiki/") for match in matches)
    has_logs = any(rel(match.path).startswith("docs/logs/") for match in matches)
    has_app = any(path.startswith("app/") for path in files)
    has_tests = any("test" in path for path in files)
    if has_wiki and has_logs and has_app and has_tests:
        return "high", "ticket, docs, logs, app files, and tests point to the same catalog slice"
    if has_app and (has_wiki or has_logs or has_tests):
        return "medium", "likely implementation area is clear, but evidence is partial"
    if files:
        return "low", "some candidate files exist, but evidence is not strong enough"
    return "NEEDS_HUMAN", "no confident repo area was found from allowed context"


def bullet_matches(matches: list[Match], empty: str) -> list[str]:
    if not matches:
        return [f"- {empty}"]
    return [
        f"- {rel(match.path)}: `{match.term}` -> {match.line[:140]}"
        for match in matches
    ]


def build_brief(args: argparse.Namespace) -> str:
    body = read_body(args)
    terms = search_terms(args.title, body)
    matches = find_matches(terms)
    docs = first_by_prefix(matches, "docs/wiki/")
    logs = first_by_prefix(matches, "docs/logs/")
    files = likely_files(matches)
    level, rationale = confidence(matches, files)
    ticket = args.jira_key or args.jira_url or "unknown"

    lines = [
        "CONTEXT_BRIEF",
        f"Ticket: {ticket}",
        f"Summary: {args.title.strip() or 'No summary provided.'}",
        "",
        "LIKELY_REPO_AREA",
        "- Petstore catalog availability: sparse ticket language points to available/pending pet visibility.",
        "",
        "DOCS_CHECKED",
        *bullet_matches(docs, "no matching wiki document found in allowed paths"),
        "",
        "LOGS_CHECKED",
        *bullet_matches(logs, "no matching log evidence found in allowed paths"),
        "",
        "LIKELY_FILES",
    ]
    if files:
        lines.extend(f"- {path}: inspect before editing" for path in files)
    else:
        lines.append("- none found")

    lines.extend(
        [
            "",
            "MISSING_INFO",
            "- none" if level in {"high", "medium"} else "- ask a human for the affected product area or log evidence",
            "",
            "CONFIDENCE",
            f"- {level}: {rationale}",
            "",
            "RECOMMENDED_NEXT_STEP",
            "- Hand this brief to `skills/sdlc-story/SKILL.md`; the main agent should create artifacts, implement the fix, add tests, and open the PR.",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--jira-key", default="")
    parser.add_argument("--jira-url", default="")
    parser.add_argument("--title", required=True)
    parser.add_argument("--body", default="")
    parser.add_argument("--body-file")
    args = parser.parse_args()
    print(build_brief(args))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
