from __future__ import annotations

import importlib.util
import json
import sys
from types import SimpleNamespace
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CANVAS_SCRIPTS = ROOT / "agent-canvas" / "scripts"


def load_delegate_module():
    path = CANVAS_SCRIPTS / "agent_canvas_delegate.py"
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


def test_idle_is_not_a_terminal_canvas_status() -> None:
    delegate = load_delegate_module()

    assert "idle" not in delegate.TERMINAL_STATUSES
    assert {"finished", "error", "stuck", "stopped"} <= delegate.TERMINAL_STATUSES


def test_render_prompt_replaces_variables(tmp_path: Path) -> None:
    delegate = load_delegate_module()
    prompt = tmp_path / "prompt.md"
    prompt.write_text("Run {{run_id}} for {{repo_slug}}", encoding="utf-8")

    assert delegate.render_prompt(prompt, {"run_id": "abc", "repo_slug": "owner/repo"}) == "Run abc for owner/repo"


def test_supervisor_prompt_delegates_all_work_cells() -> None:
    prompt = (ROOT / "agent-canvas" / "prompts" / "supervisor.md").read_text(encoding="utf-8")

    assert "The human starts only this parent conversation" in prompt
    assert "agent-canvas/scripts/run_agent_canvas_factory.py" in prompt
    assert "Do not hand-roll Agent Canvas API requests" in prompt
    assert "Do not write settings JSON files" in prompt
    assert "GitHub labels are not the trigger mechanism" in prompt
    assert "--base http://localhost:8000" in prompt
    assert "--run-date" in prompt
    assert "{{run_date}}" in prompt
    assert "{{code_review_profile_arg}}" in prompt
    assert "{{qa_playwright_arg}}" in prompt
    assert "--handoff-after-story" in prompt
    assert "The downstream delegates" in prompt
    assert "update their own PR sections" in prompt
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
        assert "{{run_date}}" in text


def test_story_prompt_requires_workcell_owned_plain_pr() -> None:
    prompt = (ROOT / "agent-canvas" / "prompts" / "workcells" / "story-to-pr.md").read_text(
        encoding="utf-8"
    )

    assert "The PR must be created by this delegated conversation" in prompt
    assert "agent/issue-{{issue_number}}-{{run_id}}" in prompt
    assert "Do not reuse a branch or PR from a" in prompt
    assert "Do not claim browser" in prompt
    assert "## 1. Story" in prompt
    assert "## 2. Code" in prompt
    assert "## 3. Code Review" in prompt
    assert "## 4. QA" in prompt
    assert "promotional language" in prompt


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
    path = CANVAS_SCRIPTS / "run_agent_canvas_factory.py"
    spec = importlib.util.spec_from_file_location("run_agent_canvas_factory", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(CANVAS_SCRIPTS))
    spec.loader.exec_module(module)

    assert module.ACTIVE_WORK_CELLS == ("story-to-pr", "code-review", "qa")
    assert module.WORK_CELLS == ("story-to-pr", "code-review", "qa")
    assert module.cell_prompt_path(Path("/tmp/prompts"), "qa") == Path("/tmp/prompts/workcells/qa.md")


def test_orchestrator_composes_plain_four_step_pr_body(tmp_path: Path) -> None:
    path = CANVAS_SCRIPTS / "run_agent_canvas_factory.py"
    spec = importlib.util.spec_from_file_location("run_agent_canvas_factory", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(CANVAS_SCRIPTS))
    spec.loader.exec_module(module)

    run_dir = tmp_path / "factory_runs" / "run-1"
    run_dir.mkdir(parents=True)
    (tmp_path / "app" / "petstore_app").mkdir(parents=True)
    (tmp_path / "app" / "petstore_app" / "catalog.py").write_text("", encoding="utf-8")
    (tmp_path / "agent-canvas" / "scripts").mkdir(parents=True)
    (tmp_path / "agent-canvas" / "scripts" / "run_petstore_playwright_qa.py").write_text(
        "",
        encoding="utf-8",
    )
    (run_dir / "story-to-pr.md").write_text("Status: done\n", encoding="utf-8")
    (run_dir / "code-review.md").write_text("Blocking: no\n", encoding="utf-8")
    (run_dir / "qa.md").write_text("Status: pass\n", encoding="utf-8")
    args = SimpleNamespace(
        repo=tmp_path,
        issue_number=88,
        request_title="Filter pets by max adoption fee",
        request_body="As an adoption coordinator, I want a max fee filter.",
    )

    body = module.compose_plain_pr_body(args, run_dir)

    assert "## 1. Story" in body
    assert "## 2. Code" in body
    assert "## 3. Code Review" in body
    assert "## 4. QA" in body
    assert "Review status: no" in body
    assert "QA status: pass" in body
    assert "`app/petstore_app/catalog.py`" in body
    assert "max-adoption-fee-filter.playwright.mjs" not in body
    assert "agent-canvas/scripts/run_petstore_playwright_qa.py" in body
    assert "Factory Lifecycle" not in body
    assert "customer-facing" not in body


def test_orchestrator_handoff_waits_only_for_story() -> None:
    path = CANVAS_SCRIPTS / "run_agent_canvas_factory.py"
    spec = importlib.util.spec_from_file_location("run_agent_canvas_factory", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(CANVAS_SCRIPTS))
    spec.loader.exec_module(module)

    assert module.should_wait_for_cell(SimpleNamespace(no_wait=False, handoff_after_story=True), "story-to-pr")
    assert not module.should_wait_for_cell(SimpleNamespace(no_wait=False, handoff_after_story=True), "code-review")
    assert not module.should_wait_for_cell(SimpleNamespace(no_wait=True, handoff_after_story=False), "story-to-pr")


def test_orchestrator_snapshots_helpers(tmp_path: Path) -> None:
    path = CANVAS_SCRIPTS / "run_agent_canvas_factory.py"
    spec = importlib.util.spec_from_file_location("run_agent_canvas_factory", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(CANVAS_SCRIPTS))
    spec.loader.exec_module(module)

    helper_dir = module.snapshot_helpers(tmp_path)

    assert helper_dir == tmp_path / "helpers"
    assert (helper_dir / "update_factory_pr_section.py").exists()


def test_pr_section_replacement_and_status(tmp_path: Path) -> None:
    path = CANVAS_SCRIPTS / "update_factory_pr_section.py"
    spec = importlib.util.spec_from_file_location("update_factory_pr_section", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    artifact = tmp_path / "factory_runs" / "run-1" / "code-review.md"
    artifact.parent.mkdir(parents=True)
    artifact.write_text("Status: changes recommended\n", encoding="utf-8")
    body = "## 1. Story\n\ntext\n\n## 2. Code\n\ntext\n\n## 3. Code Review\n\npending\n\n## 4. QA\n\npending\n"

    replacement = module.code_review_section(tmp_path, artifact)
    updated = module.replace_section(body, "## 3. Code Review", replacement)

    assert "Review status: changes recommended" in updated
    assert "## 4. QA" in updated
    assert "pending\n\n## 4. QA" not in updated


def test_orchestrator_writes_missing_artifact_report(tmp_path: Path) -> None:
    path = CANVAS_SCRIPTS / "run_agent_canvas_factory.py"
    spec = importlib.util.spec_from_file_location("run_agent_canvas_factory", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(CANVAS_SCRIPTS))
    spec.loader.exec_module(module)

    args = SimpleNamespace(repo=tmp_path, run_id="run-1", run_date="2026-07-07")
    entry = {
        "id": "child-1",
        "ui_url": "http://localhost:8000/conversations/child-1",
        "artifact": "factory_runs/run-1/qa.md",
    }

    artifact = module.write_missing_artifact_report(
        args=args,
        cell="qa",
        entry=entry,
        status_response={"execution_status": "error"},
        final_response={"response": ""},
    )

    assert artifact == tmp_path / "factory_runs" / "run-1" / "qa.md"
    text = artifact.read_text(encoding="utf-8")
    assert "Status: needs-human" in text
    assert "Execution status: `error`" in text
    assert "Run date: `2026-07-07`" in text


def test_update_summary_labels_unwaited_idle_children_as_created(tmp_path: Path) -> None:
    path = CANVAS_SCRIPTS / "run_agent_canvas_factory.py"
    spec = importlib.util.spec_from_file_location("run_agent_canvas_factory", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(CANVAS_SCRIPTS))
    spec.loader.exec_module(module)

    module.update_summary(
        tmp_path,
        [
            {
                "name": "qa",
                "id": "child-1",
                "ui_url": "http://localhost:8000/conversations/child-1",
                "artifact": "factory_runs/run-1/qa.md",
                "execution_status": "idle",
            }
        ],
    )

    text = (tmp_path / "children-summary.md").read_text(encoding="utf-8")
    assert "| `qa` | created |" in text


def test_orchestrator_snapshots_prompts_before_delegating() -> None:
    factory = (CANVAS_SCRIPTS / "run_agent_canvas_factory.py").read_text(encoding="utf-8")

    assert "prompt-snapshot" in factory
    assert "snapshot_prompts(run_dir)" in factory
    assert "prompt_root=prompt_root" in factory


def test_launcher_records_parent_conversation_artifact() -> None:
    launcher = (CANVAS_SCRIPTS / "start_agent_canvas_factory.py").read_text(encoding="utf-8")
    assert "parent.conversation.json" in launcher
    assert "--run-date" in launcher
    assert "--require-playwright-qa" in launcher
    assert "--playwright-node-path" in launcher
    assert "--allow-protected-repo" in launcher
    factory = (CANVAS_SCRIPTS / "run_agent_canvas_factory.py").read_text(encoding="utf-8")
    assert "--no-pr-body-sync" in factory
    assert "--no-publish-run-artifacts" in factory
    assert "--handoff-after-story" in factory


def test_qa_prompt_supports_required_playwright() -> None:
    qa_prompt = (ROOT / "agent-canvas" / "prompts" / "workcells" / "qa.md").read_text(encoding="utf-8")
    assert "{{qa_playwright_requirement}}" in qa_prompt
    assert "{{playwright_node_path}}" in qa_prompt
    assert "agent-canvas/scripts/run_petstore_playwright_qa.py" in qa_prompt
    assert "factory_runs/{{run_id}}/helpers/update_factory_pr_section.py" in qa_prompt
    assert "node app/web/tests/catalog-search.playwright.mjs" in qa_prompt
    assert "Playwright is required" in qa_prompt or "When Playwright is required" in qa_prompt
