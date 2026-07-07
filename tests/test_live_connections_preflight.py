from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]


def load_preflight() -> Any:
    script = ROOT / "scripts" / "validation" / "preflight_live_connections.py"
    spec = importlib.util.spec_from_file_location("preflight_live_connections", script)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_main_mode_requires_basic_jira_enabled_and_sidekick_disabled() -> None:
    module = load_preflight()
    ids = module.DEFAULT_AUTOMATION_IDS
    automations = [
        {
            "id": ids.jira_main,
            "name": "Jira main",
            "enabled": True,
            "model": "Bedrock-Claude-Sonnet-4-5-fast",
        },
        {
            "id": ids.jira_sidekick_v2,
            "name": "Jira sidekick v2",
            "enabled": False,
            "model": "Bedrock-Claude-Sonnet-4-5-fast",
        },
        {
            "id": ids.github_qa,
            "name": "GitHub QA",
            "enabled": True,
            "model": "Bedrock-Claude-Sonnet-4-5-fast",
        },
    ]

    assert module.validate_automation_states(automations, "main", ids) == []


def test_sidekick_v2_mode_catches_basic_jira_still_enabled() -> None:
    module = load_preflight()
    ids = module.DEFAULT_AUTOMATION_IDS
    automations = [
        {
            "id": ids.jira_main,
            "name": "Jira main",
            "enabled": True,
            "model": "Bedrock-Claude-Sonnet-4-5-fast",
        },
        {
            "id": ids.jira_sidekick_v2,
            "name": "Jira sidekick v2",
            "enabled": True,
            "model": "Bedrock-Claude-Sonnet-4-5-fast",
        },
        {
            "id": ids.github_qa,
            "name": "GitHub QA",
            "enabled": True,
            "model": "Bedrock-Claude-Sonnet-4-5-fast",
        },
    ]

    failures = module.validate_automation_states(
        automations,
        "sidekick-v2",
        ids,
    )

    assert "Jira main should be disabled" in failures


def test_sidekick_v2_mode_keeps_label_gated_v2_enabled() -> None:
    module = load_preflight()
    ids = module.DEFAULT_AUTOMATION_IDS
    automations = [
        {
            "id": ids.jira_main,
            "name": "Jira main",
            "enabled": False,
            "model": "Bedrock-Claude-Sonnet-4-5-fast",
        },
        {
            "id": ids.jira_sidekick_v2,
            "name": "Jira sidekick v2",
            "enabled": True,
            "model": "Bedrock-Claude-Sonnet-4-5-fast",
        },
        {
            "id": ids.github_qa,
            "name": "GitHub QA",
            "enabled": True,
            "model": "Bedrock-Claude-Sonnet-4-5-fast",
        },
    ]

    assert module.validate_automation_states(automations, "sidekick-v2", ids) == []


def test_jira_permission_validation_requires_add_comments() -> None:
    module = load_preflight()
    payload = {
        "permissions": {
            "BROWSE_PROJECTS": {"havePermission": True},
            "CREATE_ISSUES": {"havePermission": True},
            "ADD_COMMENTS": {"havePermission": False},
        }
    }

    assert module.validate_jira_permissions(payload) == [
        "Jira token cannot post PR/status comments back to Jira (ADD_COMMENTS)"
    ]


def test_openhands_auth_headers_are_split_by_api_family() -> None:
    module = load_preflight()

    assert module.automation_headers("demo-key") == {
        "Authorization": "Bearer demo-key",
    }
    assert module.app_headers("demo-key") == {
        "X-Access-Token": "demo-key",
    }


def test_live_preflight_requires_runtime_github_token(monkeypatch) -> None:
    module = load_preflight()
    for key, value in {
        "OPENHANDS_HOST": "https://example.invalid",
        "OPENHANDS_API_KEY_ORG": "demo",
        "JIRA_API_BASE_URL": "https://jira.example.invalid",
        "JIRA_API_TOKEN": "demo",
        "JIRA_SITE_URL": "https://jira.example.invalid",
        "JIRA_DEMO_PROJECT_KEY": "KAN",
        "GITHUB_DEMO_REPOSITORY": "rajshah4/sdlc-automation-github-demo",
        "GITHUB_DEMO_REPO_URL": "https://github.com/rajshah4/sdlc-automation-github-demo",
    }.items():
        monkeypatch.setenv(key, value)
    monkeypatch.delenv("GITHUB_TOKEN", raising=False)

    failures: list[str] = []
    module.check_env(failures)

    assert "missing env names: GITHUB_TOKEN" in failures
