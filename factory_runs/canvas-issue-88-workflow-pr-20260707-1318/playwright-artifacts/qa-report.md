# Playwright QA Report: Max Adoption Fee Filter (Issue #88)

Status: pass

## Target

- URL: http://localhost:4173
- Change: Max fee ($) numeric input filters available pets by adoption fee

## Browser Scenarios

- [x] Default view shows all 3 available pets with no max-fee filter
- [x] Below-threshold filter: max fee $80 shows Mochi ($75) and Pip ($45), excludes Scout ($125)
- [x] Exact-boundary filter: max fee $75 includes Mochi at exactly $75 (inclusive)
- [x] Max fee $44 (below all available pets) shows the empty-state message
- [x] Clearing max-fee input restores the full 3-pet available list

## Artifacts

- Screenshot: max-fee-below-threshold.png
- Video: max-adoption-fee-filter.webm
- GIF preview: max-adoption-fee-filter.gif

## Commands

```bash
NODE_PATH=/Users/rajiv.shah/Code/agent-canvas/node_modules \
python3 skills/sdlc-qa/scripts/with_server.py \
  --server "python3 -m http.server 4173 --directory app/web" \
  --port 4173 \
  -- node app/web/tests/max-adoption-fee-filter.playwright.mjs \
     --url http://localhost:4173 \
     --artifact-dir /private/tmp/sdlc-agent-canvas-workflow-pr-20260707-1318/factory_runs/canvas-issue-88-workflow-pr-20260707-1318/playwright-artifacts
```

## Notes

- Pet fees: Mochi=$75, Scout=$125, Pip=$45. Nova is pending and never appears.
- Boundary is inclusive: a pet whose fee equals the max is shown (tested at $75 = Mochi's exact fee).
- The test stays scoped to the max-fee story; unrelated catalog filters are covered elsewhere.
