# Catalog Availability Spec Delta

## MODIFIED Requirements

### Requirement: Default pet search returns only available pets

#### Scenario: Search with default status parameter

- Given the pet catalog contains pets with mixed statuses (available and pending)
- When a search is performed without specifying a status parameter
- Then only pets with status="available" are returned

#### Scenario: Search with explicit empty status parameter

- Given the pet catalog contains pets with mixed statuses (available and pending)
- When a search is performed with `status=""` (empty string)
- Then only pets with status="available" are returned (defaulting to available behavior)

#### Scenario: Search with whitespace-only status parameter

- Given the pet catalog contains pets with mixed statuses (available and pending)
- When a search is performed with `status="  "` (whitespace only)
- Then only pets with status="available" are returned (defaulting to available behavior)

#### Scenario: Search with explicit "available" status

- Given the pet catalog contains pets with mixed statuses
- When a search is performed with `status="available"`
- Then only pets with status="available" are returned

#### Scenario: Search with explicit "pending" status

- Given the pet catalog contains pets with mixed statuses
- When a search is performed with `status="pending"`
- Then only pets with status="pending" are returned

## PRESERVED Requirements

### Requirement: Support and operations can explicitly request pending pets

- When `status="pending"` is explicitly passed
- Then pending pets are returned for investigation workflows

### Requirement: Species and tag filters work independently of status

- Status filtering does not interfere with optional species or tag filters
- All combinations of query, species, status, and tag filters work correctly
