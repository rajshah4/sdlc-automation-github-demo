# Catalog Availability Spec Delta

## ADDED Requirements

### Requirement: Default pet search returns only available pets

Default customer-facing catalog search must exclude pets with `status="pending"`.

#### Scenario: Default search excludes pending pets

- Given the catalog contains Nova (pet-103) with status="pending"
- And the catalog contains Scout (pet-101) with status="available"
- When a customer performs a default search with no status parameter
- Then the results include only available pets
- And Nova does not appear in the results

#### Scenario: Default species search excludes pending pets

- Given the catalog contains two dogs: Scout (available) and Nova (pending)
- When a customer searches for species="dog" with default status
- Then only Scout (pet-101) is returned
- And Nova (pet-103) is excluded from results

### Requirement: Explicit pending search returns pending pets

Operations users must be able to explicitly search for pending pets.

#### Scenario: Explicit pending search finds Nova

- Given the catalog contains Nova (pet-103) with status="pending"
- When an operations user searches with status="pending"
- Then Nova appears in the results
- And available pets are excluded

## UNCHANGED Requirements

### Requirement: Search validates max_results parameter

- Given max_results must be between 1 and 50
- When a search is performed with max_results outside this range
- Then a ValueError is raised

### Requirement: Search filters by species and tags

- Given a search can filter by species (e.g., "dog", "cat", "rabbit")
- And a search can filter by tag (e.g., "indoor", "active")
- When these filters are applied
- Then only pets matching all specified filters are returned
