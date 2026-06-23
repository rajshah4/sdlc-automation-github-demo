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

- Trigger labels/comments: `openhands-qa`
- Status labels: `openhands:ready`, `openhands:in-progress`, `openhands:needs-human`, `openhands:done`
- QA may push focused test/evidence commits to the PR branch when permitted.
- QA does not approve, merge, deploy, or bypass CI.

## Strategy

1. Read the PR goal, diff, linked issue, open spec, and existing test evidence.
2. Classify the change as backend, UI, automation, docs, SRE, or mixed.
3. Read the relevant reference:
   - `references/api-qa-conventions.md` for Python behavior/API changes.
   - `references/webapp-testing.md` for UI-visible changes.
4. Add tests only for changed behavior that lacks coverage.
5. Run the smallest useful validation before broad validation.
6. For UI changes, serve `app/web` and capture browser, screenshot, DOM, or deterministic smoke evidence.
7. Report honestly when a dependency, browser, credential, or service is missing.

Do not run `pip install` or add new QA dependencies during the demo. If a browser or package is missing, fall back to dependency-free smoke checks and document the gap.

## Petstore QA Contracts

- Default catalog search returns only available pets.
- Pending pets can be found only when status is explicitly requested.
- Pending or adopted pets cannot be adopted.
- Fees use integer cents, never floats.
- UI-visible changes need UI evidence.
- Incident remediation must prove pending pets are no longer visible in the available-pet experience.

## Useful Commands

```bash
python3 -m pytest -q app/tests/test_pet_catalog.py
python3 -m pytest -q app/tests/test_adoptions.py
python3 -m pytest -q app/tests/test_cloud_run_app.py
python3 -m pytest -q
python3 -m http.server 4173 --directory app/web
python3 skills/sdlc-qa/scripts/static_ui_smoke.py --url http://localhost:4173
python3 skills/sdlc-qa/scripts/with_server.py --server "python3 -m http.server 4173 --directory app/web" --port 4173 -- python3 skills/sdlc-qa/scripts/static_ui_smoke.py --url http://localhost:4173
```

## Test Generation Rules

- Prefer pytest tests in `app/tests/`.
- Use direct function tests for catalog/adoption behavior.
- Use HTTP or server-level tests only when the changed behavior lives at the boundary.
- Add UI smoke evidence for static UI changes; do not claim visual coverage from unit tests alone.
- Keep tests focused on behavior, not implementation details.

## Report Requirements

- commands run
- tests added or changed
- result summary
- UI evidence for UI behavior
- remaining risk
- whether the open spec acceptance criteria were satisfied
