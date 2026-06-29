# Catalog Availability Spec Delta

## ADDED Requirements

### Requirement: Empty status parameter defaults to available-only results

#### Scenario: Search with empty status string

- Given the catalog contains pets with status "available" and status "pending"
- When a search is performed with status=""
- Then only pets with status "available" are returned
- And pets with status "pending" are excluded

#### Scenario: Search with whitespace-only status string

- Given the catalog contains pets with status "available" and status "pending"  
- When a search is performed with status="  "
- Then only pets with status "available" are returned
- And pets with status "pending" are excluded

#### Scenario: Search with no status parameter uses default

- Given the catalog contains pets with status "available" and status "pending"
- When a search is performed with no status parameter
- Then only pets with status "available" are returned
- And pets with status "pending" are excluded

### Requirement: Explicit pending status searches still work

#### Scenario: Operations explicitly request pending pets

- Given the catalog contains pets with status "pending"
- When a search is performed with status="pending"
- Then only pets with status "pending" are returned
- And pets with status "available" are excluded
