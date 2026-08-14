# Design: Pending Pet Visibility Fix

## Investigation Summary

### Stop 1 - Ticket
- **KAN-67**: "Customers are seeing pets that are not available"
- **Impact**: Customers seeing pending pets, creating confusion and extra operations work
- **Business rule**: Default search must show only available pets

### Stop 2 - Wiki/Docs
- **File**: `docs/wiki/petstore-catalog-availability.md`
- **Finding**: Clear acceptance criteria - default search = available only, pending requires explicit request
- **Test pet**: Nova (pet-103) is the known pending pet in demo data

### Stop 3 - Logs
- **File**: `docs/logs/pending-pet-visible.ndjson`
- **Error code**: `PENDING_PET_VISIBLE`
- **Timestamp**: 2026-06-29T12:00:00Z
- **Component**: petstore-web
- **Evidence**: pet-103 (Nova) was visible in available-pets experience

### Stop 4 - Repo/Files
- **Backend**: `app/petstore_app/catalog.py`
  - Line 31: Correct default parameter `status: str = "available"`
  - Line 50: Correct filtering logic `if normalized_status and normalized_status != pet.status`
- **Frontend**: `app/web/app.js`
  - Line 17: Correct filter `&& pet.status === "available"`
- **Tests**: `app/tests/test_pet_catalog.py`
  - Existing tests cover basic species filtering and explicit pending requests
  - **Gap**: No explicit regression test for KAN-67 scenario (Nova exclusion from default)

## Root Cause Analysis

The filtering logic in both backend and frontend is correct. The issue was likely a transient bug that has been resolved, but test coverage was insufficient to prevent regression.

## Implementation Approach

### Strategy: Add Comprehensive Regression Tests

Since the code is currently correct, the fix is to add regression tests that would have caught this bug and will prevent it in the future.

### Changes Required

1. **Backend Test**: Add explicit test for Nova (pet-103) exclusion from default search
2. **Backend Test**: Verify default search by species excludes pending pets
3. **Existing Tests**: Verify all existing tests still pass

### Files Modified

- `app/tests/test_pet_catalog.py` - Add 2 new regression tests

### Test Scenarios

1. **test_default_search_excludes_pending_nova**
   - Search with no filters (defaults to available)
   - Verify Nova (pet-103) is NOT in results
   - Verify available pets (Mochi, Scout, Pip) ARE in results

2. **test_species_search_excludes_pending**
   - Search for dogs with default status
   - Verify only Scout (available dog) appears
   - Verify Nova (pending dog) does NOT appear

## Validation Plan

1. Run new regression tests with `uv run pytest app/tests/test_pet_catalog.py -v`
2. Verify all tests pass (existing + new)
3. Run Playwright UI test to verify frontend behavior (if available)
4. Document test results in PR

## Residual Risks

- **Low**: Tests verify behavior but don't prevent future code removal of filter logic
- **Mitigation**: Code review process and QA automation on PRs

## Non-Changes

- No code changes to filtering logic (already correct)
- No schema changes
- No API changes
- No UI changes
