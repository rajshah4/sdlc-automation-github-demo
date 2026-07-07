# Automated Code Review via OpenHands

**Run ID:** `codex-smoke-canvas-factory`
**Story:** Issue #101 — Filter pets by max adoption fee
**Reviewed target:** PR #86 — `feature/canvas-issue-101-max-adoption-fee-filter` → `main`
**PR URL:** https://github.com/rajshah4/sdlc-automation-github-demo/pull/86
**Status:** draft
**Review date:** 2026-06-30

---

Status: findings
Goal: Add optional max adoption fee filter to pet catalog backend and UI
Risk: low

---

## Findings

### Important

**[Important] `tests/test_github_label_fixtures.py:50` — Pre-existing failing test ships with this PR**

`test_all_fixtures_use_known_automation_labels` fails with `KeyError: 'label'` on both
`main` and this branch. The PR is not the cause, but merging without addressing it means
`28 passed, 1 failed` continues to be the baseline. Human reviewer should confirm this
is deliberately baselined or open a separate issue to fix it before merging.

Verified locally: `uv run pytest -q` → `28 passed, 1 failed`.

---

**[Important] No CI pipeline configured — no automated safety net on this PR**

`gh pr view 86 --json statusCheckRollup` returns `[]`. There are no automated checks
running on the PR. The only verification is tests run locally. Human reviewer is the
sole gate before merge.

---

### Medium

**[Medium] `app/web/app.js:11-13` — Inline `maxFeeCents` computation duplicates `feeToCents` logic**

`feeToCents(feeStr)` strips `$` and rounds, but `maxFeeCents` in `renderResults()` is
computed inline as `Math.round(parseFloat(maxFeeInput) * 100)` — the same arithmetic
without calling `feeToCents`. If either path is modified independently, pet fees and
the user threshold could be computed differently. For the current static demo this is
harmless, but it's a maintainability risk.

Fix direction: reuse `feeToCents` for both conversions, or rename and document that
`feeToCents` is only for the `"$"-prefixed` pet data strings.

---

**[Medium] `openspec/.../design.md` vs `app/web/app.js:45` — event listener mismatch**

The design doc specifies a `"change"` event listener; the implementation correctly uses
`"input"`. The `"input"` event matches the spec requirement that "clearing the input
immediately re-filters visible pets." The design doc is wrong and should be corrected
to avoid confusing future readers.

---

**[Medium] `app/petstore_app/catalog.py:33` — `max_fee_cents` has no runtime type guard**

The type annotation is `int | None` but Python does not enforce it at runtime. A web
framework parsing `?max_fee_cents=120.0` (float) would silently pass a float. The
comparison `pet.adoption_fee_cents > 120.0` still works correctly (since
`adoption_fee_cents` is always a large-cent integer), but the type contract is broken.
Add `isinstance` check or use a Pydantic/validation layer if this function is ever
exposed via an API endpoint.

---

### Low

**[Low] `app/tests/test_pet_catalog.py:30` — Order-sensitive assertion is brittle**

`test_search_pets_filters_by_max_fee` asserts:
```python
assert [pet.name for pet in results] == ["Mochi", "Pip"]
```
This encodes the iteration order of `PETS`. If a pet is inserted between Mochi and
Pip in the fixture, the test fails even though the filter is correct. Prefer a
set comparison or `assert {p.name for p in results} == {"Mochi", "Pip"}`.

---

**[Low] `app/tests/test_pet_catalog.py` — `max_fee_cents=0` edge case not tested**

No test verifies that `max_fee_cents=0` returns an empty list (no pets cost 0 cents
in the fixture). This is a valid boundary: free-pets-only filter. Given the current
fixture data, this would return `[]`.

---

**[Low] `app/web/index.html:26` — `step="1"` does not prevent typed decimal input**

The HTML number input has `step="1"` and `min="0"`. The spinner arrows enforce whole
dollars, but a user who types `"1.5"` directly will produce `maxFeeCents = 150`
($1.50). This is arithmetically correct but may be surprising UX. The `step` attribute
alone does not block typed decimals in most browsers.

---

**[Low] No automated frontend tests**

The `feeToCents()` conversion and the live-filter rendering path are not covered by any
automated test. All 9 backend tests pass, but UI behavior can only be verified manually
or with Playwright. The PR body notes QA as a manual next step; no Playwright evidence
is attached to the PR.

---

## Petstore Contract Checks

- **Pending/adopted visibility:** ✅ `status` defaults to `"available"`; fee filter
  applies after status filter. Nova (pending, fee=11000¢) is never surfaced when
  default status is used. The test `test_search_pets_filters_by_max_fee` confirms
  this implicitly.
- **Adoption validation:** N/A — this PR does not touch adoption paths.
- **Money-as-cents:** ✅ `adoption_fee_cents: int` field; `max_fee_cents: int | None`
  parameter; test fixture values are integer cents (7500, 12500, 4500, 11000).
  `feeToCents()` in JS converts dollar strings to integer cents via `Math.round`.
  No floats stored.
- **New filters reject negative values:** ✅ `max_fee_cents < 0` raises `ValueError`
  with a message matching "max_fee_cents".
- **UI evidence:** ⚠️ The `Max fee ($)` input is present in `index.html` at line 26,
  but no screenshot or Playwright recording is attached to PR #86. The story-to-pr
  report calls for optional manual QA; UI evidence criterion is not fully satisfied.
- **Automation re-trigger risk:** Not applicable; no label changes introduced.

---

## Tests and QA

**Tests reviewed:** `app/tests/test_pet_catalog.py`

| Test | Result |
|------|--------|
| `test_search_pets_filters_by_species_and_status` | ✅ passed |
| `test_search_pets_can_find_pending_pets_when_requested` | ✅ passed |
| `test_search_pets_filters_by_tag` | ✅ passed |
| `test_search_pets_validates_max_results[0]` | ✅ passed |
| `test_search_pets_validates_max_results[51]` | ✅ passed |
| `test_search_pets_filters_by_max_fee` | ✅ passed |
| `test_search_pets_includes_pets_at_exact_fee_boundary` | ✅ passed |
| `test_search_pets_rejects_negative_max_fee` | ✅ passed |
| `test_search_pets_no_fee_filter_when_max_fee_none` | ✅ passed |

All 9 tests verified by running `uv run pytest app/tests/test_pet_catalog.py -v` locally
during this review session.

Full suite: `28 passed, 1 failed` — the 1 failure (`test_all_fixtures_use_known_automation_labels`)
is pre-existing on `main`.

**Test gaps:**
- `max_fee_cents=0` edge case (no free pets → empty result) not tested
- No test for `max_fee_cents` combined with `species` or `tag` filters (orthogonal but
  not validated in combination)
- No automated frontend tests for `feeToCents()` or the live-filter render path

**Missing evidence:**
- No UI screenshot or Playwright recording attached to PR #86
- No CI run evidence (no CI pipeline configured)

---

## Open Questions

1. **Pre-existing test failure:** Is `test_all_fixtures_use_known_automation_labels`
   intentionally baselined, or should it be fixed before this PR lands?
2. **UI evidence gate:** Does this repository require a screenshot or Playwright artifact
   before a PR with UI changes can be marked ready for review?
3. **API exposure:** Is `search_pets()` ever called from a web API endpoint (vs. only
   from test fixtures)? If so, the float type guard in `max_fee_cents` becomes important.
4. **Design doc correction:** Should `openspec/changes/canvas-issue-101-max-adoption-fee-filter/design.md`
   be updated to reflect `"input"` instead of `"change"` listener?

---

## Residual Risk

Overall risk is **low**. The backend change is minimal (one parameter, one predicate, one
guard), tests cover the four specified scenarios from the OpenSpec, and no existing tests
were broken. The UI change is additive and isolated. The main residual risks are:

- The pre-existing failing test (`test_github_label_fixtures`) — not introduced here, but
  it means the suite never fully passes and CI would report red if CI were enabled.
- Lack of UI automated tests means a regression in the JS filter logic would go undetected
  by the test suite.
- No CI pipeline means this PR could merge with a red test suite if the pre-existing
  failure is not resolved.

---

_This review was produced by an AI agent (OpenHands SDLC Automation Demo) on behalf of the repository owner. Humans decide what is blocking._
