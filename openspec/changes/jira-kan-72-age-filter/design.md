# Design

## Context

The Petstore catalog currently supports filtering by query text, species, status, and tag. The `search_pets()` function in `app/petstore_app/catalog.py` uses a simple iterative filter pattern where each pet is checked against all provided criteria.

Each pet already has an `age_months` field (integer) representing the pet's age. The existing filter logic is straightforward: for each criterion, skip pets that don't match and continue to the next pet.

Default search behavior returns only available pets (`status="available"`). This must remain unchanged.

## Decision

- Add optional `min_age_months: int | None = None` parameter to `search_pets()`.
- Add optional `max_age_months: int | None = None` parameter to `search_pets()`.
- Validate age parameters early in the function:
  - Reject negative `min_age_months` with ValueError.
  - Reject negative `max_age_months` with ValueError.
  - Reject when `min_age_months > max_age_months` with ValueError.
- Add age filtering to the existing filter loop:
  - Skip pets where `pet.age_months < min_age_months` (when min is provided).
  - Skip pets where `pet.age_months > max_age_months` (when max is provided).
- Place age validation before the main loop to fail fast.
- Place age filtering after status/species/tag filters in the loop (order doesn't affect correctness).

## Risks

- **Risk**: Age boundaries could be confused (inclusive vs exclusive).
  - **Mitigation**: Use clear inclusive semantics (≤ and ≥). Document in tests.
  
- **Risk**: Large age values could be mistyped (e.g., years instead of months).
  - **Mitigation**: No upper bound validation initially. Can add later if needed.
  
- **Risk**: None values vs zero values could be confused.
  - **Mitigation**: Use `None` as "no filter" and validate that explicit values are non-negative.

## Validation Plan

- Run existing catalog tests to ensure no regression: `python3 -m pytest -q app/tests/test_pet_catalog.py`
- Add new tests for:
  - Minimum age filtering (returns only older pets)
  - Maximum age filtering (returns only younger pets)
  - Age range filtering (returns pets within range)
  - Negative age rejection (both min and max)
  - Inverted range rejection (min > max)
  - Age + status combination
  - Age + species combination
- Run full test suite: `python3 -m pytest -q`
