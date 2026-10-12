# Design

## Context

The Petstore catalog uses `app/petstore_app/catalog.py` to filter pets by various criteria including status. According to `docs/wiki/petstore-catalog-availability.md`, default customer-facing searches must show only `status="available"` pets, while support workflows can explicitly request `status="pending"`.

Current implementation has a bug on line 50 where the status filter uses a truthy check that allows empty strings to bypass the filter entirely.

## Decision

Remove the truthy check from the status filter condition. Change from:
```python
if normalized_status and normalized_status != pet.status:
    continue
```

To:
```python
if normalized_status != pet.status:
    continue
```

This ensures the status filter always applies when a status value is provided, including the default `"available"` value.

## Risks

- **Low risk**: Simple one-line change to filter logic
- **Mitigation**: Add regression test `test_default_search_excludes_pending_pets` to prove the fix works
- **Backward compatibility**: Existing valid usage patterns (explicit status values) continue to work unchanged

## Validation Plan

1. Add new test `test_default_search_excludes_pending_pets()` proving default search excludes pending pets
2. Run `pytest app/tests/test_pet_catalog.py -v` to verify all tests pass
3. Confirm existing tests still pass: `test_search_pets_filters_by_species_and_status`, `test_search_pets_can_find_pending_pets_when_requested`
