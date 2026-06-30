from __future__ import annotations

import importlib.util
import sys
from argparse import Namespace
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts" / "launch_sidekick_v2.py"


def load_module():
    spec = importlib.util.spec_from_file_location("launch_sidekick_v2", SCRIPT_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def demo_args():
    return Namespace(
        repository="rajshah4/sdlc-automation-github-demo",
        branch="sidekick-context-experiment",
        scout_model="Bedrock-Claude-Sonnet-4-5-fast",
        main_model="Bedrock-Claude-Sonnet-4-5",
    )


def demo_ticket(module):
    return module.Ticket(
        key="KAN-123",
        url="https://rajiv-shah.atlassian.net/browse/KAN-123",
        title="Available pets list still shows unavailable animals",
        body="Customers say the available pets page includes animals that should not be adoptable.",
    )


def test_dry_run_builds_visible_parent_and_child_scouts() -> None:
    module = load_module()
    payloads = module.dry_run_payloads(demo_ticket(module), demo_args())

    assert payloads["parent"]["initial_message"]["run"] is False
    assert len(payloads["scouts"]) == 3
    assert {payload["title"].split()[-1] for payload in payloads["scouts"]} == {
        "docs-scout",
        "logs-scout",
        "repo-scout",
    }
    for payload in payloads["scouts"]:
        assert payload["parent_conversation_id"] == "<parent-conversation-id>"
        assert payload["initial_message"]["run"] is True
        assert payload["plugins"] == []
        assert payload["selected_repository"] == "rajshah4/sdlc-automation-github-demo"
        assert payload["selected_branch"] == "sidekick-context-experiment"


def test_scout_prompts_are_read_only_and_bounded() -> None:
    module = load_module()
    ticket = demo_ticket(module)

    for scout in module.SCOUTS:
        prompt = module.scout_prompt(scout, ticket)
        assert f"SCOUT_RESULT {scout.name}" in prompt
        assert "Read only" in prompt
        assert "Do not change files or external systems" in prompt
        assert "Use at most four search/read commands total" in prompt
        assert "Do not load workflow skills" in prompt
        assert "pull request" not in prompt.lower()
        assert "commit" not in prompt.lower()


def test_main_prompt_consumes_scout_results_and_triggers_qa_label() -> None:
    module = load_module()
    ticket = demo_ticket(module)
    scout = module.ConversationResult(
        name="docs-scout",
        conversation_id="abc",
        conversation_url="https://app.replicated.rajistics.com/conversations/abc",
        start_task_id="task",
        start_status="READY",
        execution_status="finished",
        started_at="2026-06-30T00:00:00+00:00",
        ready_at="2026-06-30T00:00:05+00:00",
        finished_at="2026-06-30T00:00:20+00:00",
        elapsed_to_ready_seconds=5.0,
        elapsed_to_finished_seconds=20.0,
        output="SCOUT_RESULT docs-scout\nCONFIDENCE:\n- high",
    )

    prompt = module.main_prompt(ticket, [scout])

    assert "Do not repeat a broad" in prompt
    assert "SCOUT_RESULT docs-scout" in prompt
    assert "skills/sdlc-story/SKILL.md" in prompt
    assert "openhands-qa" in prompt
    assert "Open a GitHub pull request" in prompt
