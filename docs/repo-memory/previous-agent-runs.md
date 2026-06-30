# Previous Agent Runs

This file is curated episodic memory for the live demo. It should contain durable lessons from previous OpenHands runs, not secret values, private runtime identifiers, or issue-specific scratch notes.

## Validated Build Run

- Date: 2026-06-23
- Issue: `rajshah4/sdlc-automation-github-demo#1`
- Result: OpenHands opened PR #2 for the max adoption fee filter and posted a completion summary.
- Reusable lesson: sparse catalog requests should start from `app/petstore_app/catalog.py`, `app/tests/test_pet_catalog.py`, and OpenSpec-style artifacts under `openspec/changes/`.

## QA Evidence Pattern

- Prior QA report: `docs/qa-reports/family-friendly-filter.md`
- Browser evidence example: `docs/qa-reports/family-friendly-filter-playwright/qa-report.md`
- Reusable lesson: UI-visible changes should include a deterministic smoke path and, when available, screenshot/GIF/video evidence.

## Automation Shape

- Active GitHub work cells are label-only and skip items already marked `openhands:done`.
- Reusable lesson: avoid comment-trigger loops in customer demos; labels make human control visible.
- Keep raw runtime proof and one-off debugging notes in local operator notes, not in the pushed demo repo.
