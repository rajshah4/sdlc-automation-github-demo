#!/usr/bin/env python3
"""Build a cost-aware context reuse brief for the SDLC Automation Demo.

This script is intentionally deterministic: it reads repo-local memory,
skills, prior evidence, and targeted search results before any LLM reasoning is
needed. The resulting brief is a live-demo artifact that gives the next work
cell the issue-specific information it needs without exposing a search
transcript.
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
        "before",
        "can",
        "context",
        "cost",
        "customers",
        "even",
        "evidence",
        "for",
        "from",
        "implementation",
        "issue",
        "label",
        "learned",
        "list",
        "logs",
        "memory",
        "mention",
        "not",
        "open",
        "openhands-context",
        "openhands",
        "pet",
        "pets",
        "please",
        "prior",
        "reduce",
        "repo",
        "reuse",
        "run",
        "says",
        "scout",
        "seeing",
        "she",
        "should",
        "showing",
        "source",
        "support",
        "targeted",
        "that",
        "the",
        "though",
        "this",
        "token",
        "type",
        "bug",
        "want",
        "with",
    }
    selected = [word for word in words if word not in stop]
    domain_terms: list[str] = []
    if any(term in raw for term in ("pending", "unavailable", "not available", "pending_pet_visible")):
        domain_terms.extend(
            [
                "pending_pet_visible",
                "bad_catalog_filter",
                "visible_pets",
                "nova",
                "pending",
                "available",
                "status",
                "catalog",
                "search",
                "test",
            ]
        )
    elif any(term in raw for term in ("fee", "adoption fee", "max adoption", "budget")):
        domain_terms.extend(
            [
                "adoption_fee_cents",
                "fee",
                "max",
                "catalog",
                "search",
                "available",
                "test",
            ]
        )
    if not domain_terms:
        domain_terms.extend(["catalog", "search", "adoption", "status", "available", "test"])
    domain_terms.append("qa")
    merged: list[str] = []
    for term in domain_terms + selected:
        if term not in merged:
            merged.append(term)
    return merged[:24]


def term_weight(term: str) -> int:
    weights = {
        "pending_pet_visible": 12,
        "bad_catalog_filter": 10,
        "visible_pets": 10,
        "nova": 8,
        "pending": 6,
        "available": 4,
        "status": 4,
        "adoption_fee_cents": 8,
    }
    return weights.get(term, 2 if len(term) > 4 else 1)


def is_boilerplate_snippet(line: str) -> bool:
    stripped = line.strip()
    if not stripped:
        return True
    lowered = stripped.lower()
    if lowered.startswith(("from __future__", "import ", "from ", "#!", "try:", "except ", "catch ")):
        return True
    if lowered.startswith("console.error("):
        return True
    return stripped in {"{", "}", "(", ")", ");", "};"}


def ranked_snippets(text: str, terms: list[str], limit: int = 2) -> tuple[str, ...]:
    candidates: list[tuple[int, int, str]] = []
    for idx, line in enumerate(text.splitlines(), start=1):
        line_lower = line.lower()
        if not any(term in line_lower for term in terms):
            continue
        if is_boilerplate_snippet(line):
            continue
        score = sum(line_lower.count(term) * term_weight(term) for term in terms)
        if any(marker in line_lower for marker in ("assert", "def ", "return ", "error_code")):
            score += 4
        if any(marker in line_lower for marker in ("pet.status", "===", "!=", " continue")):
            score += 4
        if "excludes_pending_by_default" in line_lower or ('"nova" not in' in line_lower):
            score += 12
        if any(marker in line_lower for marker in ("pending", "available", "nova", "visible_pets")):
            score += 3
        candidates.append((score, idx, line.strip()[:140]))

    candidates.sort(key=lambda item: (item[0], -item[1]), reverse=True)
    selected = sorted(candidates[:limit], key=lambda item: item[1])
    return tuple(f"L{idx}: {line}" for _, idx, line in selected)


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
        path_text = str(rel).lower()
        score = sum((lowered.count(term) + path_text.count(term)) * term_weight(term) for term in lowered_terms)
        if score == 0:
            continue
        snippets = ranked_snippets(text, lowered_terms)
        hits.append(SearchHit(rel, score, snippets))
    hits.sort(key=lambda hit: (hit.score, str(hit.path)), reverse=True)
    return hits[:limit]


def issue_need(trigger: TriggerContext) -> str:
    raw = " ".join([trigger.title, trigger.body, " ".join(trigger.labels)]).lower()
    if any(term in raw for term in ("pending", "unavailable", "not available", "pending_pet_visible")):
        return (
            "Investigate why a pending or unavailable pet is appearing in the "
            "available-pets experience, then preserve the default available-only "
            "catalog behavior."
        )
    if any(term in raw for term in ("fee", "adoption fee", "max adoption", "budget")):
        return (
            "Implement or validate an adoption-fee filter while preserving the "
            "repo rule that money is represented as integer cents."
        )
    return "Clarify and implement the smallest safe Petstore change implied by the issue."


def product_facts(trigger: TriggerContext) -> list[tuple[str, tuple[str, ...]]]:
    raw = " ".join([trigger.title, trigger.body, " ".join(trigger.labels)]).lower()
    facts: list[tuple[str, tuple[str, ...]]] = [
        (
            "Humans approve scope, PR review, merge, deployment, and risky follow-up decisions.",
            ("AGENTS.md", "docs/repo-memory/petstore-intelligence.md"),
        ),
    ]
    if any(term in raw for term in ("pending", "unavailable", "available", "pending_pet_visible")):
        facts.insert(
            0,
            (
                "Default pet search returns only available pets.",
                ("AGENTS.md", "docs/repo-memory/petstore-intelligence.md"),
            ),
        )
        facts.insert(
            1,
            (
                "Pending pets can be shown only when explicitly requested and cannot be adopted.",
                ("AGENTS.md", "docs/repo-memory/petstore-intelligence.md"),
            ),
        )
    if any(term in raw for term in ("fee", "adoption", "money", "cents", "budget")):
        facts.append(
            (
                "Money is represented as integer cents.",
                ("AGENTS.md", "docs/repo-memory/petstore-intelligence.md"),
            )
        )
    if any(term in raw for term in ("ui", "browser", "show", "visible", "page", "list")):
        facts.append(
            (
                "UI-visible changes need UI evidence, not only backend tests.",
                ("AGENTS.md", "docs/repo-memory/petstore-intelligence.md"),
            )
        )
    return facts


def path_hint(path: Path) -> str:
    text = str(path)
    hints = {
        "app/petstore_app/catalog.py": "catalog search, status, fee, and availability behavior",
        "app/tests/test_pet_catalog.py": "focused catalog regression tests",
        "app/petstore_app/adoptions.py": "adoption validation and pending-pet safety",
        "app/tests/test_adoptions.py": "adoption behavior tests",
        "app/web/app.js": "static UI catalog filter",
        "app/web/tests/catalog-search.playwright.mjs": "browser evidence pattern for catalog UI changes",
    }
    for known, hint in hints.items():
        if text == known:
            return hint
    if text.startswith("app/web/"):
        return "static UI surface or browser evidence path"
    if text.startswith("openspec/"):
        return "OpenSpec-style change artifact"
    return "potentially relevant repo context"


def likely_paths(hits: list[SearchHit], limit: int = 6) -> list[Path]:
    preferred = [
        Path("app/petstore_app/catalog.py"),
        Path("app/tests/test_pet_catalog.py"),
        Path("app/web/app.js"),
        Path("app/web/tests/catalog-search.playwright.mjs"),
    ]
    hit_paths = [hit.path for hit in hits]
    ordered: list[Path] = []
    for path in preferred + hit_paths:
        if path in hit_paths and path not in ordered:
            ordered.append(path)
        if len(ordered) >= limit:
            break
    return ordered


def short_body(body: str, limit: int = 280) -> str:
    normalized = " ".join(body.split())
    if len(normalized) <= limit:
        return normalized or "(none)"
    return normalized[: limit - 1].rstrip() + "..."


def cite(sources: tuple[str, ...]) -> str:
    return "Sources: " + ", ".join(f"`{source}`" for source in sources)


def hit_lookup(hits: list[SearchHit]) -> dict[Path, SearchHit]:
    return {hit.path: hit for hit in hits}


def snippets_for(path: Path, hits: list[SearchHit]) -> tuple[str, ...]:
    hit = hit_lookup(hits).get(path)
    if not hit or not hit.snippets:
        return ()
    return hit.snippets


def pr_decision(trigger: TriggerContext) -> list[str]:
    raw = " ".join([trigger.title, trigger.body, " ".join(trigger.labels)]).lower()
    if any(term in raw for term in ("pending", "unavailable", "not available", "pending_pet_visible")):
        return [
            "First check whether existing catalog code and tests already exclude pending pets from the default available-pets path.",
            "If existing code and tests already prove the behavior, do not open a code PR; post evidence and mark the issue complete or ask for the missing reproduction.",
            "If the issue reproduces, or if the regression test is missing, open a PR with a focused catalog fix and regression test.",
        ]
    if any(term in raw for term in ("fee", "adoption fee", "max adoption", "budget")):
        return [
            "First check whether the API, UI, and tests already support the requested max adoption fee behavior.",
            "If existing code already implements it, do not open a code PR; post the evidence and any usage guidance the issue needs.",
            "If the behavior is missing or uncovered, open a PR with the smallest API/UI/test change.",
        ]
    return [
        "First check whether existing code and tests already satisfy the issue.",
        "Open a PR only when behavior is missing, broken, or lacks the evidence needed for review.",
        "If existing code is sufficient, post the evidence and ask for clarification only when acceptance criteria are still ambiguous.",
    ]


def collect_skills(root: Path, labels: tuple[str, ...]) -> list[Path]:
    skill_paths = sorted((root / "skills").glob("*/SKILL.md"))
    label_text = " ".join(labels)
    if "openhands-context" in labels:
        preferred = ["sdlc-context-reuse", "sdlc-story", "sdlc-qa", "sdlc-code-review"]
    elif "openhands-build" in labels or "build" in label_text:
        preferred = ["sdlc-context-reuse", "sdlc-story"]
    elif "openhands-qa" in labels:
        preferred = ["sdlc-context-reuse", "sdlc-qa"]
    elif "openhands-review" in labels:
        preferred = ["sdlc-context-reuse", "sdlc-code-review"]
    else:
        preferred = ["sdlc-context-reuse"]
    by_name = {path.parent.name: path for path in skill_paths}
    return [by_name[name] for name in preferred if name in by_name]


def existing_logs(root: Path) -> list[Path]:
    candidates = [
        root / "docs" / "qa-reports" / "family-friendly-filter.md",
        root / "docs" / "qa-reports" / "family-friendly-filter-playwright" / "qa-report.md",
    ]
    return [path for path in candidates if path.exists()]


def previous_conversation_sources(root: Path) -> list[Path]:
    candidates = [
        root / "docs" / "repo-memory" / "previous-agent-runs.md",
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
    handoff_paths = likely_paths(hits)

    lines.append("# Context Scout Issue Brief")
    lines.append("")
    lines.append("This brief turns the issue into the context the next OpenHands work cell needs. The scout uses repo memory, skills, prior evidence, and targeted search internally; the visible output stays focused on the decision and handoff.")
    lines.append("")
    lines.append("## Issue")
    lines.append("")
    lines.append(f"- Event: `{trigger.event_type}`")
    if trigger.number is not None:
        lines.append(f"- Item: `#{trigger.number}`")
    if trigger.url:
        lines.append(f"- Source: {trigger.url}")
    lines.append(f"- Title: {trigger.title or '(none)'}")
    if trigger.labels:
        lines.append(f"- Labels: {', '.join(f'`{label}`' for label in trigger.labels)}")
    lines.append(f"- Body signal: {short_body(trigger.body)}")
    lines.append("")
    lines.append("## What The Issue Needs")
    lines.append("")
    lines.append(f"- {issue_need(trigger)}")
    lines.append(f"- Learned from: issue title/body, `AGENTS.md`, and `docs/repo-memory/petstore-intelligence.md`.")
    lines.append("- Treat the issue and its comments as the source of truth; ask a human only if scope, credentials, or production action is unclear.")
    lines.append("")
    lines.append("## Relevant Product Context")
    lines.append("")
    for fact, sources in product_facts(trigger):
        lines.append(f"- {fact} ({cite(sources)})")
    lines.append("")
    lines.append("## Existing Code Or New PR?")
    lines.append("")
    for decision in pr_decision(trigger):
        lines.append(f"- {decision}")
    lines.append("")
    lines.append("## Likely Files And Tests")
    lines.append("")
    for path in handoff_paths:
        lines.append(f"- `{path}`: {path_hint(path)}. (Sources: `docs/repo-memory/petstore-intelligence.md`, targeted repo search)")
    if not handoff_paths:
        lines.append("- No narrow file target found from deterministic search; start with `docs/repo-memory/petstore-intelligence.md` and the relevant skill.")
    lines.append("")
    lines.append("## Cited Handoff Material")
    lines.append("")
    lines.append("- Issue source: title/body/comments on the GitHub issue remain the source of truth.")
    for path in handoff_paths:
        for snippet in snippets_for(path, hits):
            lines.append(f"- `{path}`: {snippet}")
    lines.append("- Memory source: `docs/repo-memory/previous-agent-runs.md` for prior lessons and reusable file-path hints.")
    lines.append("")
    lines.append("## Reusable Memory")
    lines.append("")
    lines.append("- `AGENTS.md` and `docs/repo-memory/petstore-intelligence.md` provide product rules and app map.")
    if skill_paths:
        lines.append("- Use `skills/sdlc-context-reuse/SKILL.md` first, then the specific build, QA, or review skill required by the next label.")
    if log_paths:
        lines.append("- Existing QA evidence is available for style and safety checks; summarize only the parts relevant to this issue.")
    if conversation_paths:
        lines.append("- `docs/repo-memory/previous-agent-runs.md` captures prior lessons so the next agent does not rediscover file paths and demo guardrails.")
    lines.append("")
    lines.append("## Recommended Next Steps")
    lines.append("")
    lines.append("- If focused tests prove existing behavior already satisfies the issue, post evidence instead of opening a PR.")
    lines.append("- Apply `openhands-build` only when reproduction or missing coverage shows a code change is needed.")
    lines.append("- Run focused tests before broad QA; start with `python3 -m pytest -q` and the relevant Petstore test file.")
    lines.append("- Apply `openhands-qa` on the PR if behavior is UI-visible or needs additional evidence.")
    lines.append("- Keep production, deployment, and merge decisions with humans.")
    lines.append("")
    lines.append("## Cost Routing")
    lines.append("")
    lines.append("- Scout/context summary: lower-cost model or deterministic script.")
    lines.append("- Code edits and risk-sensitive reasoning: coding model.")
    lines.append("- Verification summaries: deterministic commands or lower-cost model.")
    lines.append(f"- Approximate context avoided before coding: ~{avoided_tokens} tokens.")
    lines.append("")
    lines.append("Exhaustive search provenance is intentionally omitted. The cited material above is the handoff raw material for deciding whether to open a PR and for drafting that PR if needed.")
    lines.append("")
    return "\n".join(lines)


def build_report(
    repo_root: Path = REPO_ROOT,
    *,
    fixture: Path | None = None,
    title: str = "Customers are seeing pets that are not available",
    body: str = "",
    labels: list[str] | None = None,
) -> str:
    trigger = trigger_from_fixture(fixture) if fixture else trigger_from_args(title, body, labels or ["openhands-context"])
    return render_report(repo_root, trigger)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixture", type=Path, help="GitHub/Jira fixture to use as trigger context")
    parser.add_argument("--title", default="Customers are seeing pets that are not available")
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
