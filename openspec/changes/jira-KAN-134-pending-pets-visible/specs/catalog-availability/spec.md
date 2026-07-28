# Catalog Availability Spec Delta

## ADDED Requirements

### Requirement: Default search excludes pending pets

#### Scenario: Empty status parameter defaults to available-only

- Given the catalog contains pets with mixed statuses (available and pending)
- When a search is performed with an empty or whitespace-only status parameter
- Then only pets with `status="available"` are returned
- And pending pets (like Nova/pet-103) are excluded

#### Scenario: Explicit pending status still works for support

- Given the catalog contains pending pets
- When a search is performed with `status="pending"`
- Then only pending pets are returned
- And available pets are excluded

#### Scenario: Default status parameter excludes pending pets

- Given the catalog contains both available and pending pets
- When a search is performed without specifying a status parameter
- Then only pets with `status="available"` are returned
- And pending pets are excluded from results
