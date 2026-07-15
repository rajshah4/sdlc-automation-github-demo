# Catalog Size Filter Spec Delta

## ADDED Requirements

### Requirement: Pet size filter

Catalog search supports an optional size filter that returns only pets matching the selected size.

#### Scenario: Filter by small size

- Given multiple pets of different sizes exist in the catalog
- When a user searches with size="small"
- Then only pets with size "small" are returned
- And pets with size "medium" or "large" are excluded

#### Scenario: Filter by medium size

- Given multiple pets of different sizes exist in the catalog
- When a user searches with size="medium"
- Then only pets with size "medium" are returned
- And pets with other sizes are excluded

#### Scenario: Filter by large size

- Given multiple pets of different sizes exist in the catalog
- When a user searches with size="large"
- Then only pets with size "large" are returned
- And pets with other sizes are excluded

#### Scenario: No size filter specified

- Given multiple pets of different sizes exist in the catalog
- When a user searches without specifying size
- Then all pets matching other criteria are returned
- And size does not affect the results

#### Scenario: Size filter combined with other filters

- Given multiple pets exist with various sizes and species
- When a user searches with both size and species filters
- Then only pets matching both criteria are returned

### Requirement: Default catalog behavior preserved

When no size filter is specified, the catalog search continues to return pets based on existing filters (status, species, tag, query) without any size-based exclusion.

#### Scenario: Default search behavior unchanged

- Given the catalog has pets of various sizes
- When a user performs a default search (available pets only)
- Then pets are returned based on status="available" as before
- And size does not influence the default result set
