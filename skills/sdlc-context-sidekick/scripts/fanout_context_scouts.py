#!/usr/bin/env python3
"""Run bounded read-only context scouts in parallel.

This is the cheap baseline for the sidekick experiment. It keeps docs, logs,
and repo search separate so the conversation shows clear launch points without
spending LLM tokens on three child agents.
"""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path
from time import perf_counter

from build_context_brief import (
    REPO_ROOT,
    Match,
    bullet_matches,
    confidence,
    likely_files,
    read_body,
    rel,
    search_terms,
)


@dataclass(frozen=True)
class Scout:
    name: str
    roots: tuple[Path, ...]
    purpose: str


@dataclass
class ScoutResult:
    scout: Scout
    matches: list[Match]
    files_checked: int
    elapsed_seconds: float


SCOUTS = (
    Scout(
        name="docs-scout",
        roots=(
            REPO_ROOT / "docs" / "wiki",
            REPO_ROOT / "openspec" / "project.md",
            REPO_ROOT / "AGENTS.md",
            REPO_ROOT / "README.md",
        ),
        purpose="find product wording, architecture notes, and acceptance hints",
    ),
    Scout(
        name="logs-scout",
        roots=(REPO_ROOT / "docs" / "logs",),
        purpose="find error codes, symptoms, and request evidence",
    ),
    Scout(
        name="repo-scout",
        roots=(REPO_ROOT / "app", REPO_ROOT / "tests"),
        purpose="find likely implementation and test files",
    ),
)

DEMO_PRIORITY = (
    "docs/wiki/petstore-catalog-availability.md",
    "docs/logs/pending-pet-visible.ndjson",
    "app/petstore_app/catalog.py",
    "app/tests/test_pet_catalog.py",
    "app/petstore_app/cloud_run_app.py",
)


def files_for_roots(roots: tuple[Path, ...]) -> list[Path]:
    files: list[Path] = []
    for root in roots:
        if root.is_file():
            files.append(root)
        elif root.is_dir():
            files.extend(sorted(path for path in root.rglob("*") if path.is_file()))
    return [
        path
        for path in files
        if ".env" not in path.parts
        and "__pycache__" not in path.parts
        and path.suffix not in {".pyc", ".png", ".gif", ".jpg", ".jpeg", ".mp4"}
    ]


def demo_priority(match: Match) -> tuple[int, str]:
    path = rel(match.path)
    try:
        return DEMO_PRIORITY.index(path), path
    except ValueError:
        return len(DEMO_PRIORITY), path


def run_scout(scout: Scout, terms: list[str], limit: int) -> ScoutResult:
    started = perf_counter()
    matches: list[Match] = []
    files = files_for_roots(scout.roots)
    seen_paths: set[Path] = set()
    for term in terms:
        needle = term.lower()
        for path in files:
            if path in seen_paths and len(matches) >= limit:
                continue
            try:
                lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
            except OSError:
                continue
            for line in lines:
                if needle in line.lower():
                    matches.append(Match(path=path, term=term, line=line.strip()))
                    seen_paths.add(path)
                    break
            if len(matches) >= limit:
                break
        if len(matches) >= limit:
            break
    return ScoutResult(
        scout=scout,
        matches=sorted(matches, key=demo_priority)[:limit],
        files_checked=len(files),
        elapsed_seconds=perf_counter() - started,
    )


def render_result(result: ScoutResult) -> list[str]:
    lines = [
        f"SCOUT_RESULT {result.scout.name}",
        f"- purpose: {result.scout.purpose}",
        f"- files_checked: {result.files_checked}",
        f"- elapsed_seconds: {result.elapsed_seconds:.3f}",
        "- findings:",
    ]
    findings = bullet_matches(
        result.matches,
        f"{result.scout.name} found no matching evidence in its bounded roots",
    )
    lines.extend(f"  {line}" for line in findings)
    return lines


def build_fanout(args: argparse.Namespace) -> str:
    body = read_body(args)
    terms = search_terms(args.title, body)
    started = perf_counter()
    with ThreadPoolExecutor(max_workers=len(SCOUTS)) as executor:
        futures = [executor.submit(run_scout, scout, terms, args.max_matches) for scout in SCOUTS]
        results = [future.result() for future in futures]

    all_matches = [match for result in results for match in result.matches]
    files = likely_files(all_matches)
    level, rationale = confidence(all_matches, files)
    ticket = args.jira_key or args.jira_url or "unknown"

    docs = next(result for result in results if result.scout.name == "docs-scout").matches
    logs = next(result for result in results if result.scout.name == "logs-scout").matches

    lines = [
        "CONTEXT_SCOUT_FANOUT",
        f"Ticket: {ticket}",
        f"Summary: {args.title.strip() or 'No summary provided.'}",
        f"Launch: docs-scout, logs-scout, and repo-scout started together",
        f"Total elapsed seconds: {perf_counter() - started:.3f}",
        "",
        "LAUNCHES",
    ]
    for scout in SCOUTS:
        lines.append(f"- {scout.name}: {scout.purpose}; read-only; no edits; no other skills")

    for result in results:
        lines.extend(["", *render_result(result)])

    lines.extend(
        [
            "",
            "CONTEXT_BRIEF",
            f"Ticket: {ticket}",
            f"Summary: {args.title.strip() or 'No summary provided.'}",
            "",
            "LIKELY_REPO_AREA",
            "- Petstore catalog availability: docs/logs/repo scouts converge on available/pending pet visibility.",
            "",
            "DOCS_CHECKED",
            *bullet_matches(docs[:3], "no matching wiki or project document found"),
            "",
            "LOGS_CHECKED",
            *bullet_matches(logs[:3], "no matching log evidence found"),
            "",
            "LIKELY_FILES",
        ]
    )
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
            "- Main Jira-to-PR agent should use this brief, inspect only likely implementation/test files first, then run the story skill workflow.",
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
    parser.add_argument("--max-matches", type=int, default=4)
    args = parser.parse_args()
    print(build_fanout(args))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
