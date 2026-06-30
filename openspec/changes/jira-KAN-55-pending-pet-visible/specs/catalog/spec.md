# Pet Catalog Status Filtering Spec Delta

## ADDED Requirements

### Requirement: Default pet search excludes pending pets

Default pet searches MUST return only pets with `status="available"` and MUST NOT include pending pets.

#### Scenario: Default search excludes Nova

- Given Nova (pet-103) has status="pending"
- When a user performs a default pet search with no status parameter
- Then Nova MUST NOT appear in the results
- And only available pets (pet-100, pet-101, pet-102) MUST be returned

#### Scenario: Empty status parameter excludes pending pets

- Given Nova (pet-103) has status="pending"
- When a user performs a pet search with status=""
- Then Nova MUST NOT appear in the results
- And only available pets MUST be returned

### Requirement: Explicit pending search works correctly

Explicit pending searches MUST work when `status="pending"` is provided.

#### Scenario: Explicit pending search returns Nova

- Given Nova (pet-103) has status="pending"
- When a user performs a pet search with status="pending"
- Then Nova MUST appear in the results
- And available pets MUST NOT appear in the results

### Requirement: Species filter respects status filter

Species filtering combined with default status filtering MUST correctly exclude pending pets.

#### Scenario: Species filter with default status excludes pending dogs

- Given Nova (pet-103) is a dog with status="pending"
- And Scout (pet-101) is a dog with status="available"
- When a user searches for species="dog" with no status parameter
- Then only Scout MUST be returned
- And Nova MUST NOT be returned
