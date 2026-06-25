from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GITHUB_AUTOMATIONS = ROOT / "automations" / "github"
JIRA_AUTOMATIONS = ROOT / "automations" / "jira"


def test_all_github_automation_packages_have_visible_demo_prompts() -> None:
    specs = sorted(GITHUB_AUTOMATIONS.glob("openhands-*/automation.prompt-preset.json"))
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


def test_jira_automation_package_has_visible_demo_prompt() -> None:
    specs = sorted(JIRA_AUTOMATIONS.glob("openhands-*/automation.prompt-preset.json"))
    assert {path.parent.name for path in specs} == {"openhands-build", "openhands-build-direct"}

    for spec_path in specs:
        spec = json.loads(spec_path.read_text(encoding="utf-8"))
        prompt = (spec_path.parent / spec["prompt_file"]).read_text(encoding="utf-8")
        assert spec["preset"] == "prompt"
        assert spec["trigger"]["source"] in {"jira", "jira-direct"}
        assert spec["trigger"]["on"] in {"comment_created", "jira:issue_created"}
        assert "JIRA_API_BASE_URL" in prompt
        assert "Authorization: Bearer" in prompt
        assert "What You Do" in prompt
        assert "What You Post Back To Jira" in prompt
        assert "Human Control" in prompt
        assert "Cost And Security" in prompt
        if spec_path.parent.name == "openhands-build-direct":
            assert "business language" in prompt
            assert "Microsoft Teams" in prompt
            assert "docs/logs" in prompt
