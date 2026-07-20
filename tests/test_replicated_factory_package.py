from __future__ import annotations

import importlib.util
import json
import sys
from argparse import Namespace
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "automations" / "replicated-jira-delegated-factory"


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_replicated_factory_is_opt_in_package() -> None:
    existing_jira = sorted((ROOT / "automations" / "jira").glob("*/automation.prompt-preset.json"))
    assert {path.parent.name for path in existing_jira} == {
        "jira-to-story",
        "jira-to-story-sidekick-v2",
    }

    spec = json.loads((PACKAGE / "automation.prompt-preset.json").read_text(encoding="utf-8"))
    assert spec["preset"] == "prompt"
    assert spec["trigger"]["source"] == "jira-direct"
    assert spec["trigger"]["on"] == "jira:issue_created"
    assert "openhands-foundry-parent" in spec["trigger"]["filter"]
    assert "foundry-it-demo" in spec["trigger"]["filter"]
    assert "rtl-request" in spec["trigger"]["filter"]
    assert spec["timeout"] == 1800
    assert spec["model"] == "Bedrock-Claude-Sonnet-4-5"
    assert "llm_profile" not in spec


def test_replicated_factory_registration_forwards_model_and_expands_ref(monkeypatch) -> None:
    monkeypatch.setenv("JIRA_DEMO_PROJECT_KEY", "KAN")
    monkeypatch.setenv("GITHUB_DEMO_REPO_URL", "https://github.com/example/demo")
    monkeypatch.setenv("GITHUB_DEMO_REF", "feature/example-ref")

    module = load_module(
        ROOT / "scripts" / "register_replicated_factory_automation.py",
        "register_replicated_factory_automation",
    )
    payload = module.load_request()

    assert payload["model"] == "Bedrock-Claude-Sonnet-4-5"
    assert payload["repos"][0]["ref"] == "feature/example-ref"
    assert "--branch feature/example-ref" in payload["prompt"]
    assert "${GITHUB_DEMO_REF}" not in payload["prompt"]


def test_replicated_factory_registration_prefers_org_automation_key(monkeypatch) -> None:
    module = load_module(
        ROOT / "scripts" / "register_replicated_factory_automation.py",
        "register_replicated_factory_automation_key",
    )
    monkeypatch.setenv("OPENHANDS_API_KEY_ORG", "org-key")
    monkeypatch.setenv("OPENHANDS_API_KEY_JIRA", "jira-key")
    monkeypatch.setenv("OPENHANDS_API_KEY_RAJISTICS", "rajistics-key")

    assert module.automation_api_key() == "org-key"


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
        assert "{{parent_final_artifact}}" in text
        assert "separate sandboxes" in text


def test_replicated_factory_orchestrator_uses_opt_in_prompt_root() -> None:
    path = ROOT / "scripts" / "run_replicated_factory.py"
    sys.path.insert(0, str(ROOT / "scripts"))
    module = load_module(path, "run_replicated_factory")

    assert module.PROMPT_ROOT == PACKAGE / "workcells"
    assert module.ACTIVE_WORK_CELLS == ("story-to-pr", "code-review", "qa")
    args = Namespace(
        run_id="demo-run",
        repo_slug="example/demo",
        issue_key="KAN-1",
        issue_url="",
        request_title="Title",
        request_body="Body",
    )
    variables = module.variables_for_cell(args, "qa", "prior")
    assert variables["parent_final_artifact"] == "factory_runs/demo-run/qa.final.md"
    assert module.cell_status("story-to-pr", "", "finished") == "needs-human"
    assert module.cell_status("story-to-pr", "status: done", "finished") == "done"
    assert module.gate_allows_next_cell("story-to-pr", "done")
    assert not module.gate_allows_next_cell("story-to-pr", "finished")
    assert module.gate_allows_next_cell(
        "code-review",
        "findings",
        "status: findings\nblocking: no\nnext_gate: qa",
    )
    assert not module.gate_allows_next_cell(
        "code-review",
        "findings",
        "status: findings\nblocking: yes\nnext_gate: stop",
    )


def test_delegated_factory_skill_points_to_replicated_template() -> None:
    skill_root = ROOT / "skills" / "delegated-conversation-factory"
    skill = (skill_root / "SKILL.md").read_text(encoding="utf-8")
    blueprint = (skill_root / "references" / "blueprint.md").read_text(encoding="utf-8")
    asset = json.loads((skill_root / "assets" / "factory-blueprint.json").read_text(encoding="utf-8"))

    assert "scripts/run_replicated_factory.py" in skill
    assert "scripts/openhands_v1_delegate.py" in skill
    assert "--runtime replicated" in skill
    assert "agent-canvas/prompts/supervisor.md" not in blueprint
    assert "<work-cell>.final.md" in blueprint
    assert asset["runtime"] == "replicated"
    assert asset["cells"][0]["artifact"].endswith(".final.md")


def test_scaffolder_defaults_to_replicated_runtime(tmp_path) -> None:
    module = load_module(
        ROOT
        / "skills"
        / "delegated-conversation-factory"
        / "scripts"
        / "scaffold_delegated_factory.py",
        "scaffold_delegated_factory",
    )
    target = tmp_path / "target-repo"
    args = Namespace(
        target=target,
        name="customer-factory",
        runtime="replicated",
        cells=["plan", "build"],
        force=False,
    )

    assert module.scaffold(args) == 0
    assert (target / "automations" / "customer-factory" / "automation.prompt-preset.json").exists()
    assert (target / "automations" / "customer-factory" / "prompt.md").exists()
    assert (target / "automations" / "customer-factory" / "workcells" / "plan.md").exists()
    assert (target / "scripts" / "run_replicated_factory.py").exists()
    assert not (target / "agent-canvas" / "prompts" / "supervisor.md").exists()

    generated = (target / "scripts" / "run_replicated_factory.py").read_text(encoding="utf-8")
    assert "customer-factory" in generated
