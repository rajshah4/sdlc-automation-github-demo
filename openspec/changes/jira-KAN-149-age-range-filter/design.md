# Design

## Context

The Petstore catalog search function (`search_pets` in `app/petstore_app/catalog.py`) currently supports filtering by:
- Query text (pet name)
- Species
- Status (defaults to "available")
- Tag
- Max results limit

Pets are stored with an `age_months` field representing their age in integer months. The existing implementation uses sequential filtering where each criterion eliminates non-matching pets from the result set.

## Decision

- Add two optional keyword-only parameters to `search_pets()`: `min_age_months: int | None = None` and `max_age_months: int | None = None`
- Validate age parameters before filtering begins:
  - Reject negative minimum age with `ValueError`
  - Reject negative maximum age with `ValueError`
  - Reject inverted range (min > max) when both are provided
- Apply age filtering in the existing filter loop after other criteria
- Treat `None` values as "no filter" for that boundary
- Keep the implementation simple with inline validation and filtering

## Alternative Considered: Separate validation function

Could extract validation logic to a separate function, but given the simple parameter checks and single usage location, inline validation is more direct and maintainable.

## Risks

- **Risk**: Age filtering might inadvertently affect pending pet visibility
  - **Mitigation**: Existing status filtering happens before age filtering, maintaining the default available-only behavior
  
- **Risk**: Invalid parameter combinations might produce confusing error messages
  - **Mitigation**: Clear, specific error messages for each validation failure case

## Validation Plan

1. Run existing tests to ensure no regression: `python3 -m pytest app/tests/test_pet_catalog.py -v`
2. Add and run new age filtering tests covering:
   - Minimum age only
   - Maximum age only
   - Age range (both min and max)
   - Boundary conditions (exact matches, zero values)
   - Validation errors (negative values, inverted range)
   - Interaction with existing filters (species, status)
3. Verify default behavior unchanged: available-only search still excludes pending pets
