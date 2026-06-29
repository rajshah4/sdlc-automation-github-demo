from __future__ import annotations

import json
from pathlib import Path


FIXTURES = Path(__file__).resolve().parent / "fixtures"
AUTOMATION_LABELS = {
    "openhands-build",
    "openhands-review",
    "openhands-qa",
    "openhands-incident",
}


def load_fixture(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def test_issue_label_build_fixture_is_sparse_bug() -> None:
    payload = load_fixture("github_issue_labeled_build.json")

    assert payload["_event_name"] == "issues"
    assert payload["action"] == "labeled"
    assert payload["label"]["name"] == "openhands-build"
    assert payload["issue"]["number"] == 7
    assert payload["issue"]["title"] == "Customers are seeing pets that are not available"
    assert "type:bug" in {label["name"] for label in payload["issue"]["labels"]}


def test_pull_request_label_qa_fixture_is_pr_event() -> None:
    payload = load_fixture("github_pr_labeled_qa.json")

    assert payload["_event_name"] == "pull_request"
    assert payload["label"]["name"] == "openhands-qa"
    assert payload["pull_request"]["head"]["ref"] == "openhands/issue-7-pending-pet-visibility"
    assert payload["pull_request"]["base"]["ref"] == "main"


def test_issue_label_incident_fixture_is_incident_event() -> None:
    payload = load_fixture("github_issue_labeled_incident.json")

    assert payload["_event_name"] == "issues"
    assert payload["label"]["name"] == "openhands-incident"
    assert "type:incident" in {label["name"] for label in payload["issue"]["labels"]}


def test_all_fixtures_use_known_automation_labels() -> None:
    for path in FIXTURES.glob("*.json"):
        payload = load_fixture(path.name)
        assert payload["label"]["name"] in AUTOMATION_LABELS
