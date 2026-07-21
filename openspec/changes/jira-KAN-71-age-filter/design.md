# Design

## Context

The Petstore catalog tracks pet age in months (`age_months` field). The current `search_pets()` function supports filtering by query string, species, status, and tag. Age filtering must integrate with existing filters without breaking default behavior.

Current catalog data:
- Mochi (cat): 18 months
- Scout (dog): 28 months  
- Pip (rabbit): 9 months
- Nova (dog): 14 months, pending status

## Decision

- Add two optional parameters to `search_pets()`: `min_age_months` and `max_age_months`
- Default value: `None` for both parameters (no filtering)
- Validation: Both must be non-negative integers; `min_age_months <= max_age_months` when both specified
- Filter logic: Apply after existing status/species/tag filters, before max_results limit
- Preserve existing behavior: Default search still returns only available pets unless status is explicitly specified

## Risks

**Risk**: Invalid age parameters could cause runtime errors  
**Mitigation**: Validate inputs early with clear error messages; add comprehensive test coverage

**Risk**: Age filtering might interact unexpectedly with other filters  
**Mitigation**: Add combination tests (age + species, age + status); age filter should compose naturally with existing filters

**Risk**: Breaking existing behavior if default parameters change  
**Mitigation**: Both age parameters default to `None`; existing calls work unchanged

## Validation Plan

- Run focused unit tests: `python3 -m pytest app/tests/test_pet_catalog.py -v`
- Verify existing tests still pass (regression check)
- Confirm new age filter tests cover: min only, max only, range, validation errors, combination with species/status
