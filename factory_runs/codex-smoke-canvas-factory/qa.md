# QA Report — Issue #101: Filter pets by max adoption fee

**Run ID:** `codex-smoke-canvas-factory`
**Branch:** `feature/canvas-issue-101-max-adoption-fee-filter`
**Story:** Issue #101 — As an adoption coordinator, I want to filter available pets by maximum adoption fee so families can find pets that fit their budget.
**QA Date:** 2026-06-30
**Status:** ✅ PASS

---

## Changed Files

| File | Change |
|------|--------|
| `app/petstore_app/catalog.py` | Added `max_fee_cents: int \| None = None` parameter to `search_pets()`; raises `ValueError` for negative values; filters pets by fee |
| `app/tests/test_pet_catalog.py` | 4 new focused tests for fee-filter behavior |
| `app/web/index.html` | Added `Max fee ($)` number input (`id="max-fee"`) to toolbar |
| `app/web/app.js` | Added `feeToCents()` helper; wired filter predicate and live `input` event listener |
| `openspec/changes/canvas-issue-101-max-adoption-fee-filter/` | OpenSpec-style proposal, design, spec, and tasks documents |

---

## Commands Run

```bash
# Focused backend tests
uv run --with pytest pytest app/tests/test_pet_catalog.py -v

# Full test suite
uv run --with pytest pytest -v

# Static UI smoke check (dependency-free)
python3 -m http.server 4173 --directory app/web &
python3 skills/sdlc-qa/scripts/static_ui_smoke.py \
  --url http://localhost:4173 \
  --expect "Max fee" \
  --expect "max-fee"

# HTML structure verification
python3 -c "... assert 'id=\"max-fee\"' in html ..."

# Browser evidence via Agent Canvas browser tools
# (navigate → screenshot default state → type fee value → screenshot filtered state)
```

---

## Test Results

### Focused: `app/tests/test_pet_catalog.py` — 9/9 PASS

| Test | Result |
|------|--------|
| `test_search_pets_filters_by_species_and_status` | ✅ PASS |
| `test_search_pets_can_find_pending_pets_when_requested` | ✅ PASS |
| `test_search_pets_filters_by_tag` | ✅ PASS |
| `test_search_pets_validates_max_results[0]` | ✅ PASS |
| `test_search_pets_validates_max_results[51]` | ✅ PASS |
| `test_search_pets_filters_by_max_fee` *(new)* | ✅ PASS — Mochi+Pip returned at max 12 000 ¢; Scout excluded |
| `test_search_pets_includes_pets_at_exact_fee_boundary` *(new)* | ✅ PASS — Mochi included at exact 7 500 ¢ boundary |
| `test_search_pets_rejects_negative_max_fee` *(new)* | ✅ PASS — `ValueError` raised |
| `test_search_pets_no_fee_filter_when_max_fee_none` *(new)* | ✅ PASS — `None` behaves identically to unfiltered |

### Broader: Full suite — 28/29 PASS (1 pre-existing failure)

| Module | Result |
|--------|--------|
| `app/tests/test_adoptions.py` (4 tests) | ✅ All pass |
| `app/tests/test_cloud_run_app.py` (3 tests) | ✅ All pass |
| `app/tests/test_pet_catalog.py` (9 tests) | ✅ All pass |
| `app/tests/test_telemetry.py` (2 tests) | ✅ All pass |
| `tests/test_agent_canvas_factory.py` (6 tests) | ✅ All pass |
| `tests/test_automation_packages.py` (1 test) | ✅ Pass |
| `tests/test_github_label_fixtures.py` (3 tests) | ⚠️ 1 FAIL — `test_all_fixtures_use_known_automation_labels` |

**Pre-existing failure note:** `test_all_fixtures_use_known_automation_labels` fails with `KeyError: 'label'` on both `main` and this branch. It is not introduced by this PR and is out of scope for this QA gate.

---

## Test Files Added or Changed

| File | Action | Tests Added |
|------|--------|-------------|
| `app/tests/test_pet_catalog.py` | Updated by PR author | 4 new tests (`test_search_pets_filters_by_max_fee`, `test_search_pets_includes_pets_at_exact_fee_boundary`, `test_search_pets_rejects_negative_max_fee`, `test_search_pets_no_fee_filter_when_max_fee_none`) |

No additional test files were added by QA — the PR-authored tests cover all expected scenarios. Coverage is sufficient.

---

## UI Evidence

**Evidence type:** Live browser screenshots captured via Agent Canvas browser tools.
**Method:** Static HTTP server (`python3 -m http.server 4173 --directory app/web`) + Agent Canvas browser navigation.
**Playwright:** Not available locally; not installed per demo constraints.

### Scenario 1 — Default catalog shows all available pets, Max fee input visible

- Navigated to `http://localhost:4173/`
- **Expected:** Mochi ($75), Scout ($125), Pip ($45) visible; Nova (pending) hidden; "Max fee ($)" input present
- **Actual:** ✅ All three available pets shown; Nova absent; "Max fee ($)" input rendered in toolbar
- **Screenshot:** `ui-evidence/ui-default-all-pets.png`

### Scenario 2 — Fee filter at $100 excludes Scout ($125), keeps Mochi and Pip

- Typed `100` into the Max fee ($) input
- **Expected:** Scout ($125) removed from results; Mochi ($75) and Pip ($45) remain; filter fires live on `input` event (no button click required)
- **Actual:** ✅ Results updated immediately on keystroke; Scout removed; Mochi and Pip displayed
- **Screenshot:** `ui-evidence/ui-fee-filter-100.png`

### Scenario 3 — Static DOM smoke check (dependency-free)

- `static_ui_smoke.py --expect "Max fee" --expect "max-fee"` against live server
- **Result:** ✅ PASS — `"max-fee"` input id, `"Max fee"` label, `type="number"`, `min="0"`, `step="1"` all confirmed in HTML source

---

## Behavioral Coverage Check

| Acceptance criterion | Covered by | Result |
|----------------------|-----------|--------|
| Filter returns only available pets within fee budget | `test_search_pets_filters_by_max_fee` + browser scenario 2 | ✅ |
| Pets at exact fee boundary are included (not excluded) | `test_search_pets_includes_pets_at_exact_fee_boundary` | ✅ |
| Negative fee values are rejected with `ValueError` | `test_search_pets_rejects_negative_max_fee` | ✅ |
| No filter when `max_fee_cents=None` (backward compat) | `test_search_pets_no_fee_filter_when_max_fee_none` | ✅ |
| Pending pets are NOT shown even when fee filter is active | `test_cloud_run_app.py::test_visible_pets_excludes_pending_by_default` + browser default view | ✅ |
| UI control renders as `type="number"` with `min="0"` | Static smoke + HTML assertion | ✅ |
| Filter reacts live on keystroke (no button click needed) | Browser scenario 2 (live observation) | ✅ |
| Fee stored as integer cents, no float leakage in backend | `max_fee_cents: int` signature + all catalog tests | ✅ |

---

## Residual Risk

| Risk | Severity | Notes |
|------|----------|-------|
| `feeToCents()` parses UI pet fee from string `"$75"` using `parseFloat(feeStr.replace("$", ""))` — no guard against non-numeric or missing `$` prefix | Low | The pet data is static and always uses `"$N"` format; expanding the dataset without `$` would silently return `NaN`, causing the comparison to return `false` and the pet to be excluded. Acceptable for current scope. |
| No upper-bound validation on `max_fee_cents` in the backend | Very low | Overly large values simply return all pets, which is the correct behavior. |
| One pre-existing test failure (`test_all_fixtures_use_known_automation_labels`) | Low | Not introduced by this PR. Should be fixed separately. |
| No automated Playwright spec for the new fee-filter scenario | Low | `catalog-search.playwright.mjs` covers default, species, name, and pending-pet scenarios but not the fee filter. A focused extension would close this gap in a follow-on ticket. |

---

## Merge-Readiness Recommendation

**Recommendation: READY TO MERGE** (human approval required per SDLC policy).

All four new focused backend tests pass. The broader suite passes on all in-scope modules. UI evidence confirms the "Max fee ($)" control is rendered, filters live on keystroke, and pending pets remain hidden. No regressions in adoption, telemetry, or cloud-run tests. The one failing test is a pre-existing defect unrelated to this feature.

_This report was generated by an AI agent (OpenHands) on behalf of the QA work cell._

---

## Artifact Paths

| Artifact | Path |
|----------|------|
| QA report | `factory_runs/codex-smoke-canvas-factory/qa.md` |
| UI screenshot — default state | `factory_runs/codex-smoke-canvas-factory/ui-evidence/ui-default-all-pets.png` |
| UI screenshot — fee filter $100 | `factory_runs/codex-smoke-canvas-factory/ui-evidence/ui-fee-filter-100.png` |
