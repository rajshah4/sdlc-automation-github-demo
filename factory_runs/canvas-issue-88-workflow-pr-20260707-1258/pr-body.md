## 1. Story

Closes #88

Story: filter pets by maximum adoption fee

As an adoption coordinator, I want to filter available pets by maximum adoption fee so families can find pets that fit their budget.

Acceptance focus:

- Blank max-fee input keeps the existing catalog behavior.
- Max-fee filtering is inclusive at the threshold.
- Pending pets remain hidden.
- Negative backend max-fee values are rejected.

## 2. Code

Built the max adoption fee filter across the backend catalog and static Petstore UI.

Key files:

- `app/petstore_app/catalog.py`
- `app/tests/test_pet_catalog.py`
- `app/web/index.html`
- `app/web/app.js`
- `app/web/tests/max-adoption-fee-filter.playwright.mjs`

Implementation report: `factory_runs/canvas-issue-88-workflow-pr-20260707-1258/story-to-pr.md`

## 3. Code Review

Review status: pending

Review report: _pending_

## 4. QA

QA status: pending

Validation:

- `python3 -m pytest -q`
- `python3 scripts/run_petstore_playwright_qa.py --artifact-dir factory_runs/<run-id>/playwright-artifacts --playwright-node-path <playwright-node-path>`

Evidence:

- QA report: _pending_
- Screenshot: _pending_
- GIF: _pending_
- Video: _pending_

QA report: _pending_
