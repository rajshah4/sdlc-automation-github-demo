# Design

## Context

The Petstore catalog implements `search_pets()` in `app/petstore_app/catalog.py`. The function has a default parameter `status: str = "available"` that should filter to available-only pets.

The current implementation on line 50 uses:
```python
if normalized_status and normalized_status != pet.status:
    continue
```

This conditional has a bug: when `status=""` (empty string), `normalized_status` becomes `""` (falsy), causing the entire filter to be bypassed. The function was designed to default to "available" filtering, but an explicit empty string bypasses the filter entirely.

Per `docs/wiki/petstore-catalog-availability.md`, default customer-facing catalog search must show only pets with `status="available"`. The `PENDING_PET_VISIBLE` error code in `docs/logs/pending-pet-visible.ndjson` confirms Nova (pet-103) with status="pending" appeared in the available-pets experience.

## Decision

- Normalize empty status strings to "available" before filtering
- Change line 41 from `normalized_status = status.strip().lower()` to:
  ```python
  normalized_status = status.strip().lower() if status.strip() else "available"
  ```
- Keep the existing filter logic on line 50 unchanged
- This ensures empty status always defaults to "available" filtering, matching the parameter default's intent

## Risks

- **Minimal**: This is a pure filter-logic fix with no API contract changes
- **Backward compatibility**: Existing callers passing explicit status values are unaffected
- **Support workflows**: Explicit `status="pending"` searches continue to work unchanged
- **Mitigation**: Focused regression test confirms the fix, existing tests confirm no regression

## Validation Plan

- Add test: `test_search_pets_empty_status_excludes_pending_pets()` verifying `search_pets(species="dog", status="")` returns only available dogs
- Run `pytest app/tests/test_pet_catalog.py` to confirm all tests pass
- Existing test coverage already validates explicit pending searches and default available-only behavior
