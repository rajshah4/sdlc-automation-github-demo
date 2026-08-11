# Design

## Context

The Petstore catalog stores pet availability in the `status` field. Default search behavior should return available pets only, while explicit status searches can inspect pending pets for support or operational workflows.

The backend (`app/petstore_app/catalog.py`) correctly defaults to `status="available"` in the `search_pets()` function. However, the frontend web UI (`app/web/app.js`) contains the pet data array and filtering logic that must also respect availability.

## Root Cause Analysis

Investigation of `app/web/app.js` shows that:
- The `pets` array (lines 1-6) includes Nova (`pet-103`) with `status: "pending"`
- The `renderResults()` function (lines 8-34) filters pets by query, species, and status
- Line 17 checks `pet.status === "available"`, which should exclude Nova
- However, the log evidence (`PENDING_PET_VISIBLE`) indicates that pending pets have been visible

The issue may be:
1. Filter logic not applying correctly on initial page load
2. A race condition or caching issue
3. Data inconsistency between backend and frontend

## Decision

**Safest approach: Add explicit validation to ensure only available pets are ever displayed**

- Keep the frontend filter on line 17: `pet.status === "available"`
- Add a defensive filter to the pets array definition to exclude non-available pets from ever being in the display list
- Alternatively, ensure renderResults() is called correctly on page load
- Add frontend integration test or visual verification that Nova never appears
- Add backend regression test that validates default search excludes pending pets
- Preserve explicit `status="pending"` searches in backend API for support workflows

## Files To Change

- `app/web/app.js`: Strengthen availability filtering (defensive approach)
- `app/tests/test_pet_catalog.py`: Add regression test for default behavior (if not already covered)

## Files NOT To Change

- `app/petstore_app/catalog.py`: Backend filter is already correct
- `app/petstore_app/adoptions.py`: Out of scope for this change (may need separate ticket)
- `app/web/index.html`: No structural changes needed

## Risks

- A broad fix could hide pending pets from support workflows that explicitly request them → Mitigated by only changing default frontend display, preserving backend `status` parameter
- Over-filtering could cause false negatives → Mitigated by focused testing and validation
- Frontend-only fix may not address adoption flow issue mentioned in ticket → Acknowledged as potential follow-up work

## Validation Plan

1. Run focused backend catalog tests: `pytest app/tests/test_pet_catalog.py -v`
2. Manually open `app/web/index.html` in browser and verify Nova is not visible by default
3. Run full pytest suite: `pytest app/tests/ -v`
4. Document validation results in PR
