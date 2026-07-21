from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
AUTOMATIONS = ROOT / "automations" / "github"
JIRA_AUTOMATIONS = ROOT / "automations" / "jira"


def load_script_function(script_path: Path, function_name: str) -> Any:
    spec = importlib.util.spec_from_file_location(script_path.stem, script_path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, function_name)


def test_all_github_automation_packages_have_visible_demo_prompts() -> None:
    specs = sorted(AUTOMATIONS.glob("openhands-*/automation.prompt-preset.json"))
    assert {path.parent.name for path in specs} == {
        "openhands-context",
        "openhands-build",
        "openhands-review",
        "openhands-qa",
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
        assert "GITHUB_TOKEN" in prompt
        assert "secret named `GITHUB`" in prompt


def test_github_automation_specs_include_model_profiles() -> None:
    expected_models = {
        "openhands-build": "Bedrock-Claude-Sonnet-4-5",
        "openhands-qa": "Bedrock-Claude-Sonnet-4-5-fast",
        "openhands-review": "Bedrock-Claude-Haiku-4-5",
    }

    for automation_name, expected_model in expected_models.items():
        spec_path = AUTOMATIONS / automation_name / "automation.prompt-preset.json"
        spec = json.loads(spec_path.read_text(encoding="utf-8"))
        assert spec["model"] == expected_model
        assert spec["repos"][0]["url"] == "${GITHUB_DEMO_REPO_URL}"
        assert spec["repos"][0]["ref"] == "${GITHUB_DEMO_REF}"

    context_spec = json.loads(
        (AUTOMATIONS / "openhands-context" / "automation.prompt-preset.json").read_text(
            encoding="utf-8"
        )
    )
    assert context_spec["model"] == "Bedrock-Claude-Haiku-4-5"
    assert context_spec["repos"][0]["ref"] == "${GITHUB_DEMO_REF}"


def test_github_registration_preserves_keep_alive(monkeypatch) -> None:
    monkeypatch.setenv("GITHUB_DEMO_REPOSITORY", "example/demo")
    monkeypatch.setenv("GITHUB_DEMO_REPO_URL", "https://github.com/example/demo")
    monkeypatch.setenv("GITHUB_DEMO_REF", "main")

    load_request = load_script_function(
        ROOT / "scripts" / "automations" / "register_github_automations.py",
        "load_request",
    )
    payload = load_request(
        AUTOMATIONS / "openhands-build" / "automation.prompt-preset.json"
    )

    assert payload["keep_alive"] is True


def test_build_prompt_is_a_short_orchestrator() -> None:
    prompt = (AUTOMATIONS / "openhands-build" / "prompt.md").read_text(
        encoding="utf-8"
    )

    assert "skills/sdlc-story/SKILL.md" in prompt
    assert "GITHUB_TOKEN" in prompt
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
    assert "GITHUB_TOKEN" in prompt
    assert spec["model"] == "Bedrock-Claude-Sonnet-4-5-fast"
    assert spec["repos"][0]["url"] == "${GITHUB_DEMO_REPO_URL}"
    assert spec["repos"][0]["ref"] == "${GITHUB_DEMO_REF}"
    assert "sidekick-v2" in spec["trigger"]["filter"]
    assert "!contains" in spec["trigger"]["filter"]
    assert "openhands-review" in prompt
    assert "Do not add `openhands-qa`" in prompt
    assert "PENDING_PET_VISIBLE" not in prompt
    assert "docs/wiki/" not in prompt
    assert "docs/logs/" not in prompt
    assert len(prompt.split()) < 220


def test_jira_registration_preserves_secret_placeholders(monkeypatch) -> None:
    monkeypatch.setenv("JIRA_DEMO_PROJECT_KEY", "KAN")
    monkeypatch.setenv("GITHUB_DEMO_REPO_URL", "https://github.com/example/demo")
    monkeypatch.setenv("GITHUB_DEMO_REF", "demo-ref")
    monkeypatch.setenv("JIRA_API_TOKEN", "secret-value-that-must-not-expand")
    monkeypatch.setenv("JIRA_API_BASE_URL", "https://jira.example.invalid")

    load_request = load_script_function(
        ROOT / "scripts" / "automations" / "register_jira_automations.py",
        "load_request",
    )
    payload = load_request(
        JIRA_AUTOMATIONS / "jira-to-story" / "automation.prompt-preset.json"
    )

    assert payload["trigger"]["filter"] == (
        "issue.fields.project.key == 'KAN' && issue.fields.issuetype.name == 'Task' "
        "&& !contains(issue.fields.labels, 'sidekick-v2')"
    )
    assert payload["repos"][0]["url"] == "https://github.com/example/demo"
    assert payload["repos"][0]["ref"] == "demo-ref"
    assert "secret-value-that-must-not-expand" not in payload["prompt"]
    assert "${JIRA_API_TOKEN}" in payload["prompt"]
    assert "${JIRA_API_BASE_URL}" in payload["prompt"]


def test_public_jira_automation_set_is_demo_focused() -> None:
    specs = sorted(JIRA_AUTOMATIONS.glob("jira-to-story*/automation.prompt-preset.json"))
    assert {path.parent.name for path in specs} == {
        "jira-to-story",
        "jira-to-story-sidekick-v2",
    }


def test_sidekick_v2_jira_automation_is_label_gated() -> None:
    spec_path = JIRA_AUTOMATIONS / "jira-to-story-sidekick-v2" / "automation.prompt-preset.json"
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    prompt = (spec_path.parent / spec["prompt_file"]).read_text(encoding="utf-8")

    assert spec["preset"] == "prompt"
    assert spec["trigger"]["source"] == "jira-direct"
    assert spec["trigger"]["on"] == "jira:issue_created"
    assert "sidekick-v2" in spec["trigger"]["filter"]
    assert "GITHUB_TOKEN" in prompt
    assert spec["model"] == "Bedrock-Claude-Sonnet-4-5-fast"
    assert spec["repos"][0]["ref"] == "${GITHUB_DEMO_REF}"
    assert "skills/sdlc-sidekick-launcher/SKILL.md" in prompt
    assert "skills/sdlc-context-sidekick/SKILL.md" not in prompt
    assert "Do not implement the code change yourself" in prompt
    assert "exactly once" in prompt
    assert "export OPENHANDS_HOST" not in prompt
    assert "python3 scripts/sidekick/launch_sidekick_v2.py" not in prompt
    assert "child conversation" not in prompt
    assert "Parent conversation" not in prompt


def test_sidekick_launcher_skill_owns_launcher_details() -> None:
    skill = (ROOT / "skills" / "sdlc-sidekick-launcher" / "SKILL.md").read_text(
        encoding="utf-8"
    )

    for phrase in [
        "scripts/sidekick/launch_sidekick_v2.py",
        "--jira-key",
        "--title",
        "--body",
        "--full",
        "exactly once",
        "Do not inspect the launcher script first",
        "Do not rerun the launcher",
        "GITHUB_TOKEN",
        "Do not use `GITHUB` or `GH_TOKEN`",
        "DEMO_STEP 0: Jira Webhook Launcher",
        "timing_summary",
        "The Step 0 response is the visible index",
    ]:
        assert phrase in skill


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
    assert "GITHUB_TOKEN" in skill
    assert "Do not use `GITHUB` or `GH_TOKEN`" in skill
    assert "docs/wiki/" in artifacts
    assert "docs/logs/" in artifacts
    assert "Jira issue URL" in artifacts
    assert "separate review conversation" in artifacts


def test_story_review_qa_handoff_is_sequential() -> None:
    story_prompt = (JIRA_AUTOMATIONS / "jira-to-story" / "prompt.md").read_text(
        encoding="utf-8"
    )
    review_prompt = (AUTOMATIONS / "openhands-review" / "prompt.md").read_text(
        encoding="utf-8"
    )
    qa_prompt = (AUTOMATIONS / "openhands-qa" / "prompt.md").read_text(
        encoding="utf-8"
    )

    assert "Add `openhands-review` as the final GitHub mutation" in story_prompt
    assert "Do not add `openhands-qa`" in story_prompt
    assert "add `openhands-qa`" in review_prompt
    assert "before posting the final review" in review_prompt
    assert "Do not add `openhands:done`" in review_prompt
    assert "add `openhands:done`" in qa_prompt

    review_spec = json.loads(
        (AUTOMATIONS / "openhands-review" / "automation.prompt-preset.json").read_text(
            encoding="utf-8"
        )
    )
    qa_spec = json.loads(
        (AUTOMATIONS / "openhands-qa" / "automation.prompt-preset.json").read_text(
            encoding="utf-8"
        )
    )
    assert "openhands:in-progress" not in review_spec["trigger"]["filter"]
    assert "openhands:in-progress" not in qa_spec["trigger"]["filter"]


def test_jira_prompt_preserves_keep_alive() -> None:
    spec = json.loads(
        (JIRA_AUTOMATIONS / "jira-to-story" / "automation.prompt-preset.json").read_text(
            encoding="utf-8"
        )
    )
    assert spec["keep_alive"] is True


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


def test_github_runtime_secret_convention_is_consistent() -> None:
    paths = [
        ROOT / "skills" / "sdlc-story" / "SKILL.md",
        ROOT / "skills" / "sdlc-qa" / "SKILL.md",
        ROOT / "skills" / "sdlc-code-review" / "SKILL.md",
        ROOT / "skills" / "sdlc-sidekick-launcher" / "SKILL.md",
        AUTOMATIONS / "openhands-build" / "prompt.md",
        AUTOMATIONS / "openhands-qa" / "prompt.md",
        AUTOMATIONS / "openhands-review" / "prompt.md",
        JIRA_AUTOMATIONS / "jira-to-story" / "prompt.md",
        JIRA_AUTOMATIONS / "jira-to-story-sidekick-v2" / "prompt.md",
    ]

    for path in paths:
        text = path.read_text(encoding="utf-8")
        assert "GITHUB_TOKEN" in text, path
        assert "GH_TOKEN" in text or "secret named `GITHUB`" in text, path
