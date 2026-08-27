# Catalog Availability Spec Delta

## ADDED Requirements

### Requirement: Default catalog search excludes pending pets

The default customer-facing pet catalog must show only pets with `status="available"`. Pending pets must never appear unless explicitly requested via `status="pending"` parameter.

#### Scenario: Default search with no status filter

- Given a catalog containing both available and pending pets
- When a customer performs a default search with no explicit status parameter
- Then only pets with `status="available"` are returned
- And pending pets (like Nova/pet-103) are excluded from results

#### Scenario: Species filter without explicit status

- Given a catalog containing dogs with both available and pending status
- When a customer filters by species="dog" without specifying status
- Then only available dogs are returned
- And pending dogs are excluded from results

#### Scenario: Frontend UI displays only available pets

- Given the web UI loads with the default pet list
- When the page renders the available pets section
- Then the displayed list contains only available pets
- And Nova (pet-103, status="pending") is not visible to customers

## MODIFIED Requirements

None - existing explicit `status="pending"` support searches remain unchanged.

## REMOVED Requirements

None.
