---
name: sdlc-qa
description: Petstore-specific QA and test generation guidance for GitHub PR automation.
triggers:
  - openhands-qa
  - qa changes
  - test generation
---

# SDLC QA

Use this skill when OpenHands validates changed behavior or adds QA/test evidence for a PR.

## Strategy

1. Read the PR goal and diff.
2. Classify the change as backend, UI, automation, docs, or incident support.
3. Add tests only for behavior that lacks coverage.
4. Run the smallest validation first.
5. For UI changes, serve `app/web` and capture browser or DOM evidence.
6. Report honestly when a dependency, browser, credential, or service is missing.

## Useful Commands

```bash
python3 -m pytest -q app/tests/test_pet_catalog.py
python3 -m pytest -q app/tests/test_adoptions.py
python3 -m pytest -q
python3 -m http.server 4173 --directory app/web
python3 .agents/skills/sdlc-qa/scripts/static_ui_smoke.py --url http://localhost:4173
```

## Report Requirements

- commands run
- tests added or changed
- result summary
- UI evidence for UI behavior
- remaining risk

