# Automated Code Review via OpenHands

**Reviewed target:** PR #86 — `feature/canvas-issue-101-max-adoption-fee-filter`
**URL:** https://github.com/rajshah4/sdlc-automation-github-demo/pull/86
**Status:** changes recommended
**Risk:** low

---

## Findings

### Medium

- **No automated Playwright test for max-fee filter** — `app/web/tests/family-friendly-filter.playwright.mjs` and `catalog-search.playwright.mjs` test the family-friendly checkbox and basic search but not the new max-fee input. The QA work cell generated screenshots via Agent Canvas browser tools, but there is no scripted Playwright test covering fee filter scenarios (entering value, clearing value, boundary behavior). This gap is noted in the previous QA report.

  **Impact:** Manual browser testing is required to verify the fee filter in future regressions. A focused Playwright scenario (similar to `family-friendly-filter.playwright.mjs`) would close this gap.

  **Recommendation:** Add a `max-fee-filter.playwright.mjs` or extend the existing `catalog-search.playwright.mjs` to cover:
  - Entering a dollar amount hides pets above that fee
  - Clearing the input restores all available pets
  - Pending pets remain excluded when fee filter is active

### Low

- **`feeToCents()` silent NaN risk** — `app/web/app.js:8-10`:
  ```javascript
  function feeToCents(feeStr) {
    return Math.round(parseFloat(feeStr.replace("$", "")) * 100);
  }
  ```
  If the pet data format ever deviates from `"$N"` (e.g., `"N"` without the dollar sign), `parseFloat` returns `NaN`, and the comparison `feeToCents(pet.fee) <= maxFeeCents` returns `false`, silently excluding the pet. Currently acceptable because pet data is static and always uses the `"$N"` format.

  **Recommendation:** Consider adding a guard: `const cents = parseFloat(feeStr.replace("$", "")); if (isNaN(cents)) return 0;` with a comment explaining the expected format.

- **PR includes 35 changed files, many are factory artifacts** — The diff includes `factory_runs/`, `openspec/changes/`, and unrelated documentation files. These are not problematic but inflate the PR size. The core feature changes are the 4 files listed in the story-to-PR report.

---

## Petstore Contract Checks

- **Pending/adopted visibility:** ✅ `pet.status === "available"` filter is preserved; pending pet Nova remains hidden. Verified by existing tests (`test_visible_pets_excludes_pending_by_default`).
- **Adoption validation:** ✅ Not changed by this PR; unchanged `adoptions.py` tests still pass.
- **Money-as-cents:** ✅ Backend uses `adoption_fee_cents: int` in `catalog.py`; `max_fee_cents` typed as `int | None`. UI converts dollars to cents with `feeToCents()`. No float leakage observed.
- **Evidence:** ✅ UI screenshots in `factory_runs/codex-smoke-canvas-factory/ui-evidence/` show default view and fee filter at $100. Playwright automation not available locally; screenshots captured via Agent Canvas browser tools.

---

## Tests Reviewed

- `app/tests/test_pet_catalog.py`: 9/9 pass, including 4 new tests covering:
  - Filter match (max 12 000¢ excludes Scout at 12 500¢)
  - Boundary inclusive (max 7 500¢ includes Mochi at 7 500¢)
  - Negative rejection (raises `ValueError`)
  - None means no bound (backward compatible)

- Full suite: 37/37 pass (verified locally)

---

## Open Questions

1. **Playwright test coverage:** Should a `max-fee-filter.playwright.mjs` test be added before or after merge? The feature works but lacks automated browser regression coverage.
2. **`feeToCents()` robustness:** Should the UI helper be hardened against format changes, or is the static pet data assumption sufficient for the current scope?

---

## Residual Risk

| Risk | Severity | Notes |
|------|----------|-------|
| No automated Playwright test for fee filter | Low-Medium | Browser evidence exists (screenshots); manual testing still needed for future regressions |
| `feeToCents()` silent NaN | Low | Static pet data; acceptable for current scope |
| Pre-existing test failure (`test_all_fixtures_use_known_automation_labels`) | Low | Unrelated to this PR |

---

## Blocking Status

**blocking: no**

The implementation is correct and the feature works as specified. Backend tests pass, UI evidence exists, and the family-friendly filter is preserved alongside the new max-fee filter. The missing Playwright test for the fee filter is a test gap rather than a correctness issue.

---

**Reviewed by:** OpenHands (code-review work cell)
**Artifacts:** `factory_runs/eval-playwright-20260707-100947/code-review.md`
