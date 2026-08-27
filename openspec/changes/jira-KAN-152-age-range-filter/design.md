# Design: Age Range Filter

## Context

The petstore catalog currently supports filtering by name (query), species, status, and tags. Customers need the ability to filter pets by age to find pets that match their lifestyle and preferences (e.g., puppies vs. adult dogs, young cats for active families).

The `Pet` dataclass already includes an `age_months: int` field, so no schema changes are needed. The `search_pets()` function in `app/petstore_app/catalog.py` uses a sequential filtering approach that can easily accommodate additional optional filters.

## Decision

Add two optional keyword-only parameters to `search_pets()`:
- `min_age_months: int | None = None` - Include only pets at or above this age
- `max_age_months: int | None = None` - Include only pets at or below this age

**Validation approach:**
1. If `min_age_months` is provided and negative, raise ValueError
2. If `max_age_months` is provided and negative, raise ValueError  
3. If both provided and min > max, raise ValueError with clear message

**Filtering approach:**
After existing filters (query, species, status, tag), add age filtering:
- If `min_age_months` provided, exclude pets with `age_months < min_age_months`
- If `max_age_months` provided, exclude pets with `age_months > max_age_months`

**Files changed:**
- `app/petstore_app/catalog.py` - Add parameters and filtering logic
- `app/tests/test_pet_catalog.py` - Add comprehensive test coverage

**Backwards compatibility:**
✓ Parameters are optional with None defaults
✓ Existing callers work without modification
✓ All existing filters and validations preserved

## Risks

**Low overall risk:**

✓ Pure addition - no modifications to existing behavior
✓ Well-scoped filtering logic
✓ Comprehensive validation prevents invalid input
✓ Test coverage for all scenarios
✓ No dependencies, schema changes, or external service calls

**Potential issues:**
- None identified - straightforward filter addition

## Validation Plan

1. Run existing tests: `python3 -m pytest -q app/tests/test_pet_catalog.py`
2. Verify all existing tests pass (no regressions)
3. Run new age filtering tests
4. Verify validation raises appropriate errors
5. Confirm age filters work standalone and combined with other filters
6. Confirm default status="available" behavior preserved
