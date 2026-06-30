#!/usr/bin/env python3
"""Build a cost-aware context reuse report for the SDLC Automation Demo.

This script is intentionally deterministic: it reads repo-local memory,
skills, prior evidence, and targeted search results before any LLM reasoning is
needed. The resulting report is a live-demo artifact that shows what an agent
can reuse instead of rediscovering the repository from scratch.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = REPO_ROOT / "docs" / "context-reuse" / "latest-context-reuse-report.md"

EXCLUDED_DIRS = {
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    "__pycache__",
    "node_modules",
    ".venv",
    "venv",
}
TEXT_SUFFIXES = {
    ".css",
    ".html",
    ".js",
    ".json",
    ".md",
    ".mjs",
    ".py",
    ".toml",
    ".txt",
    ".yaml",
    ".yml",
}


@dataclass(frozen=True)
class TriggerContext:
    event_type: str
    title: str
    body: str
    labels: tuple[str, ...]
    number: int | None = None
    url: str | None = None


@dataclass(frozen=True)
class SearchHit:
    path: Path
    score: int
    snippets: tuple[str, ...]


def estimate_tokens(text: str) -> int:
    """Return a rough token estimate for demo cost comparisons."""
    return max(1, len(text) // 4)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def should_scan(path: Path) -> bool:
    if any(part in EXCLUDED_DIRS for part in path.parts):
        return False
    if path.is_dir():
        return False
    if path.suffix.lower() not in TEXT_SUFFIXES:
        return False
    try:
        return path.stat().st_size <= 250_000
    except OSError:
        return False


def iter_text_files(root: Path) -> Iterable[Path]:
    for path in root.rglob("*"):
        rel_parts = path.relative_to(root).parts
        if any(part in EXCLUDED_DIRS for part in rel_parts):
            continue
        if should_scan(path):
            yield path


def trigger_from_fixture(path: Path) -> TriggerContext:
    payload = json.loads(path.read_text(encoding="utf-8"))
    event_name = payload.get("_event_name") or payload.get("webhookEvent", "unknown")
    if event_name == "issues":
        issue = payload.get("issue") or {}
        return TriggerContext(
            event_type=f"issues.{payload.get('action', 'unknown')}",
            title=issue.get("title", ""),
            body=issue.get("body", ""),
            labels=tuple(item.get("name", "") for item in issue.get("labels", [])),
            number=issue.get("number"),
            url=issue.get("html_url"),
        )
    if event_name == "pull_request":
        pr = payload.get("pull_request") or {}
        return TriggerContext(
            event_type=f"pull_request.{payload.get('action', 'unknown')}",
            title=pr.get("title", ""),
            body=pr.get("body", ""),
            labels=tuple(item.get("name", "") for item in pr.get("labels", [])),
            number=pr.get("number"),
            url=pr.get("html_url"),
        )
    return TriggerContext(
        event_type=str(event_name),
        title=payload.get("issueKey", "Unknown event"),
        body=json.dumps(payload, indent=2, sort_keys=True),
        labels=(),
    )


def trigger_from_args(title: str, body: str, labels: list[str]) -> TriggerContext:
    return TriggerContext(
        event_type="manual.demo",
        title=title,
        body=body,
        labels=tuple(labels),
    )


def search_terms(trigger: TriggerContext) -> list[str]:
    raw = " ".join([trigger.title, trigger.body, " ".join(trigger.labels)]).lower()
    words = re.findall(r"[a-z][a-z0-9_-]{2,}", raw)
    stop = {
        "and",
        "are",
        "can",
        "for",
        "from",
        "issue",
        "label",
        "open",
        "openhands",
        "pet",
        "pets",
        "that",
        "the",
        "this",
        "want",
        "with",
    }
    selected = [word for word in words if word not in stop]
    domain_terms = [
        "catalog",
        "search",
        "adoption",
        "adoption_fee_cents",
        "fee",
        "max_results",
        "status",
        "available",
        "pending",
        "test",
        "qa",
        "incident",
    ]
    merged: list[str] = []
    for term in selected + domain_terms:
        if term not in merged:
            merged.append(term)
    return merged[:18]


def search_repo(root: Path, terms: list[str], limit: int = 10) -> list[SearchHit]:
    hits: list[SearchHit] = []
    lowered_terms = [term.lower() for term in terms]
    for path in iter_text_files(root):
        rel = path.relative_to(root)
        if rel.parts[:2] == ("docs", "context-reuse"):
            continue
        if not rel.parts or rel.parts[0] not in {"app", "openspec"}:
            continue
        text = read_text(path)
        lowered = text.lower()
        score = sum(lowered.count(term) for term in lowered_terms)
        if score == 0:
            continue
        snippets: list[str] = []
        for idx, line in enumerate(text.splitlines(), start=1):
            line_lower = line.lower()
            if any(term in line_lower for term in lowered_terms):
                snippets.append(f"L{idx}: {line.strip()[:140]}")
            if len(snippets) == 2:
                break
        hits.append(SearchHit(rel, score, tuple(snippets)))
    hits.sort(key=lambda hit: (hit.score, str(hit.path)), reverse=True)
    return hits[:limit]


def collect_skills(root: Path, labels: tuple[str, ...]) -> list[Path]:
    skill_paths = sorted((root / "skills").glob("*/SKILL.md"))
    label_text = " ".join(labels)
    if "openhands-context" in labels:
        preferred = ["sdlc-context-reuse", "sdlc-story", "sdlc-qa", "sdlc-code-review", "sdlc-incident"]
    elif "openhands-build" in labels or "build" in label_text:
        preferred = ["sdlc-context-reuse", "sdlc-story"]
    elif "openhands-qa" in labels:
        preferred = ["sdlc-context-reuse", "sdlc-qa"]
    elif "openhands-review" in labels:
        preferred = ["sdlc-context-reuse", "sdlc-code-review"]
    elif "openhands-incident" in labels:
        preferred = ["sdlc-context-reuse", "sdlc-incident"]
    else:
        preferred = ["sdlc-context-reuse"]
    by_name = {path.parent.name: path for path in skill_paths}
    return [by_name[name] for name in preferred if name in by_name]


def existing_logs(root: Path) -> list[Path]:
    candidates = [
        root / "docs" / "work-log.md",
        root / "docs" / "tested-demo-flow.md",
        root / "docs" / "qa-reports" / "family-friendly-filter.md",
        root / "docs" / "qa-reports" / "family-friendly-filter-playwright" / "qa-report.md",
        root / "skills" / "sdlc-incident" / "references" / "cloud-run-petstore-incident.md",
    ]
    return [path for path in candidates if path.exists()]


def previous_conversation_sources(root: Path) -> list[Path]:
    candidates = [
        root / "docs" / "repo-memory" / "previous-agent-runs.md",
        root / "docs" / "tested-demo-flow.md",
        root / "docs" / "work-log.md",
    ]
    return [path for path in candidates if path.exists()]


def token_table(paths: list[Path], root: Path) -> list[tuple[str, int]]:
    rows: list[tuple[str, int]] = []
    for path in paths:
        if path.exists():
            rows.append((str(path.relative_to(root)), estimate_tokens(read_text(path))))
    return rows


def repo_token_estimate(root: Path) -> tuple[int, int]:
    files = list(iter_text_files(root))
    total = 0
    for path in files:
        rel = path.relative_to(root)
        if rel.parts[:2] == ("docs", "context-reuse"):
            continue
        total += estimate_tokens(read_text(path))
    return len(files), total


def render_report(root: Path, trigger: TriggerContext) -> str:
    terms = search_terms(trigger)
    hits = search_repo(root, terms)
    skill_paths = collect_skills(root, trigger.labels)
    log_paths = existing_logs(root)
    conversation_paths = previous_conversation_sources(root)
    durable_paths = [
        root / "AGENTS.md",
        root / "docs" / "repo-memory" / "petstore-intelligence.md",
        root / "docs" / "repo-memory" / "model-routing-policy.md",
    ]
    durable_paths = [path for path in durable_paths if path.exists()]

    baseline_file_count, baseline_tokens = repo_token_estimate(root)
    loaded_paths = durable_paths + skill_paths + log_paths + conversation_paths
    loaded_tokens = sum(estimate_tokens(read_text(path)) for path in dict.fromkeys(loaded_paths))
    search_tokens = sum(sum(estimate_tokens(snippet) for snippet in hit.snippets) for hit in hits)
    focused_tokens = loaded_tokens + search_tokens
    avoided_tokens = max(0, baseline_tokens - focused_tokens)

    lines: list[str] = []
    lines.append("# Cost-Aware Context Reuse Report")
    lines.append("")
    lines.append("This report is generated before broad model exploration. It shows which existing context a low-cost scout agent can load, summarize, and hand off to a stronger coding or review agent.")
    lines.append("")
    lines.append("## Trigger")
    lines.append("")
    lines.append(f"- Event: `{trigger.event_type}`")
    if trigger.number is not None:
        lines.append(f"- Item: `#{trigger.number}`")
    if trigger.url:
        lines.append(f"- Source: {trigger.url}")
    lines.append(f"- Title: {trigger.title or '(none)'}")
    if trigger.labels:
        lines.append(f"- Labels: {', '.join(f'`{label}`' for label in trigger.labels)}")
    lines.append("")
    lines.append("## Context Sources Used")
    lines.append("")
    lines.append("### 1. Durable Repo Memory")
    for path, tokens in token_table(durable_paths, root):
        lines.append(f"- `{path}` (~{tokens} tokens): repo rules, product constraints, commands, and reusable architecture notes.")
    lines.append("")
    lines.append("### 2. Skills As Procedural Memory")
    for path, tokens in token_table(skill_paths, root):
        lines.append(f"- `{path}` (~{tokens} tokens): task-specific workflow and stop conditions.")
    lines.append("")
    lines.append("### 3. Existing Logs And Evidence")
    for path, tokens in token_table(log_paths, root):
        lines.append(f"- `{path}` (~{tokens} tokens): prior validation, QA, incident, or operator evidence.")
    lines.append("")
    lines.append("### 4. Targeted GitHub Repo Search")
    lines.append("")
    lines.append(f"Search terms: {', '.join(f'`{term}`' for term in terms[:12])}")
    lines.append("")
    for hit in hits:
        lines.append(f"- `{hit.path}` (score {hit.score})")
        for snippet in hit.snippets:
            lines.append(f"  - {snippet}")
    lines.append("")
    lines.append("### 5. Previous Agent Runs / Conversation Memory")
    for path, tokens in token_table(conversation_paths, root):
        lines.append(f"- `{path}` (~{tokens} tokens): prior OpenHands run IDs, PRs, decisions, and unresolved live-test notes.")
    lines.append("")
    lines.append("## Cost-Aware Model Routing")
    lines.append("")
    lines.append("| Phase | Work | Recommended tier | Why |")
    lines.append("| --- | --- | --- | --- |")
    lines.append("| Preflight | Parse event, labels, repo memory, deterministic search | No LLM or lowest-cost model | Fixed inputs and scripts do most of the work. |")
    lines.append("| Scout | Summarize AGENTS.md, skills, logs, repo hits, prior runs | Low-cost model | Narrow context before expensive reasoning. |")
    lines.append("| Implement | Edit code, update tests, create PR | Coding model | Requires coherent code changes. |")
    lines.append("| Verify | Run tests and summarize evidence | Low-cost or deterministic | Prefer commands and exact output over reasoning. |")
    lines.append("| Risk review | Security, production, or broad-change judgment | Medium/strong model | Escalate only when risk warrants it. |")
    lines.append("")
    lines.append("## Reuse Decisions")
    lines.append("")
    lines.append("- Reuse `AGENTS.md` and repo-memory docs before asking the model to rediscover product rules.")
    lines.append("- Reuse skill procedures instead of restating task workflows in every prompt.")
    lines.append("- Reuse prior QA reports, incident notes, and OpenHands run links before creating new evidence.")
    lines.append("- Search focused code paths first; avoid loading unrelated app, Jira, GCP, and automation files unless the trigger requires them.")
    lines.append("- Preserve durable findings in `docs/repo-memory/`; keep issue-specific details in reports or PRs.")
    lines.append("")
    lines.append("## Token Reuse Estimate")
    lines.append("")
    lines.append(f"- Text files in repo scan: {baseline_file_count}")
    lines.append(f"- Rough full-repo text estimate: ~{baseline_tokens} tokens")
    lines.append(f"- Focused context estimate for this run: ~{focused_tokens} tokens")
    lines.append(f"- Illustrative context avoided before coding: ~{avoided_tokens} tokens")
    lines.append("")
    lines.append("These are rough character-based estimates for live-demo comparison, not billing records. The point is the harness policy: load the known context first, then spend stronger model calls only where they change the outcome.")
    lines.append("")
    lines.append("## Terraform Analogy For The Customer")
    lines.append("")
    lines.append("- `AGENTS.md` becomes Terraform workspace rules, risk policy, module ownership, and approved commands.")
    lines.append("- Skills become module-upgrade, moved-block, and plan-triage procedures.")
    lines.append("- Existing logs become Terraform Cloud plans, previous apply errors, and validation output.")
    lines.append("- GitHub search finds module usage and workspace-specific code paths without reading every repo.")
    lines.append("- Old conversation memory captures what prior agents already learned about a workspace or module family.")
    lines.append("")
    return "\n".join(lines)


def build_report(
    repo_root: Path = REPO_ROOT,
    *,
    fixture: Path | None = None,
    title: str = "Filter pets by max adoption fee",
    body: str = "",
    labels: list[str] | None = None,
) -> str:
    trigger = trigger_from_fixture(fixture) if fixture else trigger_from_args(title, body, labels or ["openhands-context"])
    return render_report(repo_root, trigger)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixture", type=Path, help="GitHub/Jira fixture to use as trigger context")
    parser.add_argument("--title", default="Filter pets by max adoption fee")
    parser.add_argument("--body", default="")
    parser.add_argument("--label", action="append", default=["openhands-context"], help="label for manual demo mode")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--stdout", action="store_true", help="also print the report")
    args = parser.parse_args()

    report = build_report(REPO_ROOT, fixture=args.fixture, title=args.title, body=args.body, labels=args.label)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(report + "\n", encoding="utf-8")
    if args.stdout:
        print(report)
    else:
        try:
            display_path = args.output.relative_to(REPO_ROOT)
        except ValueError:
            display_path = args.output
        print(f"Wrote {display_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
