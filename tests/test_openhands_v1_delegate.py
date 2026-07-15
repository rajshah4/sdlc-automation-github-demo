from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def delegate_module():
    return load_module(ROOT / "scripts" / "openhands_v1_delegate.py", "openhands_v1_delegate_test")


def test_latest_execution_status_recovers_enterprise_full_state() -> None:
    delegate = delegate_module()
    events = [
        {
            "kind": "ConversationStateUpdateEvent",
            "key": "full_state",
            "value": {"execution_status": "finished"},
        }
    ]

    assert delegate.latest_execution_status(events) == "finished"


def test_poll_conversation_recovers_finished_status_after_sandbox_pause(monkeypatch) -> None:
    delegate = delegate_module()
    monkeypatch.setattr(
        delegate,
        "request_json",
        lambda *args, **kwargs: [{"execution_status": None, "sandbox_status": "PAUSED"}],
    )
    monkeypatch.setattr(
        delegate,
        "fetch_events",
        lambda **kwargs: [
            {
                "kind": "ConversationStateUpdateEvent",
                "key": "full_state",
                "value": {"execution_status": "finished"},
            }
        ],
    )

    result = delegate.poll_conversation(
        base="https://example.test",
        headers={},
        conversation_id="child-1",
        timeout_seconds=1,
        poll_seconds=0,
    )

    assert result["execution_status"] == "finished"
    assert result["execution_status_source"] == "events"


def test_poll_conversation_turns_unresolved_pause_into_bounded_gate(monkeypatch) -> None:
    delegate = delegate_module()
    monkeypatch.setattr(
        delegate,
        "request_json",
        lambda *args, **kwargs: [{"execution_status": None, "sandbox_status": "PAUSED"}],
    )
    monkeypatch.setattr(delegate, "fetch_events", lambda **kwargs: [])

    result = delegate.poll_conversation(
        base="https://example.test",
        headers={},
        conversation_id="child-2",
        timeout_seconds=1,
        poll_seconds=0,
    )

    assert result["execution_status"] == "paused"
    assert result["execution_status_source"] == "sandbox"


def test_wait_for_agent_text_retries_eventual_enterprise_index(monkeypatch) -> None:
    delegate = delegate_module()
    event_pages = [
        [],
        [
            {
                "source": "agent",
                "llm_message": {
                    "content": [{"type": "text", "text": "status: done"}],
                },
            }
        ],
    ]
    sleeps: list[int] = []

    monkeypatch.setattr(delegate, "fetch_events", lambda **_: event_pages.pop(0))
    monkeypatch.setattr(delegate.time, "sleep", sleeps.append)

    assert (
        delegate.wait_for_agent_text(
            base="https://example.test",
            headers={},
            conversation_id="conversation-1",
            grace_seconds=30,
            poll_seconds=3,
        )
        == "status: done"
    )
    assert sleeps == [3]
