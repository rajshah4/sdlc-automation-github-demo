# Design

## Context

The Petstore catalog search function (`search_pets`) already supports filtering by query, species, status, and tag. Each Pet has an `adoption_fee_cents` field storing the fee as integer cents. The current implementation returns only available pets by default.

## Decision

- Add optional `max_fee_cents: int | None = None` parameter to `search_pets()`.
- When `max_fee_cents` is provided, filter pets where `pet.adoption_fee_cents <= max_fee_cents`.
- Validate that `max_fee_cents`, if provided, is non-negative. Raise ValueError for negative values.
- Place the validation early in the function, alongside existing `max_results` validation.
- Place the fee filter in the main loop with other filter conditions.

## Risks

- **Risk**: Negative fee handling could be inconsistent with other validation.
  - **Mitigation**: Follow the existing `max_results` validation pattern for consistency.

- **Risk**: Fee comparison could fail if adoption_fee_cents is not an integer.
  - **Mitigation**: The Pet dataclass enforces type; no additional runtime check needed.

## Validation Plan

- Run focused unit tests: `pytest app/tests/test_pet_catalog.py -v`
- Tests will verify:
  - Pets within budget are returned
  - Pets above budget are excluded
  - Negative fees raise ValueError
  - No max_fee_cents parameter behaves as before (no filtering)
