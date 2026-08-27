# Design

## Context

The Petstore catalog module (`app/petstore_app/catalog.py`) provides a `search_pets()` function that filters pets by name, species, status, and tags. The function has a default parameter `status: str = "available"` which should ensure only available pets are returned by default.

However, the current implementation has a logic flaw on line 50:
```python
if normalized_status and normalized_status != pet.status:
    continue
```

When `status=""` is passed explicitly, `normalized_status` becomes an empty string after `strip().lower()`. Since empty strings are falsy in Python, the condition `if normalized_status` evaluates to False, causing the status filter to be entirely skipped. This allows pending pets to leak into default search results.

The product rules state:
- Default pet search returns only available pets
- Pending pets can be shown only when explicitly requested and cannot be adopted

## Decision

- Modify the normalization logic to treat empty status strings as "available"
- Change line 41 from `normalized_status = status.strip().lower()` to `normalized_status = status.strip().lower() or "available"`
- This ensures the status filter is always applied with a valid value
- Explicit `status="pending"` requests continue to work as expected

## Alternative Considered

We could modify the filtering condition instead:
```python
if status and normalized_status != pet.status:
```

However, this still allows bypassing the filter with empty strings. The normalization approach is safer because it enforces the default behavior at the source.

## Risks

- **Low risk**: The change is minimal and well-scoped to status filtering logic
- **Backward compatibility**: Any code passing `status=""` was already violating product requirements
- **Test coverage**: Existing tests verify default and explicit status filtering; new test added for empty string case
- **Mitigation**: Focused regression test ensures empty status defaults to available-only results

## Validation Plan

- Run `python3 -m pytest app/tests/test_pet_catalog.py -v` to verify catalog behavior
- Run `python3 -m pytest app/tests/ -v` to ensure no regressions
- Verify the new test `test_search_pets_defaults_to_available_when_status_empty` passes
- Verify existing tests continue to pass
