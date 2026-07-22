# Design

## Context

The Petstore catalog search function (`app/petstore_app/catalog.py::search_pets`) filters pets by status, with a default of "available". The filter logic uses a pattern common to optional parameters:

```python
if normalized_status and normalized_status != pet.status:
    continue
```

This pattern works for truly optional parameters (like `species` or `tag`) where `None` or empty means "don't filter". However, `status` has a default value of `"available"`, so it should always filter.

The bug: When someone explicitly passes `status=""`, the empty string becomes falsy after normalization, causing the entire condition to short-circuit to `False`. The status filter is skipped entirely, returning all pets regardless of status.

Product rule from `docs/wiki/petstore-catalog-availability.md`: "Default customer-facing catalog search must show only pets with status='available'."

Evidence from `docs/logs/pending-pet-visible.ndjson`: Error code `PENDING_PET_VISIBLE` for pet-103 (Nova) in the `petstore-web` component confirms the regression occurred.

## Decision

**Change line 41** from:
```python
normalized_status = status.strip().lower()
```

to:
```python
normalized_status = status.strip().lower() or "available"
```

This ensures that when `status` is empty or whitespace-only, `normalized_status` defaults to `"available"`, preserving the expected behavior.

**Rationale:**
- Minimal change: one-line fix
- Preserves all existing behavior for non-empty status values
- Makes the empty-string case explicit and correct
- No changes needed to function signature or other parameters
- Maintains backward compatibility for all valid use cases

## Risks

- **False positives in validation**: If any code was intentionally passing `status=""` to bypass filtering (unlikely), it will now filter to available. Mitigation: existing tests pass, and the product spec requires available-only default behavior.
- **Whitespace handling**: We strip before checking, so `"  "` becomes `""` and then defaults to `"available"`. This is correct per spec but wasn't explicitly tested before. Mitigation: add focused regression test.

## Validation Plan

1. Run existing backend tests to ensure no regressions:
   ```bash
   python -m pytest app/tests/test_pet_catalog.py -v
   ```

2. Add new regression test `test_search_pets_defaults_to_available_when_status_is_empty` that verifies:
   - `search_pets(species="dog", status="")` returns only available dogs (Scout), not pending dogs (Nova)

3. Verify the fix covers the logged error scenario from `pending-pet-visible.ndjson`
