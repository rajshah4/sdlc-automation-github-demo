from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]


def load_preflight() -> Any:
    script = ROOT / "scripts" / "preflight_live_connections.py"
    spec = importlib.util.spec_from_file_location("preflight_live_connections", script)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_main_mode_requires_broad_jira_enabled_and_experiments_disabled() -> None:
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
            "id": ids.jira_control,
            "name": "Jira control",
            "enabled": False,
            "model": "Bedrock-Claude-Sonnet-4-5",
        },
        {
            "id": ids.jira_sidekick,
            "name": "Jira sidekick",
            "enabled": False,
            "model": "Bedrock-Claude-Sonnet-4-5",
        },
        {
            "id": ids.github_qa,
            "name": "GitHub QA",
            "enabled": True,
            "model": "Bedrock-Claude-Sonnet-4-5-fast",
        },
    ]

    assert module.validate_automation_states(automations, "main", ids) == []


def test_sidekick_mode_catches_broad_jira_still_enabled() -> None:
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
            "id": ids.jira_control,
            "name": "Jira control",
            "enabled": True,
            "model": "Bedrock-Claude-Sonnet-4-5",
        },
        {
            "id": ids.jira_sidekick,
            "name": "Jira sidekick",
            "enabled": True,
            "model": "Bedrock-Claude-Sonnet-4-5",
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
        "sidekick-experiment",
        ids,
    )

    assert "Jira main should be disabled" in failures


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
