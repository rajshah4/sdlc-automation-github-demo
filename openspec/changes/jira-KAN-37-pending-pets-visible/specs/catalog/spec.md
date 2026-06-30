# Catalog Availability Spec Delta

## ADDED Requirements

### Requirement: Default search must exclude pending pets

#### Scenario: Default search with no status parameter

- Given a catalog with mixed available and pending pets
- When a user calls `search_pets()` with no status parameter
- Then only pets with `status="available"` are returned
- And pets with `status="pending"` are never included

#### Scenario: Explicit available-only search

- Given a catalog with mixed available and pending pets
- When a user calls `search_pets(status="available")`
- Then only pets with `status="available"` are returned
- And pets with `status="pending"` are never included

#### Scenario: Empty status string treated as default

- Given a catalog with mixed available and pending pets
- When a user calls `search_pets(status="")`
- Then only pets with `status="available"` are returned
- And the empty status is treated as the default "available" filter

### Requirement: Explicit pending searches remain functional

#### Scenario: Support workflow searches for pending pets

- Given a catalog with mixed available and pending pets
- When a support user calls `search_pets(status="pending")`
- Then only pets with `status="pending"` are returned
- And this explicit pending search continues to work for operations workflows

### Requirement: Species filters respect status default

#### Scenario: Species search with default status

- Given a catalog with available and pending dogs
- When a user calls `search_pets(species="dog")`
- Then only available dogs are returned
- And pending dogs (like Nova/pet-103) are excluded
