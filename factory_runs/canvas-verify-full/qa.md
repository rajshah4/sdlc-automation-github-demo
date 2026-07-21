# QA Run Report

- **Run id:** canvas-verify-full
- **Run date:** 2026-07-07
- **Story issue:** #88 — Filter pets by max adoption fee
- **Branch:** `agent/issue-88-canvas-verify-full`
- **PR:** https://github.com/rajshah4/sdlc-automation-github-demo/pull/95
- **Workcell:** qa (delegated Agent Canvas conversation)

---

## Status: pass

All focused and broader tests pass. Playwright browser evidence confirms correct UI behavior including the inclusive exact-boundary case.

---

## Changed Files Reviewed

| File | Change type | Verified |
| --- | --- | --- |
| `app/petstore_app/catalog.py` | Added `max_fee_cents` param + ValueError guard | ✅ unit tests pass |
| `app/tests/test_pet_catalog.py` | 4 new max-fee tests added | ✅ all 9 tests pass |
| `app/web/index.html` | Added "Max adoption fee ($)" number input | ✅ browser evidence |
| `app/web/app.js` | Added `feeCents` data + max-fee filter in `renderResults` | ✅ browser evidence |
| `app/web/tests/catalog-search.playwright.mjs` | 2 new fee-filter browser scenarios added | ✅ already in branch |
| `app/web/tests/max-adoption-fee-filter.playwright.mjs` | **Created by this QA run** (missing from feature commit; required by wrapper) | ✅ 4 scenarios pass |

---

## Commands Run

### 1. Focused backend tests

```bash
python3 -m pytest app/tests/test_pet_catalog.py -v
```

**Result:** 9/9 passed (0.01s)

```
app/tests/test_pet_catalog.py::test_search_pets_max_fee_returns_pets_within_budget PASSED
app/tests/test_pet_catalog.py::test_search_pets_max_fee_exact_match_is_inclusive PASSED
app/tests/test_pet_catalog.py::test_search_pets_max_fee_below_all_returns_empty PASSED
app/tests/test_pet_catalog.py::test_search_pets_max_fee_negative_raises_value_error PASSED
```

### 2. Broader test suite

```bash
python3 -m pytest app/tests/ tests/ --ignore=tests/test_live_connections_preflight.py -v
```

**Result:** 65/65 passed (0.51s). No regressions introduced.

### 3. Playwright deterministic wrapper

```bash
NODE_PATH=/opt/homebrew/lib/node_modules \
  python3 agent-canvas/scripts/run_petstore_playwright_qa.py \
    --artifact-dir factory_runs/canvas-verify-full/playwright-artifacts
```

Note: `--playwright-node-path` was omitted (no value provided in run inputs). `NODE_PATH` was set via shell environment to `/opt/homebrew/lib/node_modules` where Playwright 1.x is globally installed (`/opt/homebrew/bin/playwright`). The wrapper inherits `os.environ` and forwards it to the subprocess.

**Result:** exit code 0 — pass

Wrapper invoked `max-adoption-fee-filter.playwright.mjs` against a temporary HTTP server on a free local port.

---

## Playwright Evidence

**Test file:** `app/web/tests/max-adoption-fee-filter.playwright.mjs`

**Scenarios exercised:**

| # | Scenario | Result |
| --- | --- | --- |
| 1 | Baseline: all three available pets shown before any fee filter | ✅ pass |
| 2 | **Below-threshold** — $80 limit: Mochi ($75) and Pip ($45) shown; Scout ($125) hidden | ✅ pass |
| 3 | **Exact-boundary** — $75 limit: Mochi ($75 = limit, inclusive) and Pip ($45) shown; Scout ($125) excluded | ✅ pass |
| 4 | Below all — $10 limit: empty-state message shown | ✅ pass |
| 5 | Clear fee: removing limit restores all three available pets | ✅ pass |

**Artifacts:**

| Artifact | Path |
| --- | --- |
| Screenshot: below-threshold ($80) | `factory_runs/canvas-verify-full/playwright-artifacts/fee-below-threshold.png` |
| Screenshot: exact-boundary ($75) | `factory_runs/canvas-verify-full/playwright-artifacts/fee-exact-boundary.png` |
| Screenshot: fee cleared | `factory_runs/canvas-verify-full/playwright-artifacts/fee-cleared.png` |
| Video | `factory_runs/canvas-verify-full/playwright-artifacts/max-adoption-fee-filter.webm` |
| GIF preview | `factory_runs/canvas-verify-full/playwright-artifacts/max-adoption-fee-filter.gif` |
| Playwright sub-report | `factory_runs/canvas-verify-full/playwright-artifacts/qa-report.md` |

**Visual confirmation (below-threshold, $80):** Screenshot `fee-below-threshold.png` shows the "Max adoption fee ($)" input field with value 80; results list displays Mochi ($75) and Pip ($45) only — Scout ($125) is correctly absent.

**Visual confirmation (exact-boundary, $75):** Screenshot `fee-exact-boundary.png` shows the input at 75; Mochi ($75) is present (inclusive boundary correct), Pip ($45) is present, Scout ($125) is absent.

---

## Test Files Added or Changed

| File | Action | Reason |
| --- | --- | --- |
| `app/web/tests/max-adoption-fee-filter.playwright.mjs` | **Created** during this QA run | The `run_petstore_playwright_qa.py` wrapper referenced this file but it was not in the feature commit. Added to provide the focused fee-filter Playwright test with all required scenarios including the exact-boundary case. Must be committed with the branch. |
| `app/tests/test_pet_catalog.py` | Verified (4 new tests were in feature commit) | All 4 new max-fee tests written by the feature workcell pass. |

---

## Acceptance Criteria Verification

From the story and PR body:

| Criterion | Verified |
| --- | --- |
| Blank max-fee input keeps existing catalog behavior | ✅ Playwright scenario 5 (clear fee restores 3 pets) |
| Max-fee filtering is inclusive at the threshold | ✅ Backend test `test_search_pets_max_fee_exact_match_is_inclusive`; Playwright scenario 3 (exact-boundary $75) |
| Pending pets remain hidden | ✅ Backend tests for status filter; Nova (pending) never appears in any Playwright scenario |
| Negative backend max-fee values are rejected | ✅ Backend test `test_search_pets_max_fee_negative_raises_value_error`; UI guards against negative input via `maxFeeRaw >= 0` check in app.js |

---

## Residual Risk

| Risk | Severity | Notes |
| --- | --- | --- |
| `max-adoption-fee-filter.playwright.mjs` created in this QA run | Low | File was referenced by `run_petstore_playwright_qa.py` but missing from the feature commit. Must be staged and pushed before merge. Covered in commit below. |
| No negative-value UI validation in `index.html` | Low | `input[type=number][min=0]` prevents negative entry in browser; app.js also guards with `maxFeeRaw >= 0`. Backend raises `ValueError` for negative values. Coverage is adequate. |
| Fee display unit mismatch between backend and UI | Informational | Backend stores and filters in integer cents; UI input and display use dollars. The conversion (`Math.round(maxFeeRaw * 100)`) is correct but not independently tested. Low risk given simple arithmetic. |
| `catalog-search.playwright.mjs` also has fee scenarios | Informational | The original Playwright file gained 2 fee scenarios from the feature commit. Those cover `$100` below-threshold and clear. The new focused file covers exact-boundary; no overlap issues. |

---

## Merge-Readiness Recommendation

**Recommendation: ready for human review and merge.**

All 65 automated tests pass. Playwright browser evidence confirms both the below-threshold filter and the inclusive exact-boundary case. The new UI input renders correctly, filters results client-side, and clears gracefully. Pending pet exclusion is unaffected. One file (`max-adoption-fee-filter.playwright.mjs`) was created during this QA run and must be committed to the branch — the commit is recorded below.

---

## PR Section Update

### Command

```bash
python3 factory_runs/canvas-verify-full/helpers/update_factory_pr_section.py \
  --repo "/Users/rajiv.shah/Code/sdlc-automation-github-demo" \
  --run-id "canvas-verify-full" \
  --pr https://github.com/rajshah4/sdlc-automation-github-demo/pull/95 \
  --section qa \
  --artifact factory_runs/canvas-verify-full/qa.md
```

### Result

Exit code 0 — success. PR #95 `## 4. QA` section updated with status and artifact link.
