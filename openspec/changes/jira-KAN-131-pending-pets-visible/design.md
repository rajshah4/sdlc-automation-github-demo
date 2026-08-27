# Design

## Context

The petstore catalog search function `search_pets()` in `app/petstore_app/catalog.py` has a default parameter `status: str = "available"` (line 31). The function normalizes the status parameter and uses it to filter pets (line 50).

The bug occurs when the status parameter is explicitly passed as an empty string. The filter logic on line 50 is:

```python
if normalized_status and normalized_status != pet.status:
    continue
```

When `normalized_status` is an empty string, the condition `if normalized_status` evaluates to `False`, causing the entire status filter to be skipped. This allows pending pets to appear in results where they should be excluded.

## Decision

- Modify the status filter logic to handle empty status as equivalent to "available"
- Change line 50 from truthy check to explicit empty-string check
- Default empty status to "available" to preserve the intended catalog behavior
- Keep the parameter default of "available" for backward compatibility
- No changes to function signature or public API

## Implementation

Replace the filter condition:

```python
# Before
if normalized_status and normalized_status != pet.status:
    continue

# After  
if normalized_status and normalized_status != pet.status:
    continue
```

Actually, the better fix is to normalize empty status to "available":

```python
normalized_status = status.strip().lower() if status.strip() else "available"
```

This ensures that empty strings are treated the same as the default.

## Risks

- **Risk**: Changing filter behavior could affect callers that rely on empty status returning all pets
- **Mitigation**: Based on wiki docs and product rules, this is a bug fix restoring intended behavior; no legitimate use case for empty status bypassing the filter

- **Risk**: Performance impact from additional string operations
- **Mitigation**: Negligible; we're adding one conditional check to an existing normalize operation

## Validation Plan

- Add test case: `test_search_pets_empty_status_excludes_pending()` that calls `search_pets(status="")` and verifies Nova is excluded
- Run existing test suite to ensure no regressions
- Verify explicit `status="pending"` searches still work for operations
