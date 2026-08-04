# Design

## Context

The petstore catalog uses a `search_pets()` function in `app/petstore_app/catalog.py` that filters pets by various criteria including status. The function has a default parameter `status: str = "available"` to enforce the business rule that default searches show only available pets.

However, the current status filter logic uses a falsy check before applying the filter:
```python
if normalized_status and normalized_status != pet.status:
    continue
```

This means if `normalized_status` is an empty string (falsy), the entire status filter is skipped, allowing all pets regardless of status to appear in results.

Relevant evidence:
- Wiki: `docs/wiki/petstore-catalog-availability.md` confirms default searches must show only `status="available"`
- Log: `docs/logs/pending-pet-visible.ndjson` shows `PENDING_PET_VISIBLE` error with `pet-103` (Nova)
- Test: Existing test `test_search_pets_can_find_pending_pets_when_requested()` confirms pending searches work correctly
- Bug: Empty status string bypasses the filter entirely

## Decision

**Fix the status parameter normalization to default empty values to "available":**

Change line 41 in `catalog.py` from:
```python
normalized_status = status.strip().lower()
```

To:
```python
normalized_status = status.strip().lower() or "available"
```

This ensures that if `status=""` or `status="   "` is passed, the normalized value becomes "available" rather than an empty string.

**Simplify the status filter check:**

Change line 50 from:
```python
if normalized_status and normalized_status != pet.status:
    continue
```

To:
```python
if normalized_status != pet.status:
    continue
```

Since `normalized_status` is now guaranteed to have a value (either provided or defaulted to "available"), the falsy check is unnecessary and was the source of the bug.

## Alternative Considered

We could add explicit validation to reject empty status strings with a ValueError. However, this would be more disruptive to existing callers. Defaulting to "available" is more forgiving and aligns with the business rule that default behavior should be safe (available-only).

## Risks

- **Low risk**: The change is minimal and focused
- **Low risk**: Existing tests cover the main scenarios (default, explicit available, explicit pending)
- **Mitigation**: Adding a new regression test to explicitly verify empty-status defaults to available
- **Mitigation**: Existing test suite will validate that explicit pending searches still work

## Validation Plan

1. Run existing test suite: `cd app && python3 -m pytest tests/test_pet_catalog.py -v`
2. Add new regression test: `test_search_pets_defaults_empty_status_to_available()`
3. Verify test coverage includes:
   - Default search excludes pending pets ✓ (existing)
   - Explicit pending search works ✓ (existing)
   - Empty status defaults to available (new)
4. Manual validation: Verify Nova (pet-103) does not appear in `search_pets()` or `search_pets(status="")`
