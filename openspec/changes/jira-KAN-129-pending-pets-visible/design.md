# Design

## Context

The Petstore catalog module (`app/petstore_app/catalog.py`) provides a `search_pets()` function that filters pets by name, species, status, and tag. The function defaults to `status="available"` to show only adoptable pets. However, when an empty string is passed for status, the filtering logic fails due to Python's falsy evaluation of empty strings.

From `docs/wiki/petstore-catalog-availability.md`:
- Default customer-facing catalog search must show only pets with `status="available"`
- Support workflows may explicitly request `status="pending"` for investigation
- Nova is `pet-103` with `status="pending"` and should not appear in default results

Current vulnerable code (line 41-42):
```python
normalized_status = status.strip().lower()
```

Current filter logic (line 50):
```python
if normalized_status and normalized_status != pet.status:
    continue
```

The bug: When `status=""`, the condition `if normalized_status and ...` is False, skipping the filter entirely.

## Decision

- Modify line 41-42 to treat empty or whitespace-only status as `"available"`
- Keep the existing filter logic unchanged (line 50)
- Add focused regression test to prevent recurrence
- No changes to function signature, parameters, or backward compatibility

**Implementation**:
```python
normalized_status = status.strip().lower() if status and status.strip() else "available"
```

This ensures:
1. Empty string or whitespace → defaults to `"available"`
2. Non-empty string → uses trimmed lowercase value
3. Existing filter logic works correctly with guaranteed non-empty `normalized_status`

**Rejected alternatives**:
- Remove the `and normalized_status` check in the filter condition (would break the default behavior intent)
- Make status a required parameter (breaks backward compatibility)

## Risks

- **Risk**: Other code paths might pass empty status intentionally
  - **Mitigation**: Existing tests verify default behavior; new test covers empty string case
- **Risk**: Future status values beyond "available" and "pending"
  - **Mitigation**: This change doesn't preclude adding new statuses; it only ensures empty defaults to "available"

## Validation Plan

- Run new regression test: `pytest app/tests/test_pet_catalog.py::test_search_pets_defaults_empty_status_to_available -v`
- Run full catalog test suite: `pytest app/tests/test_pet_catalog.py -v`
- Manual verification: `python3 -c "from app.petstore_app.catalog import search_pets; print([p.name for p in search_pets(status='')])"` should return `['Mochi', 'Scout', 'Pip']` (not Nova)
