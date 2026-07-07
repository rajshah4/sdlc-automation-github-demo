from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "automations" / "replicated-jira-delegated-factory"


def test_replicated_factory_is_opt_in_package() -> None:
    existing_jira = sorted((ROOT / "automations" / "jira").glob("openhands-*/automation.prompt-preset.json"))
    if existing_jira:
        assert {path.parent.name for path in existing_jira} == {"openhands-build"}

    spec = json.loads((PACKAGE / "automation.prompt-preset.json").read_text(encoding="utf-8"))
    assert spec["preset"] == "prompt"
    assert spec["trigger"]["source"] == "jira-direct"
    assert spec["trigger"]["on"] == "jira:issue_created"
    assert spec["timeout"] >= 3600


def test_replicated_factory_parent_prompt_delegates_and_stays_alive() -> None:
    prompt = (PACKAGE / "prompt.md").read_text(encoding="utf-8")

    assert "Stay alive as the parent supervisor" in prompt
    assert "scripts/run_replicated_factory.py" in prompt
    assert "skills/delegated-conversation-factory/SKILL.md" in prompt
    assert "Do not modify or depend on the existing" in prompt
    for cell in ("story-to-pr", "code-review", "qa"):
        assert cell in prompt


def test_replicated_factory_workcells_have_output_contracts() -> None:
    prompts = sorted((PACKAGE / "workcells").glob("*.md"))
    assert {path.stem for path in prompts} == {"story-to-pr", "code-review", "qa"}

    for path in prompts:
        text = path.read_text(encoding="utf-8")
        assert "## Inputs" in text
        assert "## What You Do" in text
        assert "## Human Control" in text
        assert "## Output Contract" in text
        assert "Final response format" in text
        assert "{{artifact_path}}" in text


def test_replicated_factory_orchestrator_uses_opt_in_prompt_root() -> None:
    path = ROOT / "scripts" / "run_replicated_factory.py"
    spec = importlib.util.spec_from_file_location("run_replicated_factory", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(ROOT / "scripts"))
    spec.loader.exec_module(module)

    assert module.PROMPT_ROOT == PACKAGE / "workcells"
    assert module.ACTIVE_WORK_CELLS == ("story-to-pr", "code-review", "qa")
