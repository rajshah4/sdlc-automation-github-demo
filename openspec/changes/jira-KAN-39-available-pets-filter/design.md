# Design

## Context

The `catalog.py` module provides `search_pets()` with a default `status="available"` parameter. However, the implementation has a bug: line 50 checks `if normalized_status and normalized_status != pet.status`, which means when `status=""` (empty string), the condition is falsy and the status filter is completely bypassed.

According to `docs/wiki/petstore-catalog-availability.md`:
- Default customer-facing catalog search must show only `status="available"` pets
- Pending pets must not appear in default available-pets experience
- Nova (pet-103) has `status="pending"` and should not appear by default
- `PENDING_PET_VISIBLE` log indicates a catalog regression

The current test suite has tests for explicit `status="pending"` searches but lacks regression coverage for empty status strings or default behavior guarantees.

## Decision

- Change line 50 from `if normalized_status and normalized_status != pet.status:` to `if normalized_status != pet.status:`
- This ensures empty strings are treated like any other non-matching status value
- Since `normalized_status` is always a string (from `status.strip().lower()`), the check will always execute
- The default parameter `status="available"` already provides the correct fallback
- Add focused regression tests proving empty status defaults to available-only results

## Alternative Considered

An alternative would be to normalize empty strings to `"available"` explicitly:
```python
normalized_status = (status or "available").strip().lower()
```

This was rejected because:
- The function signature already provides the correct default
- Normalizing empty to "available" would make it impossible to search "all statuses" if that were ever needed
- The simpler fix is to just remove the truthiness check

## Risks

- **Breaking change risk**: LOW - The API contract already defaults to `status="available"`, so this fix enforces existing documented behavior
- **Test coverage risk**: LOW - Existing tests for explicit pending searches still pass; new tests prove the fix
- **Performance risk**: NONE - The change is a single condition removal with no loops or data operations

## Validation Plan

1. Run existing tests: `python -m pytest app/tests/test_pet_catalog.py -v`
2. Run new regression tests proving:
   - Default search excludes pending pets
   - Empty status string excludes pending pets
   - Nova (pet-103) does not appear in default results
3. Verify explicit `status="pending"` searches still work
