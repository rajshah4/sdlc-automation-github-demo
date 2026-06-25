# Design

## Context

The Petstore catalog maintains a list of pets with adoption fees stored as integer cents. The `search_pets()` function currently supports filtering by query string, species, status, and tag. Default search behavior returns only available pets unless a different status is explicitly requested.

Existing pet data:
- Mochi (cat): 7500 cents ($75.00)
- Scout (dog): 12500 cents ($125.00)  
- Pip (rabbit): 4500 cents ($45.00)
- Nova (dog, pending): 11000 cents ($110.00)

## Decision

1. Add a keyword-only optional `max_adoption_fee_cents: int | None = None` parameter to the `search_pets()` function signature
2. Add validation: raise `ValueError` if `max_adoption_fee_cents` is provided and is negative
3. Apply the fee filter in the existing pet iteration loop, after other filter checks
4. Exclude pets where `pet.adoption_fee_cents > max_adoption_fee_cents` when the parameter is provided
5. When the parameter is omitted (`None`), no fee filtering is applied

## Implementation Details

- Place the fee filter check after species/status/tag filters to maintain logical flow
- Use existing validation pattern (consistent with `max_results` validation)
- Preserve all existing search behavior when the parameter is not provided
- No changes to the `Pet` dataclass or `PETS` data
- No API endpoint changes (this is a library function used by future API/UI)

## Risks

- **Money representation**: Using floats instead of integer cents could introduce rounding errors. Mitigation: Keep integer cents throughout.
- **Default behavior regression**: Accidentally changing the default status filter could expose pending pets inappropriately. Mitigation: Preserve existing default `status="available"` and test explicitly.
- **Filter interaction**: The fee cap could conflict with other filters. Mitigation: Apply filters sequentially and test combinations.
- **Negative fee validation**: Accepting negative fees would be nonsensical. Mitigation: Validate and raise `ValueError` for negative values.

## Validation Plan

1. Run focused catalog tests:
   - `test_search_pets_filters_by_max_adoption_fee`: Verify Mochi ($75) and Pip ($45) match, Scout ($125) excluded for $75 cap
   - `test_search_pets_combines_fee_cap_with_existing_filters`: Verify fee cap works with tag filters
   - `test_search_pets_rejects_negative_max_adoption_fee`: Verify ValueError for negative fee

2. Run full test suite: `python -m pytest app/tests/ -v`

3. Manual verification:
   - Search with max_adoption_fee_cents=7500 should return Mochi and Pip only
   - Search with max_adoption_fee_cents=10000 should return Mochi and Pip only (Scout still excluded)
   - Search without fee parameter should return Mochi, Scout, Pip (default behavior preserved)

## Evidence

Implementation validates against log scenario in `docs/logs/pet-search-budget-limit.ndjson`:
- Family request: budget_limit_dollars=75 (7500 cents)
- Expected: Mochi ($75), Pip ($45)
- Incorrectly included before fix: Scout ($125)
- After fix: Scout correctly excluded
