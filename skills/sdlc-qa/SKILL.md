---
name: sdlc-qa
description: Build or extend the automated test suite for GitHub PRs in the SDLC Automation Demo, including Petstore API tests, UI evidence, and deterministic QA reports.
triggers:
  - openhands-qa
  - qa changes
  - test generation
  - automated qa
---

# SDLC QA

Use this skill when OpenHands validates changed behavior, adds focused tests, or produces QA evidence for a GitHub PR.

This skill is based on the automated QA demo pattern: understand the changed behavior, run the real software where practical, add tests only where coverage is missing, and report evidence honestly.

## GitHub Boundaries

- Trigger label: `openhands-qa`
- Status labels: `openhands:ready`, `openhands:in-progress`, `openhands:needs-human`, `openhands:done`
- QA may push focused test/evidence commits to the PR branch when permitted.
- QA does not approve, merge, deploy, or bypass CI.

## Strategy

0. Use `skills/sdlc-context-reuse/SKILL.md` or `scripts/build_context_reuse_report.py` to reuse durable context, prior QA reports, and targeted repo search before broad exploration.
1. Read the PR diff, changed files, linked issue, OpenSpec-style change folder, and existing test evidence. Treat the diff as the source of truth; the PR body may be sparse.
2. Classify the change as backend, UI, automation, docs, SRE, or mixed.
3. Read the relevant reference:
   - `references/api-qa-conventions.md` for Python behavior/API changes.
   - `references/webapp-testing.md` for UI-visible changes.
4. Add tests only for changed behavior that lacks coverage.
5. Run the smallest useful validation before broad validation.
6. For UI changes, infer browser scenarios from the diff and run the real UI through Playwright or BrowserToolSet when available.
7. Capture browser evidence: screenshot, video, GIF preview when possible, selectors/roles used, and a concise summary report.
8. Report honestly when a dependency, browser, credential, or service is missing.

Do not run `pip install` or add new QA dependencies during the demo. If a browser or package is missing, fall back to dependency-free smoke checks and document the gap.
Do not install Playwright inside a timed live automation run. Use it when the runtime already provides Playwright or BrowserToolSet. The checked-in example at `app/web/tests/catalog-search.playwright.mjs` shows the expected browser-evidence shape.

## Diff-Driven UI Inference

The PR author should not have to write test instructions. For UI-visible changes,
derive scenarios from:

- changed labels, controls, buttons, validation messages, and aria-live regions
- changed selectors or element IDs
- changed fixture/data values and rendered states
- changed product rules from the linked issue or OpenSpec-style change artifacts
- existing Petstore rules such as available-only default search and integer-cent fees

When a PR adds a UI control, test the natural workflow for that control:
default state, one successful interaction, one boundary/empty state when
applicable, and one validation/error path when applicable.

## Petstore QA Contracts

- Default catalog search returns only available pets.
- Pending pets can be found only when status is explicitly requested.
- Pending or adopted pets cannot be adopted.
- Fees use integer cents, never floats.
- UI-visible changes need UI evidence.
- Incident remediation must prove pending pets are no longer visible in the available-pet experience.

## UI Artifact Contract

For UI-visible PRs, aim for the automated QA demo shape:

- generate or update a Playwright spec/smoke script under the relevant UI test folder
- run the static UI with `skills/sdlc-qa/scripts/with_server.py`
- capture a screenshot
- record browser video when Playwright supports it
- convert video to a small GIF when `ffmpeg` is available
- write a `qa-report.md` summary
- commit lightweight generated specs and demo artifacts to the PR branch when useful
- post a PR comment with inline GIF or artifact links, commands run, pass/fail status, and residual risk

If Playwright is unavailable, use dependency-free DOM/static checks as fallback
evidence, but say clearly that browser interaction was not exercised.

## Useful Commands

```bash
python3 -m pytest -q app/tests/test_pet_catalog.py
python3 -m pytest -q app/tests/test_adoptions.py
python3 -m pytest -q app/tests/test_cloud_run_app.py
python3 -m pytest -q
python3 -m http.server 4173 --directory app/web
python3 skills/sdlc-qa/scripts/static_ui_smoke.py --url http://localhost:4173
python3 skills/sdlc-qa/scripts/with_server.py --server "python3 -m http.server 4173 --directory app/web" --port 4173 -- python3 skills/sdlc-qa/scripts/static_ui_smoke.py --url http://localhost:4173
python3 skills/sdlc-qa/scripts/with_server.py --server "python3 -m http.server 4173 --directory app/web" --port 4173 -- python3 skills/sdlc-qa/scripts/run_playwright_ui_demo.py --url http://localhost:4173 --artifact-dir /tmp/sdlc-petstore-playwright/catalog-search
```

## Test Generation Rules

- Prefer pytest tests in `app/tests/`.
- Use direct function tests for catalog/adoption behavior.
- Use HTTP or server-level tests only when the changed behavior lives at the boundary.
- Add Playwright/browser evidence for static UI changes when available; do not claim visual coverage from unit tests or DOM inspection alone.
- Keep tests focused on behavior, not implementation details.

## Report Requirements

- commands run
- tests added or changed
- result summary
- UI evidence for UI behavior, including GIF/screenshot/report links when available
- remaining risk
- whether the OpenSpec-style acceptance criteria were satisfied
