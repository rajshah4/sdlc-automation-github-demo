#!/usr/bin/env python3
"""Scaffold a delegated Agent Canvas workflow in a target repository."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]


def write_if_missing(path: Path, text: str, *, force: bool) -> bool:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and not force:
        return False
    path.write_text(text, encoding="utf-8")
    return True


def supervisor_prompt(name: str) -> str:
    return f"""# {name} Supervisor

You are the parent Agent Canvas conversation for this delegated workflow.

The human starts only this parent conversation. Orchestrate child conversations,
collect their artifacts, apply gate logic, and write one lifecycle report. Do
not perform the full lifecycle silently inside the parent conversation.

## Inputs

- Run id: `{{{{run_id}}}}`
- Repository: `{{{{repo_slug}}}}`
- Local repository path: `{{{{repo_path}}}}`
- Request title: `{{{{request_title}}}}`
- Request body: `{{{{request_body}}}}`

## Operating Rules

1. Keep humans in control of scope, credentials, review, merge, deployment, and
   production changes.
2. Give each child a self-contained prompt.
3. Record every child id, UI URL, final response, and artifact under
   `factory_runs/{{{{run_id}}}}/`.
4. Stop or mark `needs-human` when a child reports unsafe scope, missing
   credentials, failed validation, or unresolved product/security questions.

## Final Report

Write `factory_runs/{{{{run_id}}}}/lifecycle-report.md` with the child table,
artifact links, gate decisions, and exact next human action.
"""


def workcell_prompt(name: str) -> str:
    title = name.replace("-", " ").title()
    return f"""# {title} Work Cell

You are a delegated Agent Canvas child conversation.

## Inputs

- Run id: `{{{{run_id}}}}`
- Repository: `{{{{repo_slug}}}}`
- Local repository path: `{{{{repo_path}}}}`
- Request title: `{{{{request_title}}}}`
- Request body: `{{{{request_body}}}}`

## What You Do

Use `{{{{repo_path}}}}` as the only working tree. Do the bounded work for this
cell, prefer deterministic scripts and repo-local skills, and write a durable
artifact for the supervisor.

## Human Control

Do not merge, approve your own work, bypass branch protection, mutate
production, or reveal secrets.

## Output Contract

Write `factory_runs/{{{{run_id}}}}/{name}.md`.

Final response format:

```text
status: done | needs-human | failed
artifact: factory_runs/{{{{run_id}}}}/{name}.md
summary: <five or fewer bullets>
next_gate: <next-cell-or-stop>
```
"""


def build_blueprint(name: str, cells: list[str]) -> dict[str, object]:
    return {
        "name": name,
        "run_directory": "factory_runs/{{run_id}}",
        "supervisor": {
            "prompt": "agent-canvas/prompts/supervisor.md",
            "report": "factory_runs/{{run_id}}/lifecycle-report.md",
        },
        "cells": [
            {
                "name": cell,
                "prompt": f"agent-canvas/prompts/workcells/{cell}.md",
                "artifact": f"factory_runs/{{{{run_id}}}}/{cell}.md",
                "continue_on": ["done"],
                "next": cells[index + 1 : index + 2],
            }
            for index, cell in enumerate(cells)
        ],
        "human_gates": ["scope", "credentials", "review", "merge", "deployment"],
    }


def scaffold(args: argparse.Namespace) -> int:
    target = args.target.resolve()
    cells = args.cells or ["plan", "build", "review", "qa"]
    created: list[str] = []
    skipped: list[str] = []

    files = {
        target / "agent-canvas" / "factory-blueprint.json": json.dumps(
            build_blueprint(args.name, cells), indent=2
        )
        + "\n",
        target / "agent-canvas" / "prompts" / "supervisor.md": supervisor_prompt(args.name),
    }
    for cell in cells:
        files[target / "agent-canvas" / "prompts" / "workcells" / f"{cell}.md"] = workcell_prompt(cell)

    for path, text in files.items():
        if write_if_missing(path, text, force=args.force):
            created.append(str(path))
        else:
            skipped.append(str(path))

    print(json.dumps({"created": created, "skipped": skipped}, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", type=Path, required=True, help="target repository")
    parser.add_argument("--name", default="delegated-sdlc-factory", help="workflow name")
    parser.add_argument("--cells", nargs="+", help="ordered work-cell names")
    parser.add_argument("--force", action="store_true", help="overwrite existing scaffold files")
    return parser


def main() -> int:
    return scaffold(build_parser().parse_args())


if __name__ == "__main__":
    raise SystemExit(main())
