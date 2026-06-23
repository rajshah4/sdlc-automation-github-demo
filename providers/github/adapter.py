"""GitHub payload normalization helpers."""

from __future__ import annotations

import re
from typing import Any

from providers.common.normalized_event import (
    CommentRef,
    IssueRef,
    NormalizedEvent,
    PullRequestRef,
    RepositoryRef,
    TriggerRef,
)


TRIGGER_RE = re.compile(r"\b(openhands-[a-z0-9-]+)\b(?P<args>.*)", re.IGNORECASE)
AUTOMATION_LABELS = {
    "openhands-build",
    "openhands-review",
    "openhands-qa",
    "openhands-incident",
}
STATUS_LABEL_PREFIX = "openhands:"


def extract_trigger(comment_body: str) -> TriggerRef | None:
    match = TRIGGER_RE.search(comment_body or "")
    if not match:
        return None
    return TriggerRef(
        name=match.group(1).lower(),
        arguments=match.group("args").strip(),
        raw=match.group(0).strip(),
    )


def label_names(labels: list[dict[str, Any]] | None) -> list[str]:
    return [label.get("name", "") for label in labels or [] if label.get("name")]


def trigger_from_label(label_name: str | None) -> TriggerRef | None:
    if not label_name:
        return None
    normalized = label_name.lower()
    if normalized in AUTOMATION_LABELS:
        return TriggerRef(name=normalized, raw=label_name)
    return None


def repository_ref(payload: dict[str, Any]) -> RepositoryRef:
    repo = payload.get("repository", {})
    return RepositoryRef(
        id=str(repo.get("id")) if repo.get("id") is not None else None,
        name=repo.get("name", ""),
        full_name=repo.get("full_name"),
        clone_url=repo.get("clone_url"),
        web_url=repo.get("html_url"),
    )


def issue_ref(issue: dict[str, Any]) -> IssueRef:
    return IssueRef(
        id=issue.get("id") or issue.get("number"),
        number=issue.get("number"),
        title=issue.get("title"),
        url=issue.get("html_url"),
        labels=label_names(issue.get("labels")),
    )


def pull_request_ref(pr: dict[str, Any]) -> PullRequestRef:
    return PullRequestRef(
        id=pr.get("id") or pr.get("number"),
        number=pr.get("number"),
        title=pr.get("title"),
        source_branch=((pr.get("head") or {}).get("ref")),
        target_branch=((pr.get("base") or {}).get("ref")),
        url=pr.get("html_url"),
    )


def normalize_issue_comment(payload: dict[str, Any]) -> NormalizedEvent:
    """Normalize a GitHub issue_comment payload for issue and PR comments."""
    repo = payload.get("repository", {})
    issue = payload.get("issue", {})
    comment = payload.get("comment", {})
    body = comment.get("body", "") or ""
    trigger = extract_trigger(body) or TriggerRef(name="unknown", raw=body)
    pr_ref = None
    if issue.get("pull_request"):
        pr_ref = PullRequestRef(
            id=issue.get("number"),
            number=issue.get("number"),
            title=issue.get("title"),
            url=issue.get("html_url"),
        )

    return NormalizedEvent(
        provider="github",
        event_type=f"issue_comment.{payload.get('action', 'created')}",
        organization=(repo.get("owner") or {}).get("login"),
        repository=repository_ref(payload),
        issue=issue_ref(issue),
        pull_request=pr_ref,
        comment=CommentRef(
            id=comment.get("id"),
            author=(comment.get("user") or {}).get("login"),
            body=body,
            url=comment.get("html_url"),
        ),
        trigger=trigger,
        raw_event=payload,
    )


def normalize_issues_event(payload: dict[str, Any]) -> NormalizedEvent:
    """Normalize GitHub issue events, including label-triggered work cells."""
    issue = payload.get("issue", {})
    label = payload.get("label", {})
    trigger = trigger_from_label(label.get("name")) or TriggerRef(name="unknown", raw=label.get("name"))
    repo = payload.get("repository", {})
    return NormalizedEvent(
        provider="github",
        event_type=f"issues.{payload.get('action', 'unknown')}",
        organization=(repo.get("owner") or {}).get("login"),
        repository=repository_ref(payload),
        issue=issue_ref(issue),
        trigger=trigger,
        raw_event=payload,
    )


def normalize_pull_request_event(payload: dict[str, Any]) -> NormalizedEvent:
    """Normalize GitHub pull_request events, including label-triggered PR work cells."""
    pr = payload.get("pull_request", {})
    label = payload.get("label", {})
    trigger = trigger_from_label(label.get("name")) or TriggerRef(name="unknown", raw=label.get("name"))
    repo = payload.get("repository", {})
    return NormalizedEvent(
        provider="github",
        event_type=f"pull_request.{payload.get('action', 'unknown')}",
        organization=(repo.get("owner") or {}).get("login"),
        repository=repository_ref(payload),
        pull_request=pull_request_ref(pr),
        trigger=trigger,
        raw_event=payload,
    )
