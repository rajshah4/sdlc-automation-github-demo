# Design

## Context

The Petstore catalog uses `search_pets()` in `app/petstore_app/catalog.py` to filter pets by name query, species, status, and tag. Each pet has an `age_months` integer field. The default search returns only "available" pets unless explicitly requested otherwise.

Customers report seeing pets they shouldn't be able to adopt, and age-based filtering would help them find appropriate pets for their household.

## Decision

- Add two optional keyword parameters: `min_age_months: int | None = None` and `max_age_months: int | None = None`
- Filter pets after other filters (species, status, tag) are applied
- Validate parameters before filtering:
  - Both parameters must be >= 0 if provided
  - If both are provided, `min_age_months` must be <= `max_age_months`
- Use inclusive range checking: `min_age_months <= pet.age_months <= max_age_months`
- Maintain existing behavior when neither parameter is provided

## Risks

- **Risk**: Customers may expect different age units (years vs. months)
  - **Mitigation**: Use the existing `age_months` field consistently; document parameter names clearly
  
- **Risk**: Invalid range specification could cause confusion
  - **Mitigation**: Validate parameters early with clear error messages

- **Risk**: Age filtering combined with other filters might return empty results
  - **Mitigation**: Filters are optional and independent; expected behavior

## Validation Plan

- Run existing catalog tests to ensure no regression: `python -m pytest app/tests/test_pet_catalog.py -v`
- Run new age filter tests to verify implementation
- Verify all test scenarios from spec.md pass
