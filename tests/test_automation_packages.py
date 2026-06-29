from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUTOMATIONS = ROOT / "automations" / "github"


def test_all_github_automation_packages_have_visible_demo_prompts() -> None:
    specs = sorted(AUTOMATIONS.glob("openhands-*/automation.prompt-preset.json"))
    assert {path.parent.name for path in specs} == {
        "openhands-build",
        "openhands-review",
        "openhands-qa",
        "openhands-incident",
    }

    for spec_path in specs:
        spec = json.loads(spec_path.read_text(encoding="utf-8"))
        prompt = (spec_path.parent / spec["prompt_file"]).read_text(encoding="utf-8")
        assert spec["preset"] == "prompt"
        assert spec_path.parent.name in spec["trigger"]["filter"]
        assert "What You Do" in prompt
        assert "What You Post Back To GitHub" in prompt
        assert "Human Control" in prompt
        assert "Cost And Security" in prompt


def test_build_prompt_makes_bug_evidence_stops_visible() -> None:
    prompt = (AUTOMATIONS / "openhands-build" / "prompt.md").read_text(
        encoding="utf-8"
    )

    for waypoint in [
        "Stop 1 - Ticket",
        "Stop 2 - Wiki/Docs",
        "Stop 3 - Logs",
        "Stop 4 - Repo/Files",
        "Stop 5 - Tests/PR",
    ]:
        assert waypoint in prompt

    assert "docs/wiki/" in prompt
    assert "docs/logs/" in prompt
    assert "PENDING_PET_VISIBLE" in prompt
