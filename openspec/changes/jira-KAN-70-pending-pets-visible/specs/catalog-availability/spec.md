# Catalog Availability Spec Delta

## ADDED Requirements

### Requirement: Default catalog search excludes pending pets

#### Scenario: Default search without status parameter

- Given the catalog contains pets with mixed availability status
- When a customer performs a default search with no status parameter
- Then only pets with status="available" are returned
- And pets with status="pending" are excluded

#### Scenario: Empty status string defaults to available-only

- Given the catalog contains pets with mixed availability status
- When a customer performs a search with an empty status string
- Then only pets with status="available" are returned
- And pets with status="pending" are excluded

#### Scenario: Explicit pending status search for support workflows

- Given the catalog contains pets with status="pending"
- When support staff explicitly requests status="pending"
- Then pending pets are returned as requested
- And this capability remains unchanged

## UNCHANGED Requirements

### Requirement: Species filtering works with default status

- Given the catalog contains dogs with various status values
- When searching by species="dog" with default status
- Then only available dogs are returned

## Acceptance Criteria

- [x] Default search excludes pending pets
- [x] Empty status string defaults to available-only behavior
- [x] Explicit pending searches still work for support workflows
- [x] Regression tests added and passing
- [x] No changes to unrelated catalog behavior
