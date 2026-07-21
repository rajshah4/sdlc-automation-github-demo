# Design: Fix Pending Pets Visibility Bug

## Context

Customers are seeing pets with `status="pending"` in the default catalog search results. According to `docs/wiki/petstore-catalog-availability.md`, the default catalog search must show only available pets. Support and operations may explicitly request pending pets, but they must not appear in the default customer-facing experience.

Log evidence in `docs/logs/pending-pet-visible.ndjson` shows error code `PENDING_PET_VISIBLE` for pet-103 (Nova), confirming a catalog availability regression.

## Root Cause

The `search_pets()` function in `app/petstore_app/catalog.py` has a filtering logic bug on line 50:

```python
if normalized_status and normalized_status != pet.status:
    continue
```

When `status=""` (empty string), `normalized_status` becomes an empty string, which is falsy in Python. The condition `if normalized_status` evaluates to `False`, so the status filter is skipped entirely, allowing all pets regardless of status to be returned.

## Evidence Trail

**Stop 1 - Ticket**: Jira KAN-70 reports "Customers are seeing pets that are not available yet"

**Stop 2 - Wiki/Docs**: `docs/wiki/petstore-catalog-availability.md` confirms:
- Default catalog search must show only `status="available"` pets
- Nova is pet-103 with `status="pending"`
- Pending pets should only appear when explicitly requested

**Stop 3 - Logs**: `docs/logs/pending-pet-visible.ndjson` shows:
- Error code: `PENDING_PET_VISIBLE`
- Bug signal: `catalog_availability_regression` marked as `safe_to_fix:true`
- Affected pet: `pet-103` (Nova)

**Stop 4 - Repo/Files**: `app/petstore_app/catalog.py` line 50 contains the filter logic bug

## Decision

Change the status filter logic to treat empty status as equivalent to the default "available":

```python
# Normalize empty status to the default "available"
effective_status = status.strip() if status.strip() else "available"
normalized_status = effective_status.lower()
```

This ensures that:
1. Empty status strings default to "available" behavior
2. Explicit non-empty status values are respected
3. The default parameter value `status="available"` continues to work correctly

### Files Changed

- `app/petstore_app/catalog.py`: Fix status filter logic (lines 31-42)
- `app/tests/test_pet_catalog.py`: Add regression tests

### Validation Plan

1. Run existing tests to ensure no regressions
2. Add new test for empty status string behavior
3. Add new test for default search behavior
4. Verify pending pet searches still work for support workflows

## Risks

- **Low**: The fix is isolated to filter logic with no side effects
- **Low**: Existing tests already cover the expected behavior patterns
- **None**: No schema, auth, deployment, or dependency changes required
- **Mitigation**: Regression tests added to prevent future occurrences
