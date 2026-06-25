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


def test_issue_label_build_fixture_is_sparse_story() -> None:
    payload = load_fixture("github_issue_labeled_build.json")

    assert payload["_event_name"] == "issues"
    assert payload["action"] == "labeled"
    assert payload["label"]["name"] == "openhands-build"
    assert payload["issue"]["number"] == 7
    assert payload["issue"]["title"] == "Filter pets by max adoption fee"


def test_pull_request_label_qa_fixture_is_pr_event() -> None:
    payload = load_fixture("github_pr_labeled_qa.json")

    assert payload["_event_name"] == "pull_request"
    assert payload["label"]["name"] == "openhands-qa"
    assert payload["pull_request"]["head"]["ref"] == "openhands/issue-7-max-fee"
    assert payload["pull_request"]["base"]["ref"] == "main"


def test_issue_label_incident_fixture_is_incident_event() -> None:
    payload = load_fixture("github_issue_labeled_incident.json")

    assert payload["_event_name"] == "issues"
    assert payload["label"]["name"] == "openhands-incident"
    assert "type:incident" in {label["name"] for label in payload["issue"]["labels"]}


def test_all_fixtures_use_known_automation_labels() -> None:
    for path in FIXTURES.glob("github_*.json"):
        payload = load_fixture(path.name)
        assert payload["label"]["name"] in AUTOMATION_LABELS


def test_jira_comment_fixture_targets_build_automation() -> None:
    payload = load_fixture("jira_comment_created_build.json")

    assert payload["webhookEvent"] == "comment_created"
    assert payload["source"] == "jira-automation"
    assert payload["projectKey"] == "KAN"
    assert payload["issueKey"].startswith("KAN-")


def test_jira_direct_fixture_uses_sparse_business_language() -> None:
    payload = load_fixture("jira_issue_created_budget_story.json")

    assert payload["webhookEvent"] == "jira:issue_created"
    assert payload["issue"]["fields"]["project"]["key"] == "KAN"
    assert payload["issue"]["fields"]["issuetype"]["name"] == "Task"
    assert payload["issue"]["fields"]["summary"] == "Families need to find pets in their budget"
    assert "pet-search-budget-limit.ndjson" in {
        attachment["filename"] for attachment in payload["issue"]["fields"]["attachment"]
    }


def test_jira_direct_needs_human_fixture_is_intentionally_ambiguous() -> None:
    payload = load_fixture("jira_issue_created_needs_human.json")

    assert payload["webhookEvent"] == "jira:issue_created"
    assert payload["issue"]["fields"]["summary"] == "People are confused by pet prices"
    assert "needs-clarification" in payload["issue"]["fields"]["labels"]
