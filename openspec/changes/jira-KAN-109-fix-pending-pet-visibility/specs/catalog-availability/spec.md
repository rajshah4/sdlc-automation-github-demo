# Catalog Availability Spec Delta

## ADDED Requirements

### Requirement: Default search excludes pending pets

The default catalog search operation must return only pets with status="available" and must not return pets with status="pending" or any other non-available status.

#### Scenario: Default search with no status parameter

- Given the catalog contains both available and pending pets
- When a caller invokes `search_pets()` without specifying a status parameter
- Then only pets with status="available" are returned
- And pets with status="pending" are excluded from results

#### Scenario: Default search with empty status string

- Given the catalog contains both available and pending pets
- When a caller invokes `search_pets(status="")` with an explicit empty string
- Then the default status="available" filter is still applied
- And only pets with status="available" are returned
- And pets with status="pending" are excluded from results

### Requirement: Explicit pending status search continues to work

Support and operations workflows that explicitly request pending pets must continue to function correctly.

#### Scenario: Explicit pending status search

- Given the catalog contains both available and pending pets
- When a caller invokes `search_pets(status="pending")`
- Then only pets with status="pending" are returned
- And pets with status="available" are excluded from results

## CHANGED Requirements

None. The existing requirement that default search returns only available pets was already documented in `docs/wiki/petstore-catalog-availability.md`, but the implementation had a regression bug.

## REMOVED Requirements

None.
