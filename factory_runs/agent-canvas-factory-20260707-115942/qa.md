# QA Workcell Report

Run ID: `agent-canvas-factory-20260707-115942`
Run date: 2026-07-07

## Result

Status: pass

## Commands

```bash
python3 -m pytest -q
```

```bash
python3 scripts/run_petstore_playwright_qa.py \
  --artifact-dir factory_runs/agent-canvas-factory-20260707-115942/playwright-artifacts \
  --playwright-node-path /path/to/node_modules
```

## Backend Validation

The full local Python suite passed after the factory hardening changes:

```text
59 passed
```

The suite includes focused catalog tests for:

- max-fee matching
- inclusive exact-boundary behavior
- negative fee rejection
- no-fee passthrough
- existing status, species, tag, adoption, telemetry, and factory orchestration
  behavior

## Browser Validation

The Playwright workcell ran the static Petstore UI and captured browser evidence
for five scenarios:

| Scenario | Result |
| --- | --- |
| Default view shows all available pets | pass |
| Max fee `$80` shows Mochi and Pip, excluding Scout | pass |
| Max fee `$75` includes Mochi at the exact boundary | pass |
| Max fee `$44` shows the empty state | pass |
| Clearing the input restores all available pets | pass |

## Evidence

| Artifact | Path |
| --- | --- |
| QA report | `playwright-artifacts/qa-report.md` |
| Screenshot | `playwright-artifacts/max-fee-below-threshold.png` |
| GIF | `playwright-artifacts/max-adoption-fee-filter.gif` |
| Video | `playwright-artifacts/max-adoption-fee-filter.webm` |

## Residual Risk

The feature is ready for human review. The remaining decisions are product and
release gates: whether the scope matches story #88, when to convert the draft
PR to ready-for-review, when to merge, and when to deploy.
