from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_delegate_module():
    path = ROOT / "scripts" / "agent_canvas_delegate.py"
    spec = importlib.util.spec_from_file_location("agent_canvas_delegate", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_delegate_payload_preserves_encrypted_settings_and_adds_tools(tmp_path: Path) -> None:
    delegate = load_delegate_module()
    settings = {
        "agent_settings": {
            "schema_version": "1",
            "mcp_config": {"servers": {}},
            "llm": {"api_key": "gAAAAA-encrypted-token"},
            "tools": [{"name": "terminal", "params": {"existing": True}}],
            "agent_context": {"load_public_skills": False},
        },
        "conversation_settings": {"max_iterations": 77},
    }

    payload = delegate.build_conversation_payload(
        settings_response=settings,
        prompt="hello",
        workspace=tmp_path,
        max_iterations=None,
        include_task_tools=True,
        run=True,
    )

    assert payload["secrets_encrypted"] is True
    assert payload["agent_settings"]["llm"]["api_key"] == "gAAAAA-encrypted-token"
    assert "schema_version" not in payload["agent_settings"]
    assert "mcp_config" not in payload["agent_settings"]
    assert payload["max_iterations"] == 77
    assert payload["workspace"]["working_dir"] == str(tmp_path.resolve())
    assert payload["initial_message"]["run"] is True

    tool_names = {tool["name"] for tool in payload["agent_settings"]["tools"]}
    assert {
        "terminal",
        "file_editor",
        "task_tracker",
        "browser_tool_set",
        "canvas_ui",
        "task_tool_set",
    } <= tool_names

    context = payload["agent_settings"]["agent_context"]
    assert context["load_public_skills"] is True
    assert context["load_user_skills"] is True
    assert context["load_project_skills"] is True


def test_render_prompt_replaces_variables(tmp_path: Path) -> None:
    delegate = load_delegate_module()
    prompt = tmp_path / "prompt.md"
    prompt.write_text("Run {{run_id}} for {{repo_slug}}", encoding="utf-8")

    assert delegate.render_prompt(prompt, {"run_id": "abc", "repo_slug": "owner/repo"}) == "Run abc for owner/repo"


def test_supervisor_prompt_delegates_all_work_cells() -> None:
    prompt = (ROOT / "agent-canvas" / "prompts" / "supervisor.md").read_text(encoding="utf-8")

    assert "The human starts only this parent conversation" in prompt
    assert "scripts/run_agent_canvas_factory.py" in prompt
    assert "Do not hand-roll Agent Canvas API requests" in prompt
    assert "Do not write settings JSON files" in prompt
    assert "GitHub labels are not the trigger mechanism" in prompt
    assert "--base http://localhost:8000" in prompt
    assert "{{code_review_profile_arg}}" in prompt
    assert "{{qa_playwright_arg}}" in prompt
    for name in ("story-to-pr", "code-review", "qa"):
        assert name in prompt


def test_work_cell_prompts_are_self_contained() -> None:
    prompts = sorted((ROOT / "agent-canvas" / "prompts" / "workcells").glob("*.md"))
    assert {path.stem for path in prompts} == {
        "code-review",
        "qa",
        "story-to-pr",
    }

    for path in prompts:
        text = path.read_text(encoding="utf-8")
        assert "## Inputs" in text
        assert "## What You Do" in text
        assert "## Output Contract" in text
        assert "Final response format" in text
        assert "factory_runs/{{run_id}}" in text
        assert "GitHub labels are not" in text
        assert "Use `{{repo_path}}` as the only working tree" in text


def test_delegate_registry_append(tmp_path: Path) -> None:
    delegate = load_delegate_module()
    registry = tmp_path / "children.json"

    delegate.append_registry(registry, {"id": "one", "name": "story-to-pr"})
    delegate.append_registry(registry, {"id": "two", "name": "code-review"})

    assert json.loads(registry.read_text(encoding="utf-8")) == [
        {"id": "one", "name": "story-to-pr"},
        {"id": "two", "name": "code-review"},
    ]


def test_orchestrator_has_all_work_cells() -> None:
    path = ROOT / "scripts" / "run_agent_canvas_factory.py"
    spec = importlib.util.spec_from_file_location("run_agent_canvas_factory", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(ROOT / "scripts"))
    spec.loader.exec_module(module)

    assert module.ACTIVE_WORK_CELLS == ("story-to-pr", "code-review", "qa")
    assert module.WORK_CELLS == ("story-to-pr", "code-review", "qa")
    assert module.cell_prompt_path(Path("/tmp/prompts"), "qa") == Path("/tmp/prompts/workcells/qa.md")


def test_orchestrator_snapshots_prompts_before_delegating() -> None:
    factory = (ROOT / "scripts" / "run_agent_canvas_factory.py").read_text(encoding="utf-8")

    assert "prompt-snapshot" in factory
    assert "snapshot_prompts(run_dir)" in factory
    assert "prompt_root=prompt_root" in factory


def test_launcher_records_parent_conversation_artifact() -> None:
    launcher = (ROOT / "scripts" / "start_agent_canvas_factory.py").read_text(encoding="utf-8")
    assert "parent.conversation.json" in launcher
    assert "--require-playwright-qa" in launcher
    assert "--playwright-node-path" in launcher


def test_qa_prompt_supports_required_playwright() -> None:
    qa_prompt = (ROOT / "agent-canvas" / "prompts" / "workcells" / "qa.md").read_text(encoding="utf-8")
    assert "{{qa_playwright_requirement}}" in qa_prompt
    assert "{{playwright_node_path}}" in qa_prompt
    assert "Playwright is required" in qa_prompt or "When Playwright is required" in qa_prompt
