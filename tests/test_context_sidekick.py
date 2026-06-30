from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SIDEKICK = ROOT / "skills" / "sdlc-context-sidekick"


def run_script(name: str) -> str:
    result = subprocess.run(
        [
            sys.executable,
            str(SIDEKICK / "scripts" / name),
            "--jira-key",
            "KAN-123",
            "--title",
            "Available pets list still shows unavailable animals",
            "--body",
            "Customers say the available pets page includes animals that should not be adoptable.",
        ],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    return result.stdout


def test_context_brief_avoids_workflow_skill_context() -> None:
    output = run_script("build_context_brief.py")

    assert "CONTEXT_BRIEF" in output
    assert "docs/wiki/petstore-catalog-availability.md" in output
    assert "docs/logs/pending-pet-visible.ndjson" in output
    assert "app/petstore_app/catalog.py" in output
    assert "skills/sdlc-story" not in output


def test_fanout_scouts_split_context_and_stay_bounded() -> None:
    output = run_script("fanout_context_scouts.py")

    assert "CONTEXT_SCOUT_FANOUT" in output
    assert "Launch: docs-scout, logs-scout, and repo-scout started together" in output
    assert "SCOUT_RESULT docs-scout" in output
    assert "SCOUT_RESULT logs-scout" in output
    assert "SCOUT_RESULT repo-scout" in output
    assert "CONTEXT_BRIEF" in output
    assert "no other skills" in output
    assert "skills/sdlc-story" not in output
