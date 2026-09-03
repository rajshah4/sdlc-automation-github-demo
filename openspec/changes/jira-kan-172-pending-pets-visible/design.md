# Design

## Context

The Petstore catalog search function (`search_pets` in `app/petstore_app/catalog.py`) has a status parameter with a default value of `"available"`. The current implementation normalizes the status value with `.strip().lower()` and then uses a truthy check `if normalized_status and ...` to decide whether to filter by status.

The bug occurs when callers pass `status=""` or `status="  "` (whitespace-only):
- After normalization, these become `""` (empty string)
- The truthy check `if "" and ...` evaluates to False
- Status filtering is bypassed entirely
- Pending pets leak through to default search results

Evidence from investigation:
- **Wiki**: `docs/wiki/petstore-catalog-availability.md` documents that default searches must show only available pets
- **Logs**: `docs/logs/pending-pet-visible.ndjson` shows error code `PENDING_PET_VISIBLE` for pet-103 (Nova)
- **Code**: `app/petstore_app/catalog.py` lines 42 and 50 contain the problematic filtering logic

## Decision

- Normalize empty or whitespace-only status values to `"available"` before filtering
- This ensures that any attempt to bypass the status filter will default to safe behavior
- The fix is minimal: add one check after normalization to replace empty strings with "available"
- No changes to function signature, return type, or data structures

Implementation approach:
```python
normalized_status = status.strip().lower()
if not normalized_status:  # Empty or whitespace-only
    normalized_status = "available"
```

This ensures:
- Default behavior remains unchanged: `status="available"` works as before
- Empty strings are treated safely: `status=""` becomes `status="available"`
- Whitespace is normalized: `status="  "` becomes `status="available"`
- Explicit pending searches still work: `status="pending"` is preserved

## Risks

- **Risk**: Changing the filtering logic could break existing callers that expect empty status to return all pets
  - **Mitigation**: The product requirement is clear that default searches must exclude pending pets. Any caller expecting all pets should explicitly request `status=None` or use a different API. Empty strings should not bypass safety filters.

- **Risk**: The fix might not address all edge cases (e.g., `status="PENDING"` with different casing)
  - **Mitigation**: The normalization with `.lower()` already handles casing. The fix only addresses the empty-string bypass.

- **Risk**: Tests might fail if they depend on the buggy behavior
  - **Mitigation**: Review test coverage before and after the fix. Add new tests for edge cases.

## Validation Plan

1. Run existing tests: `pytest app/tests/test_pet_catalog.py -v`
2. Add new test cases for edge cases:
   - `test_search_pets_with_empty_status_defaults_to_available()`
   - `test_search_pets_with_whitespace_status_defaults_to_available()`
3. Verify that Nova (pet-103) does not appear in default searches
4. Verify that explicit pending searches still work correctly

## Evidence Waypoints

- **Stop 1 - Ticket**: Jira KAN-172, customer reports of pending pets visible in default searches
- **Stop 2 - Wiki/Docs**: Confirmed product rule in `docs/wiki/petstore-catalog-availability.md`
- **Stop 3 - Logs**: Found error code `PENDING_PET_VISIBLE` in `docs/logs/pending-pet-visible.ndjson` for pet-103
- **Stop 4 - Repo/Files**: Identified root cause in `app/petstore_app/catalog.py` lines 42-50
- **Stop 5 - Tests/PR**: Will add focused tests and create draft PR after implementation
