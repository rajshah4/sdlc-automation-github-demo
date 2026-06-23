---
name: github-automation
description: GitHub event, label, and status-boundary guidance for SDLC Automation Demo work cells.
triggers:
  - github event
  - openhands label
---

# GitHub Automation Boundaries

Use this skill when interpreting GitHub issues, PRs, comments, and labels.

## Trigger Labels

- `openhands-build`
- `openhands-review`
- `openhands-qa`
- `openhands-incident`

## Status Labels

- `openhands:ready`
- `openhands:in-progress`
- `openhands:needs-human`
- `openhands:done`

## Rules

- Event-driven automation is the default; do not poll GitHub.
- Use labels/comments as explicit human intent.
- Avoid result comments that include exact trigger text.
- Remove or replace `openhands:in-progress` when work ends.
- Leave merge and deployment decisions to humans.

