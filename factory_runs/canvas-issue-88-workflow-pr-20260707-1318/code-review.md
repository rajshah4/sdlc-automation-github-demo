# Automated Code Review via OpenHands

- **Run date**: 2026-07-07
- **Run ID**: canvas-issue-88-workflow-pr-20260707-1318
- **Story**: #88 — Filter pets by maximum adoption fee
- **Reviewed target**: PR #91 — https://github.com/rajshah4/sdlc-automation-github-demo/pull/91
- **Branch**: `agent/issue-88-canvas-issue-88-workflow-pr-20260707-1318`
- **Diff base**: `origin/main` → commit `cfa9fc4`

---

Status: findings
Goal: Add max adoption fee filter to pet catalog backend and static UI.
Risk: low

---

## Findings

### Medium

- **`app/web/app.js` — `feeToCents` silently returns `NaN` for non-standard fee strings**
  `feeToCents(feeStr)` does `parseFloat(feeStr.replace("$", "")) * 100`. Any future pet whose `fee`
  field does not start with `$` (e.g. `"Free"`, `"USD 75"`, or a bare number like `"75"`) will produce
  `NaN`. Because `NaN <= maxFeeCents` is always `false`, that pet will be invisibly hidden whenever a
  max-fee filter is active — a silent exclusion with no error or UI feedback. The current four pets
  all use `"$NN"` format, so this is latent rather than an immediate bug, but it is fragile against
  future data additions.
  **Fix direction**: add a guard — `if (!isFinite(cents)) return true;` (keep pet when fee is
  unparseable) or store fees as integer cents in the JS data to remove the conversion step entirely.

- **`app/web/app.js` — UI does not reject negative max-fee input**
  `<input type="number" min="0" step="1">` specifies `min="0"` as a browser hint, but browsers do not
  prevent a user from typing a negative value directly. When the user enters `-5`, `maxFeeCents`
  becomes `-500` and `feeToCents(pet.fee) <= -500` is false for every pet (all fees > $0), producing
  an empty list with no explanation. The backend correctly raises `ValueError` for negative values but
  the UI has no matching guard.
  **Fix direction**: clamp or discard negative input in `renderResults` before building `maxFeeCents`:
  ```js
  const maxFeeCents = maxFeeInput !== "" && parseFloat(maxFeeInput) >= 0
    ? Math.round(parseFloat(maxFeeInput) * 100)
    : null;
  ```

### Low

- **`app/tests/test_pet_catalog.py:30` — Boundary test does not assert Scout is excluded**
  `test_search_pets_includes_pets_at_exact_fee_boundary` calls `search_pets(max_fee_cents=7500)` and
  asserts `any(pet.name == "Mochi" for pet in results)`. It does not assert that Scout (12500¢ > 7500¢)
  is absent from the result. The filter logic is correct (verified by running all 13 tests), but the
  test provides weaker exclusion coverage than the filter-match test does.
  **Fix direction**: add `assert all(pet.name != "Scout" for pet in results)` to the boundary test,
  or replace with an exact equality check: `assert [p.name for p in results] == ["Mochi", "Pip"]`.

- **`app/tests/test_pet_catalog.py` — No test for `max_fee_cents=0`**
  Zero is a valid non-negative value and distinct in semantics: it means "show only free pets." With
  the current catalog (all fees > $0) `search_pets(max_fee_cents=0)` correctly returns `[]`, but this
  is untested. It is also the most natural input when a user accidentally types `0` in the UI.
  **Fix direction**: add `assert search_pets(max_fee_cents=0) == []` as a single-line test.

---

## Petstore Contract Checks

- **Pending/adopted visibility**: ✅ Preserved. `status="available"` default is unchanged. Nova
  (pending, $110) is excluded from every available search regardless of the max-fee value — confirmed
  in test data and by inspecting the filter chain in `catalog.py`.
- **Adoption validation**: ✅ Unchanged — `create_adoption_order` is not modified.
- **Money as cents**: ✅ Backend parameter is `int | None` with `>= 0` guard. No floats in Python.
  UI converts whole-dollar input with `Math.round(... * 100)` which is correct for integer-dollar
  amounts; `step="1"` discourages fractional entry.
- **Negative fee rejection**: ✅ Backend raises `ValueError("max_fee_cents must be >= 0")` for `-1`.
  Tested and passing.

---

## Tests and QA

### Backend tests — personally run and verified

```
python3 -m pytest app/tests/ -v
```

Result: **13 passed, 0 failed** (0.01 s, Python 3.12, pytest 9.1.1)

New tests added and passing:
- `test_search_pets_filters_by_max_fee` — verifies Mochi + Pip returned, Scout excluded at 12000¢
- `test_search_pets_includes_pets_at_exact_fee_boundary` — verifies inclusive boundary at 7500¢
- `test_search_pets_rejects_negative_max_fee` — verifies `ValueError` on `-1`
- `test_search_pets_no_fee_filter_when_max_fee_none` — verifies `None` disables filter

Existing 9 tests continue to pass unmodified.

### Playwright UI test — not executed

`app/web/tests/max-adoption-fee-filter.playwright.mjs` exists in the branch and covers 5 scenarios
(default view, below-threshold, exact boundary, empty state, clear restores list). Execution requires
a live HTTP server and Playwright installation. This run did not execute it. UI evidence is therefore
asserted by spec, not by runtime screenshot or recording.

**Test gap**: no screenshot or video evidence from this run confirms the UI renders and filters
correctly in a real browser. This is the primary residual risk.

---

## Open Questions

1. **Should the UI reject or silently ignore non-integer dollar inputs?** The `step="1"` hint
   discourages fractional values but does not block them. Is "$75.50" a valid max-fee entry, or
   should the UI round to the nearest dollar before filtering?

2. **Will `max_fee_cents` ever be exposed via an HTTP API?** Currently `search_pets()` is called only
   from Python tests and the UI uses its own static JS data. If a REST endpoint is added later, the
   `max_fee_cents` query parameter will need its own API-layer validation and documentation.

3. **Localization / currency**: the UI placeholder label is `Max fee ($)` hard-coded to USD. Is that
   intentional for this demo, or is a locale-agnostic label preferred?

---

## Residual Risk

- UI filter correctness is unverified by runtime execution in this cell. A passing Playwright run from
  the QA cell (or a manual browser check) is the remaining gate before merge confidence is high.
- `feeToCents` is fragile against future fee-string format changes (medium finding above); no test
  covers a malformed fee string.

---

## Blocking Status

**Blocking: no.**

The backend logic is correct and all 13 tests pass. The two medium findings are robustness concerns
(latent for current static data, not current bugs). The low findings are test-quality gaps, not
defects. The PR should proceed to QA. A human reviewer should assess whether the medium UI findings
warrant a fix before merge.

---

## PR Section Update

Command run:

```bash
python3 factory_runs/canvas-issue-88-workflow-pr-20260707-1318/helpers/update_factory_pr_section.py \
  --repo "/private/tmp/sdlc-agent-canvas-workflow-pr-20260707-1318" \
  --run-id "canvas-issue-88-workflow-pr-20260707-1318" \
  --pr https://github.com/rajshah4/sdlc-automation-github-demo/pull/91 \
  --section code-review \
  --artifact factory_runs/canvas-issue-88-workflow-pr-20260707-1318/code-review.md
```

Result: **success** — PR #91 `## 3. Code Review` section updated to `Review status: findings` with link to this artifact. Exit code 0.
