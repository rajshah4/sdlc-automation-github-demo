# Design

## Context

The petstore catalog uses `app/petstore_app/catalog.py::search_pets()` to filter pets by various criteria including status. The function has a default parameter `status: str = "available"` which should ensure that default searches only return available pets.

The bug occurs in the filtering logic at line 50:

```python
if normalized_status and normalized_status != pet.status:
    continue
```

This conditional includes a truthiness check on `normalized_status`. When `normalized_status` is an empty string (falsy in Python), the entire status filter is skipped, allowing all pets regardless of status to be returned.

The wiki at `docs/wiki/petstore-catalog-availability.md` clearly states that the default customer-facing catalog must show only `status="available"` pets. The log evidence at `docs/logs/pending-pet-visible.ndjson` shows the `PENDING_PET_VISIBLE` error code with `pet-103` (Nova) appearing in results when it shouldn't.

## Decision

- Remove the truthiness check from the status filter condition on line 50.
- Change `if normalized_status and normalized_status != pet.status:` to `if normalized_status != pet.status:`.
- This ensures the status filter always applies when a status parameter is provided (including the default).
- Add a focused test to verify default search behavior excludes pending pets.

## Risks

- **Breaking existing callers**: Low risk. The function signature and default remain unchanged. Any code passing `status=""` explicitly would be a bug that should be fixed.
- **Test coverage**: Current tests verify explicit status filtering but not default behavior. New test addresses this gap.
- **Performance**: No impact. The fix removes a condition check, marginally improving performance.

## Validation Plan

- Run existing tests with `python3 -m pytest app/tests/test_pet_catalog.py -v` to ensure no regressions.
- Run new test `test_search_pets_excludes_pending_by_default` to verify the fix.
- Verify that Nova (pet-103) does not appear in default search results.
- Verify that explicit `status="pending"` searches still work for operational use cases.
