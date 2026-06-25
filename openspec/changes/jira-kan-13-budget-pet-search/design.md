# Design

## Context

The Petstore catalog search (`app/petstore_app/catalog.py`) currently supports filtering by name query, species, status, tag, and max_results. Default behavior returns only available pets. Pending pets appear only when status is explicitly requested. This contract must be preserved.

Log evidence from `docs/logs/pet-search-budget-limit.ndjson` shows a family requested pets within a $75 budget (max_adoption_fee_cents=7500), but the search returned Scout with adoption_fee_cents=12500, confirming that fee filtering is not yet implemented.

## Decision

- Add an optional `max_adoption_fee_cents: int | None = None` parameter to `search_pets()`.
- When provided, filter pets where `pet.adoption_fee_cents <= max_adoption_fee_cents`.
- Reject negative values by raising `ValueError` before performing the search.
- Apply the fee filter after all other filters (query, species, status, tag) to maintain composability.
- Use the existing filtering pattern (sequential checks in the loop).

## Risks

- **Backward compatibility**: Adding an optional parameter with a default value of `None` preserves existing behavior. All current callers continue to work unchanged.
- **Validation placement**: Validate `max_adoption_fee_cents` alongside the existing `max_results` validation at the function entry point.
- **Edge case: zero fee**: A max fee of zero cents is technically valid (free pets) and should not be rejected. Only negative values are invalid.

## Validation Plan

- Run focused unit tests: `python3 -m pytest -q app/tests/test_pet_catalog.py::test_search_pets_filters_by_max_adoption_fee`
- Run focused unit tests: `python3 -m pytest -q app/tests/test_pet_catalog.py::test_search_pets_validates_negative_max_adoption_fee`
- Run full catalog test suite: `python3 -m pytest -q app/tests/test_pet_catalog.py`
- Verify log scenario: pets within $75 budget (7500 cents) should exclude Scout (12500 cents).
