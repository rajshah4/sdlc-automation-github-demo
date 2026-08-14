# Design

## Context

The Petstore catalog currently supports filtering by species, status, tag, and max adoption fee. The `Pet` dataclass includes an `age_months` field that stores the pet's age as an integer representing months. Adopters want to filter by age range to find pets matching their preferences (puppies, adults, seniors).

## Decision

- Add two optional parameters to `search_pets()`: `min_age_months` and `max_age_months`.
- Both parameters default to `None`, meaning no age filtering.
- Validate that age values are non-negative.
- Validate that when both are provided, `min_age_months <= max_age_months`.
- Apply filters inclusively: pets with `age_months` exactly at the boundary are included.
- Follow the existing pattern used for `max_fee_cents` validation and filtering.

## Risks

- **Inverted range risk**: If a caller passes `min_age_months > max_age_months`, the result would be an empty list. Mitigation: raise `ValueError` early in validation.
- **Negative age risk**: Negative ages are nonsensical. Mitigation: validate `>= 0` for both parameters.
- **Boundary confusion**: Users might expect exclusive boundaries. Mitigation: document inclusive behavior and test boundary cases.

## Validation Plan

- Unit tests for happy path: filter by min only, max only, and both.
- Unit tests for boundaries: pets at exact min/max are included.
- Unit tests for validation: reject negative ages and inverted ranges.
- Unit tests for optional behavior: `None` values mean no filtering.
- Run `pytest app/tests/test_pet_catalog.py -v` to verify all tests pass.
