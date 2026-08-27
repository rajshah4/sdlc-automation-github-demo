# Design

## Context

The Petstore catalog filtering has a documented product rule: "Default pet search returns only available pets. Pending pets can be shown only when explicitly requested and cannot be adopted."

Log evidence from `docs/logs/pending-pet-visible.ndjson` shows that on 2026-06-29, pet-103 "Nova" with `status="pending"` leaked into the customer-facing available-pets experience (error code: `PENDING_PET_VISIBLE`).

Current implementation:
- Backend `search_pets()` has `status: str = "available"` as default parameter (line 31 of `catalog.py`)
- Frontend `app.js` filters by `pet.status === "available"` (line 17)
- Both appear correct in current code

Hypothesis: The bug may have been recently fixed, or there's an edge case with null/undefined/empty status values that needs defensive handling.

## Decision

- **Backend**: Keep the existing `status="available"` default but add validation to ensure empty strings are handled correctly
- **Frontend**: Keep the existing `pet.status === "available"` filter (already correct)
- **Tests**: Add comprehensive test coverage for:
  1. Default search behavior (no status parameter)
  2. Edge cases (null, empty, undefined status values)
  3. Explicit pending pet search (verify it still works for operations)
- **Validation**: Run existing tests plus new edge-case tests to ensure no regression

This is the smallest safe change: strengthen existing filtering and add test coverage rather than redesigning the architecture.

## Risks

- **False fix risk**: If the bug was already fixed, we're adding defensive code that may not be strictly necessary
  - Mitigation: Additional defensive checks and tests improve robustness and prevent future regressions
  
- **Operational workflow break**: If we accidentally block operations from seeing pending pets
  - Mitigation: Preserve explicit `status="pending"` parameter support and add test coverage for it

- **Test coverage gap**: Existing tests may not cover all edge cases
  - Mitigation: Add focused tests for default behavior and edge cases

## Validation Plan

1. Run existing backend tests: `pytest app/tests/test_pet_catalog.py -v`
2. Verify the new edge-case tests pass
3. Check that operations can still explicitly request pending pets
4. Confirm default search behavior excludes pending pets

Command:
```bash
python3 -m pytest app/tests/test_pet_catalog.py -v
```
