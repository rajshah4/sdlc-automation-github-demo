# Catalog Search Spec Delta

## MODIFIED Requirements

### Requirement: Default search returns only available pets

#### Scenario: Search with default status parameter

- Given the catalog contains pets with status "available" and "pending"
- When `search_pets()` is called with default parameters
- Then only pets with status "available" are returned

#### Scenario: Search with empty status string

- Given the catalog contains pets with status "available" and "pending"
- When `search_pets(status="")` is called with an empty status string
- Then only pets with status "available" are returned
- And pending pets are excluded from results

#### Scenario: Search with explicit "pending" status

- Given the catalog contains a pending pet named "Nova"
- When `search_pets(status="pending")` is called
- Then only pending pets are returned
- And available pets are excluded from results

## UNCHANGED Requirements

### Requirement: Species filter works correctly

- Existing behavior preserved

### Requirement: Tag filter works correctly

- Existing behavior preserved

### Requirement: Name query search works correctly

- Existing behavior preserved
