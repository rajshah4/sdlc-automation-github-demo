# Playwright QA Report: Max Adoption Fee Filter

Status: pass

## Target

- Change: `Max fee ($)` numeric input filters available pets by adoption fee.
- Browser runner: Playwright through `scripts/run_petstore_playwright_qa.py`.

## Browser Scenarios

- [x] Default view shows all 3 available pets with no max-fee filter.
- [x] Max fee `$80` shows Mochi and Pip, excluding Scout.
- [x] Max fee `$75` includes Mochi at exactly the boundary.
- [x] Max fee `$44` shows the empty-state message.
- [x] Clearing max fee restores the full available-pet list.

## Artifacts

- Screenshot: `max-fee-below-threshold.png`
- Video: `max-adoption-fee-filter.webm`
- GIF preview: `max-adoption-fee-filter.gif`

## Reproduction Command

```bash
python3 scripts/run_petstore_playwright_qa.py \
  --artifact-dir factory_runs/agent-canvas-factory-20260707-115942/playwright-artifacts \
  --playwright-node-path /path/to/node_modules
```

## Notes

- Pet fees: Mochi `$75`, Scout `$125`, Pip `$45`.
- Nova is pending and never appears in the available-pets experience.
- Boundary behavior is inclusive.
- The scenario set stays scoped to the max-fee story.
