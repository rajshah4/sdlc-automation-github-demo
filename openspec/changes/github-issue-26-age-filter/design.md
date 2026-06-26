# Design

## Context

The Petstore catalog already supports search filtering by query, species, status, and tag. The `Pet` dataclass includes an `age_months` field (integer). The `search_pets` function returns a filtered list of pets.

## Decision

- Add optional `min_age: int | None = None` and `max_age: int | None = None` parameters to `search_pets`.
- Apply age filtering after other filters in the existing loop.
- Validate that `min_age` and `max_age` are non-negative when provided.
- Validate that `min_age <= max_age` when both are provided.
- Raise `ValueError` with descriptive messages for invalid inputs.

## Risks

- **Risk**: Inverted ranges or negative ages could cause confusion if not validated.  
  **Mitigation**: Add explicit validation with clear error messages before filtering.

- **Risk**: Edge case where min_age equals max_age.  
  **Mitigation**: This is valid and should return pets with exactly that age.

## Validation Plan

- Run `pytest app/tests/test_pet_catalog.py` to verify:
  - Age filtering includes pets within range
  - Age filtering excludes pets outside range
  - Negative ages raise ValueError
  - Inverted ranges (min > max) raise ValueError
  - Edge case: min_age == max_age returns exact matches
