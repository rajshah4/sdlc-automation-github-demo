# Design

## Context

The Petstore catalog implements pet search filtering in `app/petstore_app/catalog.py`. The product rule (documented in `docs/wiki/petstore-catalog-availability.md`) requires:

- Default customer-facing search returns only `status="available"` pets
- Pending pets can only be shown when explicitly requested with `status="pending"`
- The log entry `docs/logs/pending-pet-visible.ndjson` shows error code `PENDING_PET_VISIBLE` indicating Nova (pet-103, status="pending") appeared in available-pets results

Current implementation has a logic flaw at line 50:
```python
if normalized_status and normalized_status != pet.status:
    continue
```

When `status=""` is passed, `normalized_status` becomes an empty string (falsy), causing the status filter to be skipped entirely. This allows all pets (including pending ones) to be returned.

## Decision

- Normalize empty or whitespace-only status values to `"available"` before filtering
- Place the normalization immediately after stripping whitespace
- Preserve existing behavior for explicit `status="pending"` requests
- Keep the fix minimal: one conditional check added to the normalization logic

Implementation approach:
```python
normalized_status = status.strip().lower()
if not normalized_status:
    normalized_status = "available"
```

This ensures empty status always defaults to the safe, customer-facing behavior.

## Risks

- **Backward compatibility**: If any existing code relies on empty status returning all pets, this will break that behavior
  - **Mitigation**: The product rule explicitly requires available-only defaults; returning all pets was never intended behavior
- **Test coverage**: Existing tests don't cover the empty-status edge case
  - **Mitigation**: Add explicit regression test for `search_pets(status="")`

## Validation Plan

- Run existing test suite to ensure no regressions: `cd app && python -m pytest tests/test_pet_catalog.py -v`
- Add and run new test `test_search_pets_empty_status_defaults_to_available` to prove the fix works
- Verify test output shows pending pets excluded from empty-status search
