# Petstore Catalog Spec Delta

## ADDED Requirements

### Requirement: Empty status parameter defaults to available pets

When the `search_pets()` function is called with an empty status string, it must return only pets with `status="available"`, not all pets.

#### Scenario: Empty status string excludes pending pets

- Given the catalog contains pet-103 (Nova) with `status="pending"`
- And the catalog contains pet-100, pet-101, pet-102 with `status="available"`
- When `search_pets(status="")` is called
- Then only available pets (pet-100, pet-101, pet-102) are returned
- And pending pets (pet-103) are excluded

#### Scenario: Explicit available status works correctly

- Given the catalog contains pets with various statuses
- When `search_pets(status="available")` is called
- Then only pets with `status="available"` are returned

#### Scenario: Explicit pending status continues to work

- Given support or operations needs to view pending pets
- When `search_pets(status="pending")` is called with explicit intent
- Then only pets with `status="pending"` are returned
- And this capability remains available for operational workflows

## UNCHANGED Requirements

### Requirement: Default parameter behavior

- The `search_pets()` function continues to default to `status="available"` when no status parameter is provided
- Existing callers are unaffected

### Requirement: Species and tag filtering

- Species filtering continues to work correctly
- Tag filtering continues to work correctly
- Multiple filters can be combined as before

## Acceptance Criteria

1. Unit test passes: `search_pets(status="")` returns only available pets
2. Existing tests continue to pass without modification
3. UI Playwright test confirms no regression in frontend behavior
4. Error log pattern `PENDING_PET_VISIBLE` should not recur for this root cause
