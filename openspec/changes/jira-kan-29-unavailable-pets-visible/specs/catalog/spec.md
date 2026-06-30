# Catalog Availability Spec Delta

## ADDED Requirements

### Requirement: Default pet search excludes unavailable animals

The default customer-facing pet catalog must show only pets with `status="available"`. Pending, adopted, or any non-available pets must not appear in default searches.

#### Scenario: Default search returns only available pets

- Given a catalog containing pets with mixed statuses (available, pending)
- When a user performs a default search with no status filter specified
- Then only pets with `status="available"` are returned

#### Scenario: Empty status parameter treated as available-only filter

- Given a catalog containing pets with mixed statuses
- When a user performs a search with an empty string status parameter
- Then only pets with `status="available"` are returned

#### Scenario: Species filter combined with default status

- Given a catalog containing dogs with different statuses (Scout available, Nova pending)
- When a user searches for species="dog" with default status
- Then only available dogs are returned (Scout yes, Nova no)

### Requirement: Explicit pending searches remain functional

Support and operations workflows must be able to explicitly request pending pets when investigating cases.

#### Scenario: Explicit pending search returns only pending pets

- Given a catalog containing pets with mixed statuses
- When a user explicitly requests `status="pending"`
- Then only pets with `status="pending"` are returned

#### Scenario: Pending pets never leak into available-only results

- Given pet-103 (Nova) has `status="pending"`
- When a user performs any available-only search
- Then Nova must not appear in results
- And the log must not contain `PENDING_PET_VISIBLE` error code
