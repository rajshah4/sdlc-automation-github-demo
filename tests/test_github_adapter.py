from __future__ import annotations

import json
from pathlib import Path

from providers.github.adapter import (
    normalize_issue_comment,
    normalize_issues_event,
    normalize_pull_request_event,
)


FIXTURES = Path(__file__).resolve().parents[1] / "fixtures"


def load_fixture(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def test_issue_comment_build_trigger_normalizes_sparse_issue() -> None:
    event = normalize_issue_comment(load_fixture("github_issue_comment_build.json"))

    assert event.provider == "github"
    assert event.event_type == "issue_comment.created"
    assert event.trigger.name == "openhands-build"
    assert event.issue is not None
    assert event.issue.number == 7
    assert event.pull_request is None


def test_pull_request_label_qa_trigger_normalizes_pr() -> None:
    event = normalize_pull_request_event(load_fixture("github_pr_labeled_qa.json"))

    assert event.trigger.name == "openhands-qa"
    assert event.pull_request is not None
    assert event.pull_request.source_branch == "openhands/issue-7-max-fee"
    assert event.pull_request.target_branch == "main"


def test_issue_label_incident_trigger_normalizes_issue() -> None:
    event = normalize_issues_event(load_fixture("github_issue_labeled_incident.json"))

    assert event.trigger.name == "openhands-incident"
    assert event.issue is not None
    assert "type:incident" in event.issue.labels

