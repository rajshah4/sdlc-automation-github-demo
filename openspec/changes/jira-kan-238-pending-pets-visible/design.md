# Design

## Context

The Petstore catalog search in `app/petstore_app/catalog.py` has a product rule that default searches must return only `status="available"` pets. Support reports and the `PENDING_PET_VISIBLE` log confirm customers are seeing Nova (pet-103), a pending pet, in the default available-pets experience.

The `search_pets()` function has a default parameter `status="available"`, but the status filter logic skips filtering when the normalized status evaluates to a falsy value:

```python
normalized_status = status.strip().lower()
# ...
if normalized_status and normalized_status != pet.status:
    continue
```

This means if `status=""` or status becomes empty after stripping, the filter is bypassed entirely.

## Decision

Change the status filter from checking truthiness to explicitly checking for `None`:

**Before:**
```python
normalized_status = status.strip().lower()
if normalized_status and normalized_status != pet.status:
    continue
```

**After:**
```python
normalized_status = status.strip().lower() if status else None
if normalized_status is not None and normalized_status != pet.status:
    continue
```

This ensures:
- The default `status="available"` is always enforced
- Empty strings are treated as `None` and don't bypass the filter
- Explicit status requests (including `status="pending"`) continue to work

## Risks

- **Low**: This is a small, focused change to filter logic
- **No breaking changes**: Function signature remains unchanged
- **Backward compatible**: Explicit status searches still work
- **Test coverage**: Existing test verifies explicit pending searches; new test verifies default behavior

## Validation Plan

1. Add regression test: `test_search_pets_excludes_pending_by_default()` verifies Nova is excluded from default searches
2. Run `pytest app/tests/test_pet_catalog.py -v` to verify all catalog tests pass
3. Confirm existing test `test_search_pets_can_find_pending_pets_when_requested()` still passes
