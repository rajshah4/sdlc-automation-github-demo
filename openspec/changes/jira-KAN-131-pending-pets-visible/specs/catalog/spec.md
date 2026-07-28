# Catalog Availability Spec Delta

## ADDED Requirements

### Requirement: Default search must exclude pending pets

#### Scenario: Search with default status returns only available pets

- Given the catalog contains available and pending pets
- When a search is performed with the default status parameter
- Then only pets with status="available" are returned

#### Scenario: Search with empty status string returns only available pets

- Given the catalog contains available and pending pets (including pet-103 "Nova" with status="pending")
- When a search is performed with status=""
- Then only pets with status="available" are returned
- And pending pets like Nova (pet-103) are excluded

#### Scenario: Explicit pending search still works for operations

- Given operations needs to view pending pets
- When a search is performed with status="pending"
- Then only pets with status="pending" are returned
- And this workflow remains functional for operations team

## MODIFIED Requirements

None. The intended requirement already existed but was not enforced for empty status parameters.

## REMOVED Requirements

None.
