# Design

## Context

The Petstore catalog currently supports searching pets by name, species, status, and tag. The `search_pets()` function returns results in the order they appear in the `PETS` tuple. Adoption fees are already stored as `adoption_fee_cents` (integer cents per the Petstore product rules).

## Decision

- Add an optional `sort_by` parameter to `search_pets()` with default value `None`.
- When `sort_by="adoption_fee"`, sort the matched results by `adoption_fee_cents` in ascending order before applying `max_results` limit.
- When `sort_by` is `None` or any other value, preserve the current behavior (no sorting).
- Sorting happens after filtering and before applying the `max_results` limit to ensure the lowest-fee pets are returned.

## Risks

- **Risk**: Adding a parameter could break existing callers if they use positional arguments incorrectly.
  - **Mitigation**: Use keyword-only parameter (after the `*` in the function signature) to prevent accidental positional usage.

- **Risk**: Sorting could change performance characteristics if the catalog grows.
  - **Mitigation**: Current catalog is small (4 pets); sorting is acceptable. Document in PR that this is an in-memory sort suitable for the demo scope.

## Validation Plan

- Run `pytest app/tests/test_pet_catalog.py -v` to verify new tests pass.
- Verify all existing tests still pass (regression check).
- Manually inspect sorted output to confirm ascending order by adoption fee.
