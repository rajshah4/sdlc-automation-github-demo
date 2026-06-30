# Design

## Context

The Petstore catalog search function (`app/petstore_app/catalog.py::search_pets`) currently supports filtering by:
- Text query (pet name)
- Species
- Status (default: "available")
- Tag
- Max results (with validation)

Pet data includes `age_months` as an integer field. The requirement is to add optional age range filtering without breaking existing behavior or requiring UI changes.

## Decision

- Add two optional parameters to `search_pets()`: `min_age_months` and `max_age_months`
- Both parameters default to `None` (no age filtering)
- When `min_age_months` is provided, filter pets with `age_months >= min_age_months`
- When `max_age_months` is provided, filter pets with `age_months <= max_age_months`
- Both can be used together to specify a range
- Validate that age values are non-negative
- Validate that `min_age_months <= max_age_months` when both are provided
- Raise `ValueError` with descriptive messages for invalid inputs
- Age filtering applies after all other filters (query, species, status, tag)

## Risks

- **Risk**: Age filtering could conflict with other filters if not applied in the correct order
  - **Mitigation**: Apply age filtering in the same loop as other filters, maintaining the existing filter chain pattern

- **Risk**: Invalid age ranges could cause confusing behavior
  - **Mitigation**: Validate parameters at the start of the function before any filtering logic

- **Risk**: Breaking change if callers pass unexpected keyword arguments
  - **Mitigation**: This is an additive change; existing callers are unaffected since parameters default to None

## Validation Plan

- Run focused catalog tests: `python3 -m pytest app/tests/test_pet_catalog.py -v`
- Add new test cases covering:
  - Minimum age filtering (inclusive boundary)
  - Maximum age filtering (inclusive boundary)
  - Age range filtering (both min and max)
  - Combined with species filter
  - Negative age validation
  - Inverted range validation
  - Preserves default status filtering
- Run full test suite: `python3 -m pytest app/tests/ -v`
