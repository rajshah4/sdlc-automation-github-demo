# Design

## Context

The SDLC Automation Demo Petstore maintains a simple pet catalog with statuses: `available` and `pending`. Product rules require that:

1. Default searches return only available pets
2. Pending pets appear only when explicitly requested with `status="pending"`
3. Pending pets cannot be adopted (enforced in backend)

Current implementation:
- Backend: `catalog.py` has `search_pets()` with default parameter `status="available"`
- Frontend: `app/web/app.js` has hardcoded pets array and filter logic
- Tests: Existing tests in `test_pet_catalog.py` verify backend behavior

Evidence from `docs/logs/pending-pet-visible.ndjson` shows error code `PENDING_PET_VISIBLE` for pet-103 (Nova), indicating the bug exists in production.

## Decision

**Primary fix**: Review and strengthen the frontend filter in `app.js`

The backend `search_pets()` already defaults to `status="available"` and has tests confirming this works. The bug is most likely in the frontend JavaScript filter or an edge case where the filter isn't applied consistently.

Actions:
1. Review the `renderResults()` function in `app.js` for any edge cases where the status filter might be bypassed
2. Ensure the filter `pet.status === "available"` is always enforced
3. Add defensive checks to prevent regressions
4. Add comprehensive tests that verify both backend and demonstrate correct UI behavior

**Secondary consideration**: The pets array is hardcoded in `app.js`. In a real system, this would fetch from a backend API. For this demo, we maintain the static data but ensure the filter is bulletproof.

## Risks

- **Risk**: The bug might be intermittent or browser-specific
  - **Mitigation**: Add explicit tests and verify with UI smoke testing
  
- **Risk**: The fix might accidentally break support/operations ability to query pending pets
  - **Mitigation**: Preserve existing `status` parameter support; only fix the default filter

- **Risk**: If the actual root cause is different (caching, race conditions), the filter fix alone might not resolve all cases
  - **Mitigation**: Document assumptions in PR; QA will test the actual UI behavior

## Validation Plan

1. **Backend tests**: Run `python3 -m pytest app/tests/test_pet_catalog.py -v` to confirm existing tests pass
2. **New regression test**: Add test verifying default search excludes pending pets
3. **UI smoke test**: Run `python3 skills/sdlc-qa/scripts/static_ui_smoke.py --url http://localhost:4173`
4. **Manual verification**: Load UI in browser and verify Nova is not visible in default view
