from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUTOMATIONS = ROOT / "automations" / "github"
JIRA_AUTOMATIONS = ROOT / "automations" / "jira"


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


def test_github_automation_specs_include_model_profiles() -> None:
    expected_models = {
        "openhands-build": "Bedrock-Claude-Sonnet-4-5",
        "openhands-qa": "Bedrock-Qwen3-Coder-30B",
        "openhands-review": "Bedrock-Claude-Haiku-4-5",
        "openhands-incident": "Bedrock-Claude-Sonnet-4-5",
    }

    for automation_name, expected_model in expected_models.items():
        spec_path = AUTOMATIONS / automation_name / "automation.prompt-preset.json"
        spec = json.loads(spec_path.read_text(encoding="utf-8"))
        assert spec["model"] == expected_model


def test_build_prompt_is_a_short_orchestrator() -> None:
    prompt = (AUTOMATIONS / "openhands-build" / "prompt.md").read_text(
        encoding="utf-8"
    )

    assert "skills/sdlc-story/SKILL.md" in prompt
    assert "PENDING_PET_VISIBLE" not in prompt
    assert "docs/wiki/" not in prompt
    assert "docs/logs/" not in prompt
    assert "Stop 1 - Ticket" not in prompt
    assert len(prompt.split()) < 220


def test_jira_prompt_is_a_short_orchestrator() -> None:
    spec_path = JIRA_AUTOMATIONS / "jira-to-story" / "automation.prompt-preset.json"
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    prompt = (spec_path.parent / spec["prompt_file"]).read_text(encoding="utf-8")

    assert spec["preset"] == "prompt"
    assert spec["trigger"]["source"] == "jira-direct"
    assert spec["trigger"]["on"] == "jira:issue_created"
    assert "JIRA_DEMO_PROJECT_KEY" in spec["trigger"]["filter"]
    assert "skills/sdlc-story/SKILL.md" in prompt
    assert spec["model"] == "Bedrock-Claude-Sonnet-4-5"
    assert "openhands-qa" in prompt
    assert "PENDING_PET_VISIBLE" not in prompt
    assert "docs/wiki/" not in prompt
    assert "docs/logs/" not in prompt
    assert len(prompt.split()) < 220


def test_sidekick_experiment_jira_automation_specs_are_label_gated() -> None:
    expected = {
        "jira-to-story-control": {
            "label": "control-experiment",
            "required_prompt": "skills/sdlc-story/SKILL.md",
            "forbidden_prompt": "skills/sdlc-context-sidekick",
        },
        "jira-to-story-sidekick": {
            "label": "sidekick-experiment",
            "required_prompt": "skills/sdlc-context-sidekick/SKILL.md",
            "forbidden_prompt": "",
        },
    }

    for automation_name, expectation in expected.items():
        spec_path = JIRA_AUTOMATIONS / automation_name / "automation.prompt-preset.json"
        spec = json.loads(spec_path.read_text(encoding="utf-8"))
        prompt = (spec_path.parent / spec["prompt_file"]).read_text(encoding="utf-8")

        assert spec["preset"] == "prompt"
        assert spec["trigger"]["source"] == "jira-direct"
        assert spec["trigger"]["on"] == "jira:issue_created"
        assert expectation["label"] in spec["trigger"]["filter"]
        assert spec["repos"][0]["ref"] == "sidekick-context-experiment"
        assert spec["model"] == "Bedrock-Claude-Sonnet-4-5"
        assert expectation["required_prompt"] in prompt
        if expectation["forbidden_prompt"]:
            assert expectation["forbidden_prompt"] not in prompt


def test_story_skill_owns_bug_evidence_and_artifact_details() -> None:
    skill = (ROOT / "skills" / "sdlc-story" / "SKILL.md").read_text(
        encoding="utf-8"
    )
    artifacts = (
        ROOT / "skills" / "sdlc-story" / "references" / "story-artifacts.md"
    ).read_text(encoding="utf-8")

    for waypoint in [
        "Stop 1 - Ticket",
        "Stop 2 - Wiki/Docs",
        "Stop 3 - Logs",
        "Stop 4 - Repo/Files",
        "Stop 5 - Tests/PR",
    ]:
        assert waypoint in artifacts

    assert "PENDING_PET_VISIBLE" in skill
    assert "docs/wiki/" in artifacts
    assert "docs/logs/" in artifacts
    assert "Jira issue URL" in artifacts
    assert "second QA conversation" in artifacts


def test_context_sidekick_is_read_only_and_bounded() -> None:
    skill = (ROOT / "skills" / "sdlc-context-sidekick" / "SKILL.md").read_text(
        encoding="utf-8"
    )
    brief_format = (
        ROOT / "skills" / "sdlc-context-sidekick" / "references" / "brief-format.md"
    ).read_text(encoding="utf-8")

    for phrase in [
        "Read only",
        "Do not edit files",
        "Do not create branches, commits, PRs",
        "CONTEXT_BRIEF",
        "NEEDS_HUMAN",
    ]:
        assert phrase in skill

    for section in [
        "LIKELY_REPO_AREA",
        "DOCS_CHECKED",
        "LOGS_CHECKED",
        "LIKELY_FILES",
        "CONFIDENCE",
        "RECOMMENDED_NEXT_STEP",
    ]:
        assert section in brief_format
