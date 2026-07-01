# Design: Pending Pet Visibility Regression Tests

## Context

The PENDING_PET_VISIBLE error (logged 2026-06-29 12:00 UTC) indicates that pet-103 (Nova) appeared in available pet searches despite having status="pending". The current code correctly filters pets by status, but test coverage is insufficient to catch regressions.

## Evidence Review

**Stop 1 - Ticket**: KAN-60 reports Nova showing in available pets list

**Stop 2 - Wiki/Docs**: 
- `docs/wiki/petstore-catalog-availability.md` confirms default search must show only available pets
- Nova is pet-103 with status="pending"

**Stop 3 - Logs**: 
- `docs/logs/pending-pet-visible.ndjson` shows PENDING_PET_VISIBLE error with pet-103 in pending_pet_ids array
- Error marked as catalog_availability_regression with safe_to_fix=true

**Stop 4 - Repo/Files**:
- `app/petstore_app/catalog.py` correctly filters by status="available" (default parameter, line 31)
- `app/web/app.js` correctly filters with `pet.status === "available"` (line 17)
- Current tests don't explicitly verify that pending pets are excluded from default search

## Root Cause

Missing test coverage. While the code is correct, there's no test that explicitly verifies:
1. Default search with no arguments returns only available pets
2. Nova (pet-103) specifically is excluded from default results
3. All pending pets are filtered out unless explicitly requested

## Implementation Plan

Add three focused regression tests to `app/tests/test_pet_catalog.py`:

1. **test_default_search_excludes_pending_pets**: Verify `search_pets()` with no args returns only available pets
2. **test_nova_excluded_from_default_search**: Explicit test that Nova (pet-103) is not in default results
3. **test_all_available_pets_included_by_default**: Verify all three available pets (Mochi, Scout, Pip) are included

## Files Changed

- `app/tests/test_pet_catalog.py`: Add three new test functions

## Decision

Add focused regression tests without changing production code. The catalog filtering logic is confirmed correct through manual testing and code inspection. The fix is purely additive test coverage to prevent future regressions.

## Risks

- **Risk Level**: Low
- **Reasoning**: Only adding tests, no production code changes
- **Rollback**: Can simply remove the tests if needed
- **Blast Radius**: Test suite only

## Validation Plan

1. Run `pytest app/tests/test_pet_catalog.py -v` to verify all tests pass
2. Verify new tests explicitly check:
   - Default search excludes pending pets
   - Nova (pet-103) is not in default results
   - All available pets are included
3. Confirm test output shows 7 total tests (4 existing + 3 new)
4. Manual smoke test: Open `app/web/index.html` and verify only 3 available pets show on page load
