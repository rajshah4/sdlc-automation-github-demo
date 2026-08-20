# Design

## Context

The Petstore catalog search (`app/petstore_app/catalog.py`) currently supports filtering by:
- Query string (pet name substring match)
- Species (exact match)
- Status (defaults to "available")
- Tag (must be present in pet's tags)
- Max results (with validation)

The Pet dataclass already includes `age_months: int` field. The sample data includes:
- Mochi (cat): 18 months
- Scout (dog): 28 months
- Pip (rabbit): 9 months
- Nova (dog, pending): 14 months

The implementation map at `skills/sdlc-story/references/petstore-implementation-map.md` provides explicit guidance for age range filtering.

## Decision

- Add two optional parameters to `search_pets()`: `min_age_months: int | None = None` and `max_age_months: int | None = None`
- Validate parameters before filtering:
  - Both parameters must be non-negative if provided
  - If both provided, min_age_months must not exceed max_age_months
- Apply age filtering after other filters in the existing filter loop
- Keep parameter validation consistent with existing `max_results` validation pattern
- Use clear, specific error messages for validation failures

## Risks

- **Breaking changes**: Low risk - adding optional parameters maintains backward compatibility
- **Performance**: Low risk - filtering in memory over small dataset (4 pets in sample data)
- **Edge cases**: Mitigated by explicit validation of negative values and inverted ranges
- **Interaction with other filters**: Low risk - age filtering composes naturally with existing filters in the same loop

## Validation Plan

1. Run existing catalog tests to ensure no regression: `python3 -m pytest app/tests/test_pet_catalog.py -v`
2. Add new tests covering:
   - Minimum age filter only
   - Maximum age filter only
   - Both min and max (range filter)
   - Age filter combined with species filter
   - Validation: negative min_age
   - Validation: negative max_age
   - Validation: inverted range (min > max)
3. Run full test suite: `python3 -m pytest app/tests/ -v`
4. Verify test coverage includes all scenarios from spec delta
