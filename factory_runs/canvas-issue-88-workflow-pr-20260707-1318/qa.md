# QA Report

- **Run ID**: canvas-issue-88-workflow-pr-20260707-1318
- **Run date**: 2026-07-07
- **Story**: #88 — Filter pets by max adoption fee
- **Branch**: `agent/issue-88-canvas-issue-88-workflow-pr-20260707-1318`
- **PR**: https://github.com/rajshah4/sdlc-automation-github-demo/pull/91
- **Overall status**: pass

---

## Changed Files Under Test

| File | Change |
|---|---|
| `app/petstore_app/catalog.py` | Added `max_fee_cents: int \| None = None` parameter to `search_pets()`; inclusive upper-bound predicate; `ValueError` on negative input |
| `app/tests/test_pet_catalog.py` | 4 new focused tests for max-fee behavior |
| `app/web/index.html` | Added `<input id="max-fee" type="number" min="0" step="1">` to toolbar |
| `app/web/app.js` | Added `feeToCents()` helper and max-fee filter predicate; wired `input` listener |
| `app/web/styles.css` | Minor toolbar label width adjustment |
| `app/web/tests/max-adoption-fee-filter.playwright.mjs` | New Playwright test: 5 UI scenarios covering required evidence shape |

---

## 1. Backend Tests

### Command

```bash
python3 -m pytest app/tests/ -v
```

### Result: 13 passed, 0 failed (0.01s)

```
app/tests/test_adoptions.py::test_create_adoption_order_returns_totals_in_cents        PASSED
app/tests/test_adoptions.py::test_create_adoption_order_rejects_pending_pet            PASSED
app/tests/test_adoptions.py::test_create_adoption_order_rejects_invalid_email         PASSED
app/tests/test_adoptions.py::test_create_adoption_order_rejects_negative_donation     PASSED
app/tests/test_pet_catalog.py::test_search_pets_filters_by_species_and_status         PASSED
app/tests/test_pet_catalog.py::test_search_pets_can_find_pending_pets_when_requested  PASSED
app/tests/test_pet_catalog.py::test_search_pets_filters_by_tag                        PASSED
app/tests/test_pet_catalog.py::test_search_pets_validates_max_results[0]              PASSED
app/tests/test_pet_catalog.py::test_search_pets_validates_max_results[51]             PASSED
app/tests/test_pet_catalog.py::test_search_pets_filters_by_max_fee                    PASSED
app/tests/test_pet_catalog.py::test_search_pets_includes_pets_at_exact_fee_boundary   PASSED
app/tests/test_pet_catalog.py::test_search_pets_rejects_negative_max_fee              PASSED
app/tests/test_pet_catalog.py::test_search_pets_no_fee_filter_when_max_fee_none       PASSED
```

New tests for issue #88 (all pass):
- `test_search_pets_filters_by_max_fee` — below-threshold filter: max 12000¢ ($120) shows Mochi ($75) + Pip ($45), excludes Scout ($125)
- `test_search_pets_includes_pets_at_exact_fee_boundary` — inclusive boundary: max 7500¢ ($75) includes Mochi at exactly $75
- `test_search_pets_rejects_negative_max_fee` — negative `max_fee_cents` raises `ValueError`
- `test_search_pets_no_fee_filter_when_max_fee_none` — `None` produces identical results to the unfiltered default

---

## 2. Playwright UI Tests

`scripts/run_petstore_playwright_qa.py` does not exist on this branch; test was run directly via the existing test file.

### Command

```bash
NODE_PATH="/Users/rajiv.shah/Code/agent-canvas/node_modules" \
python3 skills/sdlc-qa/scripts/with_server.py \
  --server "python3 -m http.server 4173 --directory app/web" \
  --port 4173 \
  -- node app/web/tests/max-adoption-fee-filter.playwright.mjs \
       --url http://localhost:4173 \
       --artifact-dir factory_runs/canvas-issue-88-workflow-pr-20260707-1318/playwright-artifacts
```

### Result: pass — 5 of 5 scenarios passed

```
Playwright max-adoption-fee-filter QA passed
Screenshot: …/playwright-artifacts/max-fee-below-threshold.png
Video:      …/playwright-artifacts/max-adoption-fee-filter.webm
GIF:        …/playwright-artifacts/max-adoption-fee-filter.gif
Report:     …/playwright-artifacts/qa-report.md
```

### Scenarios Exercised

| # | Scenario | Result |
|---|---|---|
| 1 | Default view shows all 3 available pets (Mochi, Scout, Pip) with no max-fee set | ✅ pass |
| 2 | Below-threshold filter: max fee $80 shows Mochi ($75) + Pip ($45), excludes Scout ($125) | ✅ pass |
| 3 | Exact-boundary filter: max fee $75 includes Mochi at exactly the boundary (inclusive) | ✅ pass |
| 4 | Max fee $44 (below all available fees) shows empty-state message | ✅ pass |
| 5 | Clearing max-fee input restores the full 3-pet available list | ✅ pass |

Scenarios 2 and 3 satisfy the Playwright requirement: at least one below-threshold filter and one exact-boundary scenario.

### Browser Evidence

| Artifact | Path |
|---|---|
| Screenshot (below-threshold filter applied) | `factory_runs/canvas-issue-88-workflow-pr-20260707-1318/playwright-artifacts/max-fee-below-threshold.png` |
| Video (full 5-scenario run) | `factory_runs/canvas-issue-88-workflow-pr-20260707-1318/playwright-artifacts/max-adoption-fee-filter.webm` |
| GIF preview | `factory_runs/canvas-issue-88-workflow-pr-20260707-1318/playwright-artifacts/max-adoption-fee-filter.gif` |
| Playwright report | `factory_runs/canvas-issue-88-workflow-pr-20260707-1318/playwright-artifacts/qa-report.md` |

Evidence is live browser execution (Chromium via Playwright, Node v25.6.1).

---

## 3. Test Files Added or Changed

| File | Status | Note |
|---|---|---|
| `app/tests/test_pet_catalog.py` | Modified (by code cell) | 4 new max-fee tests; all 13 pass |
| `app/web/tests/max-adoption-fee-filter.playwright.mjs` | New (by code cell) | 5-scenario Playwright spec; all pass |

No QA-owned test files were added or modified during this QA run — both files were already present on the branch from the code cell. Coverage is sufficient; no new tests required.

---

## 4. Residual Risk

| Risk | Severity | Notes |
|---|---|---|
| Fee data is hard-coded in `PETS` tuple | Low | Acceptable for demo; changing fees without updating Playwright thresholds would break scenario 2/3 |
| UI input is in whole dollars; cents conversion is client-side only | Low | Behavior is correct per product rule (integer cents, UI in dollars). No server-side API for the UI means no mismatch path |
| Nova (pending) fee $110 is never shown; its presence in PETS is untested at the boundary | Low | Product rule is that pending pets cannot be adopted or shown in default results; existing adoption tests cover the pending guard |
| Empty-state message text is exact-matched in Playwright | Low | Brittle if copy changes — acceptable for demo scope |

No high-severity residual risks identified.

---

## 5. Merge-Readiness Recommendation

**Recommended: merge-ready pending human review approval.**

All acceptance criteria from story #88 are met:
- Blank max-fee input preserves existing catalog behavior ✅
- Max-fee filtering is inclusive at the threshold ✅
- Pending pets remain hidden ✅
- Negative backend max-fee values are rejected ✅

Backend: 13/13 tests pass. UI: 5/5 Playwright scenarios pass with live browser evidence (screenshot, video, GIF).

Human reviewer should confirm the UI rendering and interaction feel are acceptable before merging.

---

## 6. PR Section Update

### Command

```bash
python3 factory_runs/canvas-issue-88-workflow-pr-20260707-1318/helpers/update_factory_pr_section.py \
  --repo "/private/tmp/sdlc-agent-canvas-workflow-pr-20260707-1318" \
  --run-id "canvas-issue-88-workflow-pr-20260707-1318" \
  --pr https://github.com/rajshah4/sdlc-automation-github-demo/pull/91 \
  --section qa \
  --artifact factory_runs/canvas-issue-88-workflow-pr-20260707-1318/qa.md
```

Result: **exit 0 — success**. PR section `## 4. QA` updated at https://github.com/rajshah4/sdlc-automation-github-demo/pull/91 with QA status, evidence paths, and artifact link.
