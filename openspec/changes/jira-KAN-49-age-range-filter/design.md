# Design

## Context

The Petstore catalog search function (`app/petstore_app/catalog.py::search_pets`) currently supports:
- Name query filtering
- Species filtering
- Status filtering (defaults to "available")
- Tag filtering
- Result limit validation

All pets have an `age_months` field (integer representing age in months). The current implementation does not filter by age.

## Decision

- Add two optional parameters to `search_pets()`: `min_age_months` and `max_age_months` (both `int | None`).
- Validate parameters before filtering:
  - Both must be non-negative if provided.
  - If both are provided, `min_age_months` must not exceed `max_age_months`.
- Apply age filters in the existing loop after other filter conditions.
- Preserve all existing behavior: default status filtering, max_results validation, and filter composition.

## Risks

**Risk**: Inverted ranges or negative ages could cause unexpected behavior.  
**Mitigation**: Validate parameters early and raise `ValueError` with clear messages.

**Risk**: Age filtering could interact unexpectedly with status filtering.  
**Mitigation**: Maintain filter independence; age filters apply to the same loop as other filters. Test coverage confirms age + status combinations work correctly.

**Risk**: Future UI integration may need different validation or messaging.  
**Mitigation**: Keep backend validation strict and deterministic; UI layer can add user-friendly messages.

## Validation Plan

- Run `python3 -m pytest -q app/tests/test_pet_catalog.py` to verify all tests pass.
- New tests cover:
  - Minimum age filtering
  - Maximum age filtering
  - Combined min/max age range
  - Negative age rejection
  - Inverted range rejection
  - Age + status filter interaction
