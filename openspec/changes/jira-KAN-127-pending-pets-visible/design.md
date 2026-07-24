# Design

## Context

The Petstore catalog maintains pets with multiple status values: "available", "pending", and potentially others. Product rules require that default customer-facing searches show only available pets. Pending pets should only appear when explicitly requested by support or operations.

Log evidence (`docs/logs/pending-pet-visible.ndjson`) shows error code `PENDING_PET_VISIBLE` with pet-103 (Nova) appearing in the available-pets experience. Nova has `status="pending"` according to the demo fixtures and `docs/wiki/petstore-catalog-availability.md`.

## Root Cause Analysis

The `search_pets()` function in `app/petstore_app/catalog.py` has a bug in its status filtering logic:

```python
def search_pets(
    query: str = "",
    *,
    species: str | None = None,
    status: str = "available",  # Default is correct
    tag: str | None = None,
    max_results: int = 10,
) -> list[Pet]:
    # ...
    normalized_status = status.strip().lower()
    
    for pet in PETS:
        # ...
        if normalized_status and normalized_status != pet.status:  # BUG: allows empty status
            continue
```

The problem: `if normalized_status and normalized_status != pet.status` only filters when `normalized_status` is truthy. If someone passes `status=""` or the status gets normalized to an empty string, the filter is bypassed and ALL pets (including pending ones) are returned.

## Decision

Fix the status filter to always apply when status is provided, and ensure the default "available" value is always used when status is empty or None:

1. Update the function signature to handle None explicitly
2. Convert None or empty status to "available" before normalization
3. Change the filter condition to always apply status matching (remove the truthiness check)

This is the smallest safe change:
- Preserves the default "available" behavior
- Fixes the empty-string bypass bug
- Keeps explicit `status="pending"` searches functional
- No changes to the PETS data, adoption logic, or UI

## Risks

- **Backward compatibility**: If any existing code relies on empty status returning all pets, this will break that behavior. Mitigation: Product rules explicitly forbid showing pending pets by default, so this is the correct behavior.
- **Test coverage**: Need regression tests to prove pending pets stay out of default searches. Mitigation: Add focused tests for empty status, default status, and explicit pending searches.

## Validation Plan

1. Run existing tests to ensure no regressions: `python3 -m pytest app/tests/test_pet_catalog.py -v`
2. Add new regression tests for the bug scenarios
3. Run full test suite: `python3 -m pytest -q`
4. Verify that:
   - Default search excludes Nova (pet-103)
   - Species="dog" search excludes Nova
   - Explicit status="pending" still returns Nova
   - Empty status behaves like "available"
