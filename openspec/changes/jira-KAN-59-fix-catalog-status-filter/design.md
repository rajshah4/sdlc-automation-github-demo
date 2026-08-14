# Design

## Context

The Petstore catalog search function `search_pets()` in `app/petstore_app/catalog.py` has a status filter that uses a conditional check:

```python
if normalized_status and normalized_status != pet.status:
    continue
```

When `status=""` (empty string) is passed, `normalized_status` becomes `""` after `.strip().lower()`. The condition `if normalized_status` evaluates to `False`, causing the entire status filter to be skipped. This allows pets with ANY status (including pending) to be returned, even though the default parameter is `status="available"`.

The wiki (`docs/wiki/petstore-catalog-availability.md`) confirms that default customer-facing catalog search must show only pets with `status="available"`, and pending pets must not appear in the default experience.

## Root Cause

The bug is in line 50 of `catalog.py`:
```python
if normalized_status and normalized_status != pet.status:
```

This condition has a logical flaw: when `normalized_status` is an empty string (falsy), the filter is skipped entirely, allowing all pets regardless of status.

## Decision

Replace the faulty conditional with a proper filter that:
1. Always applies status filtering when a status parameter is provided (even empty string)
2. Defaults empty status to "available"
3. Maintains backward compatibility for explicit status="pending" searches

The fix:
```python
# Default empty status to "available"
if not normalized_status:
    normalized_status = "available"

# Apply status filter
if normalized_status != pet.status:
    continue
```

This ensures the status filter is always applied and empty strings default to "available".

## Risks

- **Low risk**: The change is a narrow logic fix in a well-tested function
- **Mitigation**: Add regression test to verify empty status behavior
- **Backward compatibility**: Explicit status="pending" searches continue to work

## Validation Plan

1. Run existing catalog tests: `pytest app/tests/test_pet_catalog.py`
2. Add new test: `test_search_pets_defaults_empty_status_to_available()`
3. Verify pending pet (Nova/pet-103) is excluded from default search
4. Verify explicit pending search still works
