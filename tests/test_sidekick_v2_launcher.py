from __future__ import annotations

import importlib.util
import sys
from argparse import Namespace
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts" / "sidekick" / "launch_sidekick_v2.py"


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
        branch="main",
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


def test_dry_run_builds_top_level_scouts_and_main() -> None:
    module = load_module()
    payloads = module.dry_run_payloads(demo_ticket(module), demo_args())

    assert payloads["conversation_layout"] == "top-level"
    assert "parent" not in payloads
    assert len(payloads["scouts"]) == 3
    assert {payload["title"] for payload in payloads["scouts"]} == {
        "Step 2A - Docs Context Scout (KAN-123)",
        "Step 2B - Logs Context Scout (KAN-123)",
        "Step 2C - Repo Context Scout (KAN-123)",
    }
    for payload in payloads["scouts"]:
        assert "parent_conversation_id" not in payload
        assert payload["initial_message"]["run"] is True
        assert payload["plugins"] == []
        assert payload["selected_repository"] == "rajshah4/sdlc-automation-github-demo"
        assert payload["selected_branch"] == "main"
        prompt = payload["initial_message"]["content"][0]["text"]
        assert "DEMO_STEP 2" in prompt
        assert "SCOUT_RESULT" in prompt
    assert payloads["main"]["title"] == "Step 3 - Implement Fix and Open PR (KAN-123)"
    assert "parent_conversation_id" not in payloads["main"]


def test_app_conversation_headers_use_access_token_only(monkeypatch) -> None:
    module = load_module()
    monkeypatch.setenv("OPENHANDS_API_KEY_ORG", "demo-key")

    headers = module.app_headers()

    assert headers == {
        "X-Access-Token": "demo-key",
        "Accept": "application/json",
    }
    assert "Authorization" not in headers


def test_github_token_waits_for_runtime_secret(monkeypatch) -> None:
    module = load_module()
    calls = {"sleep": 0}

    monkeypatch.delenv("GITHUB_TOKEN", raising=False)
    monkeypatch.setenv("SIDEKICK_SECRET_WAIT_SECONDS", "3")
    monkeypatch.setattr(module.time, "monotonic", lambda: float(calls["sleep"]))

    def fake_sleep(_seconds: float) -> None:
        calls["sleep"] += 1
        monkeypatch.setenv("GITHUB_TOKEN", "demo-token")

    monkeypatch.setattr(module.time, "sleep", fake_sleep)

    assert module.github_token() == "demo-token"
    assert calls["sleep"] == 1


def test_github_token_fails_without_runtime_secret(monkeypatch) -> None:
    module = load_module()
    monkeypatch.delenv("GITHUB_TOKEN", raising=False)
    monkeypatch.setenv("SIDEKICK_SECRET_WAIT_SECONDS", "0")

    with pytest.raises(SystemExit, match="Missing required setting: GITHUB_TOKEN"):
        module.github_token()


def test_scout_prompts_are_read_only_and_bounded() -> None:
    module = load_module()
    ticket = demo_ticket(module)

    for scout in module.SCOUTS:
        prompt = module.scout_prompt(scout, ticket)
        step, label = module.scout_step(scout.name)
        assert f"DEMO_STEP {step}: {label}" in prompt
        assert f"DEMO_STEP {step} COMPLETE: {label}" in prompt
        assert f"SCOUT_RESULT {scout.name}" in prompt
        assert "Read only" in prompt
        assert "Do not change files or external systems" in prompt
        assert "Use at most four search/read commands total" in prompt
        assert "Do not load workflow skills" in prompt
        assert "pull request" not in prompt.lower()
        assert "commit" not in prompt.lower()


def test_extract_scout_result_accepts_markdown_marker() -> None:
    module = load_module()
    events = [
        {
            "kind": "MessageEvent",
            "source": "agent",
            "message": (
                "**SCOUT_RESULT** `docs-scout`\n"
                "FILES_CHECKED:\n"
                "- docs/wiki/payments.md: product clue\n"
                "CONFIDENCE:\n"
                "- high"
            ),
        }
    ]

    result = module.extract_scout_result(events, "docs-scout")

    assert "**SCOUT_RESULT** `docs-scout`" in result
    assert "docs/wiki/payments.md" in result


def test_extract_scout_result_accepts_code_block_marker() -> None:
    module = load_module()
    events = [
        {
            "kind": "MessageEvent",
            "source": "agent",
            "content": [
                {
                    "type": "text",
                    "text": (
                        "```text\n"
                        "SCOUT_RESULT logs-scout\n"
                        "EVIDENCE:\n"
                        "- docs/logs/payment-error.log: timeout trace\n"
                        "```"
                    ),
                }
            ],
        }
    ]

    result = module.extract_scout_result(events, "logs-scout")

    assert "SCOUT_RESULT logs-scout" in result
    assert "payment-error.log" in result


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

    assert "Do not repeat a" in prompt
    assert "broad docs/logs/project search" in prompt
    assert "SCOUT_RESULT docs-scout" in prompt
    assert "DEMO_STEP 3: Implement Fix, Add Tests, Open PR" in prompt
    assert "DEMO_STEP 3 COMPLETE: PR ready for human review" in prompt
    assert "skills/sdlc-story/SKILL.md" in prompt
    assert "Create the implementation branch from origin/main" in prompt
    assert "git log --oneline origin/main..HEAD" in prompt
    assert "GITHUB_TOKEN" in prompt
    assert "Do not use GITHUB" in prompt
    assert "openhands-qa" in prompt
    assert "Open a GitHub pull request" in prompt


def test_timing_summary_calls_out_launcher_and_handoff_segments() -> None:
    module = load_module()
    scout = module.ConversationResult(
        name="repo-scout",
        conversation_id="scout",
        conversation_url="https://app.replicated.rajistics.com/conversations/scout",
        start_task_id="scout-task",
        start_status="READY",
        execution_status="finished",
        started_at="2026-06-30T00:00:20+00:00",
        ready_at="2026-06-30T00:00:30+00:00",
        finished_at="2026-06-30T00:01:20+00:00",
        elapsed_to_ready_seconds=10.0,
        elapsed_to_finished_seconds=60.0,
    )
    main = module.ConversationResult(
        name="main-jira-to-pr",
        conversation_id="main",
        conversation_url="https://app.replicated.rajistics.com/conversations/main",
        start_task_id="main-task",
        start_status="READY",
        execution_status="finished",
        started_at="2026-06-30T00:01:30+00:00",
        ready_at="2026-06-30T00:01:40+00:00",
        finished_at="2026-06-30T00:04:00+00:00",
        elapsed_to_ready_seconds=10.0,
        elapsed_to_finished_seconds=150.0,
    )

    summary = module.timing_summary(
        started_at="2026-06-30T00:00:00+00:00",
        finished_at="2026-06-30T00:04:10+00:00",
        scout_results=[scout],
        main_result=main,
        main_start_barrier_seconds=90,
    )

    assert summary["total_launcher_elapsed_seconds"] == 250.0
    assert summary["conversation_layout"] == "top-level"
    assert "parent_ready_seconds" not in summary
    assert "Step 0 automation output is the index" in summary["index_note"]
    assert summary["scout_slowest_finished_seconds"] == 60.0
    assert summary["main_elapsed_seconds"] == 150.0
    assert "Review starts after the main agent adds openhands-review" in summary["qa_timing_note"]
    assert "openhands-qa" in summary["qa_timing_note"]
