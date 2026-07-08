# Automated Code Review via OpenHands

- **Run id:** canvas-verify-full
- **Run date:** 2026-07-07
- **Story:** #88 — Filter pets by max adoption fee
- **Reviewed target:** PR #95 — `agent/issue-88-canvas-verify-full` → `main`
  (https://github.com/rajshah4/sdlc-automation-github-demo/pull/95)
- **Local branch verified at:** `/Users/rajiv.shah/Code/sdlc-automation-github-demo`

Status: changes recommended
Goal: Add optional `max_fee_cents` filter to `search_pets` and expose it in the static Petstore UI
Risk: low

---

## Findings

### [Medium] `app/web/app.js:11` — `parseFloat` is more permissive than `valueAsNumber`

```js
const maxFeeRaw = parseFloat(document.querySelector("#max-fee").value);
```

`parseFloat("5abc")` silently returns `5`; `HTMLInputElement.valueAsNumber` returns `NaN`
for any non-numeric string, which is the correct sentinel for "no value entered."
The `type="number"` browser constraint usually prevents bad strings from reaching this
code, but using `.valueAsNumber` makes the intent explicit and is more idiomatic for
number inputs.

Suggested fix:
```js
const maxFeeRaw = document.querySelector("#max-fee").valueAsNumber;
const maxFeeCents = isFinite(maxFeeRaw) && maxFeeRaw >= 0 ? Math.round(maxFeeRaw * 100) : null;
```

Impact: edge-case parsing robustness; no effect on normal browser usage.

---

### [Medium] Backend and UI disagree on negative-value handling

- **Backend** (`catalog.py:39`): raises `ValueError("max_fee_cents must be zero or a
  positive integer")` for any `max_fee_cents < 0`.
- **UI** (`app.js:12`): silently treats negative input as `null` (filter disabled).
  The HTML `min="0"` prevents browser users from entering negatives, but the
  behaviors diverge for any caller that bypasses the HTML layer.

The story-to-pr assumptions document this intentionally, so it is not a bug. However,
if a future REST layer wraps `search_pets`, clients will encounter a validation error
the UI never exposes. This is worth calling out for the human reviewer.

No immediate action required; document in the OpenSpec design note.

---

### [Low] Missing test for `max_fee_cents=0` edge case

`proposal.md` explicitly states "a max fee of 0 means only free pets (if any exist),
which is valid." No test exercises this boundary. Since all fixture pets have
`adoption_fee_cents > 0`, a `max_fee_cents=0` call returns an empty list — functionally
covered by `test_search_pets_max_fee_below_all_returns_empty(100)` — but an explicit
test at zero would be cleaner and matches the documented edge case.

---

### [Low] No test for `max_fee_cents` combined with a second filter

Each new test passes `max_fee_cents` in isolation. A combination test (e.g.
`search_pets(species="cat", max_fee_cents=8000)`) would confirm filter interaction.
The loop structure makes this very unlikely to regress, but the spec calls out filter
combination as expected behavior.

---

### [Low] Floating-point cents conversion for non-integer dollar values (`app.js:12`)

`Math.round(maxFeeRaw * 100)` is correct for whole-dollar inputs enforced by
`step="1"`. If a caller bypasses the step constraint (e.g. programmatic `.value = "50.005"`),
IEEE 754 float representation can cause `Math.round(50.005 * 100)` to evaluate to
`5000` or `5001` depending on runtime. The `step="1"` HTML attribute makes this
unreachable in normal browser usage; no change required, but worth noting if the input
is ever relaxed to accept cents.

---

## Petstore Contract Checks

- **Pending/adopted visibility:** ✓ — `pet.status === "available"` guard is preserved
  in `renderResults`; Nova (pending) remains hidden under all max-fee values.
- **Pending max-fee filter interaction:** ✓ — Backend `status` filter runs before the
  `max_fee_cents` filter; passing `status="pending"` explicitly would still apply the
  fee filter correctly.
- **Adoption validation:** ✓ — No changes to adoption logic; pending/adopted rejection
  is untouched.
- **Money-as-cents:** ✓ — `adoption_fee_cents` (int), `feeCents` in JS (int), and the
  `max_fee_cents` parameter (int | None) all stay in integer cents. No floats stored.
- **Data consistency:** ✓ — `feeCents` values in `app.js` match `adoption_fee_cents`
  values in `catalog.py` for all four pets (7500, 12500, 4500, 11000).
- **Evidence:** Backend tests pass (13/13). Playwright scenarios are written but
  not yet executed (playwright not installed in the story-to-pr runtime).

---

## Tests and QA

- **Tests reviewed:** `app/tests/test_pet_catalog.py` — 4 new tests added, all pass
  locally (`pytest app/tests/ -v` → 13 passed in 0.01s).
  - `test_search_pets_max_fee_returns_pets_within_budget` — correct fixture names
  - `test_search_pets_max_fee_exact_match_is_inclusive` — ≤ semantics verified
  - `test_search_pets_max_fee_below_all_returns_empty` — correct
  - `test_search_pets_max_fee_negative_raises_value_error` — correct
  - All 9 pre-existing tests continue to pass.
- **Playwright scenarios:** 2 new scenarios in
  `app/web/tests/catalog-search.playwright.mjs` (lines 178–189). **Not executed —
  playwright npm package not installed in the story-to-pr runtime.** QA work cell
  must run these and produce screenshot/video evidence.
- **Missing evidence:** UI behavior is not verified by any executed test. This is the
  primary gap; it is assigned to the QA work cell, not a blocker for human code review.

---

## Open Questions

1. Should the UI show a validation message when a negative value is entered, to match
   the backend's ValueError? Currently it silently ignores out-of-range input.
2. If a REST API endpoint wraps `search_pets` in the future, should `max_fee_cents`
   validation errors return HTTP 400 or 422? The current ValueError maps cleanly to
   either; documenting the intent now would prevent drift.

---

## Residual Risk

- UI evidence gap: Playwright tests are written but unexecuted. QA work cell must
  validate `app/web/app.js` fee-filter rendering and the "clearing restores all pets"
  scenario with screenshots before the PR is merge-ready.
- `parseFloat` permissiveness (medium finding above) is a minor robustness issue;
  no user-visible defect in normal browser usage.
- Overall risk is **low**: the change is additive and opt-in, all existing tests pass,
  and Petstore contracts are maintained.

---

## Blocking Status

**Blocking: no.** No correctness bugs or contract violations found. The medium findings
are robustness and documentation concerns that do not prevent the feature from working
correctly for users. The low findings are test-gap suggestions.

Human reviewer should confirm scope and decide whether to address the medium findings
before merge. The PR is not ready for merge until the QA work cell produces executed
Playwright evidence.

---

## PR Section Update

Command run:
```bash
python3 factory_runs/canvas-verify-full/helpers/update_factory_pr_section.py \
  --repo "/Users/rajiv.shah/Code/sdlc-automation-github-demo" \
  --run-id "canvas-verify-full" \
  --pr https://github.com/rajshah4/sdlc-automation-github-demo/pull/95 \
  --section code-review \
  --artifact factory_runs/canvas-verify-full/code-review.md
```

Result: _see below after execution_
