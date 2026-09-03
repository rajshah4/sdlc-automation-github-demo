# Design

## Context

The Petstore catalog supports multiple pet statuses: `available` and `pending`. Product rule states that default pet search returns only available pets, and pending pets can be shown only when explicitly requested.

Current implementation:
- **Backend** (`app/petstore_app/catalog.py`): `search_pets()` function with `status="available"` default parameter
- **Frontend** (`app/web/app.js`): Filter with hardcoded `pet.status === "available"` check
- **Evidence**: Historical `PENDING_PET_VISIBLE` log from June 29, 2026 suggests this was a past issue

Investigation findings show the current code is **already correct** in both backend and frontend.

## Decision

- **Verify existing implementation**: Both backend and frontend have correct filtering logic.
- **Add explicit regression test**: Create `test_default_search_excludes_pending_pets()` to make the requirement more visible and prevent future regressions.
- **Test naming**: Use explicit test name that directly states the requirement.
- **No code changes needed**: The filtering logic is correct; only test strengthening is required.

## Risks

- **Risk**: Tests pass but edge case exists in production (e.g., caching, deployment mismatch, race condition).
  - **Mitigation**: Document that investigation found correct code; recommend production verification if issue persists.
  
- **Risk**: Historical log from June 29, 2026 may indicate this was fixed before and regressed.
  - **Mitigation**: Explicit regression test with clear name will make requirement visible and easier to catch in review.
  
- **Risk**: Test coverage gap - no single test explicitly named for this exact requirement.
  - **Mitigation**: Add `test_default_search_excludes_pending_pets()` test.

## Validation Plan

1. **Validate OpenSpec artifacts**: Run `python3 skills/sdlc-story/scripts/validate_open_spec.py openspec/changes/jira-KAN-174-pending-pets-visible`
2. **Add regression test**: Create explicit test in `app/tests/test_pet_catalog.py`
3. **Run backend tests**: `python3 -m pytest -q app/tests/test_pet_catalog.py -v`
4. **Verify all tests pass**: Ensure new test and all existing tests pass
5. **Document findings**: Create PR with evidence waypoints showing investigation results
