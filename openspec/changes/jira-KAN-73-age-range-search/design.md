# Design

## Context

The Petstore catalog search function (`app/petstore_app/catalog.py`) currently supports:
- Query string matching on pet name
- Species filtering
- Status filtering (defaults to "available")
- Tag filtering
- Max results validation (1-50 range)

The Pet dataclass already includes an `age_months` field (integer). We need to add optional minimum and maximum age filtering without breaking existing behavior.

## Decision

- Add two new optional parameters: `min_age_months: int | None = None` and `max_age_months: int | None = None`
- Validate age parameters before filtering:
  - Reject negative ages with ValueError
  - Reject inverted ranges (min > max) with ValueError
- Apply age filtering in the existing filter loop alongside other criteria
- Follow the existing pattern: normalize, validate, filter
- Keep default behavior unchanged (no age filter when parameters are None)

## Risks

- **Risk**: Breaking existing callers that don't expect new ValueError cases
  - **Mitigation**: New parameters are optional and only validated when provided; existing calls unaffected
  
- **Risk**: Performance impact with multiple filters
  - **Mitigation**: Single-pass filtering already in place; adding two integer comparisons is negligible

- **Risk**: Age validation conflicts with other validation
  - **Mitigation**: Validate age parameters first, before the existing max_results check, to fail fast

## Validation Plan

- Run existing tests to confirm no regressions: `python3 -m pytest -q app/tests/test_pet_catalog.py`
- Add new tests for:
  - Minimum age filtering (include/exclude cases)
  - Maximum age filtering (include/exclude cases)
  - Range filtering (combined min/max)
  - Negative age rejection
  - Inverted range rejection
  - Age filter combined with status filter (confirm available-only default preserved)
- Run full test suite: `python3 -m pytest -q`
