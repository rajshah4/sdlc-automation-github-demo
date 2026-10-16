# Pet Catalog Availability Spec Delta

## ADDED Requirements

### Requirement: Explicit test coverage for pending pet exclusion rule

The default catalog search MUST exclude pending pets from results, and this rule MUST be explicitly tested to prevent regressions.

#### Scenario: Default search excludes pending pets

- Given Nova (pet-103) has status `pending`
- And Mochi (pet-100), Scout (pet-101), and Pip (pet-102) have status `available`
- When `search_pets()` is called with no status parameter (using default `status="available"`)
- Then the results include pet-100, pet-101, and pet-102
- And the results do NOT include pet-103

#### Scenario: Default species filter excludes pending pets of that species

- Given Scout (pet-101, dog) has status `available`
- And Nova (pet-103, dog) has status `pending`
- When `search_pets(species="dog")` is called (using default `status="available"`)
- Then the results include only Scout (pet-101)
- And the results do NOT include Nova (pet-103)

#### Scenario: Explicit pending search returns pending pets

- Given Nova (pet-103, dog) has status `pending`
- When `search_pets(species="dog", status="pending")` is called
- Then the results include Nova (pet-103)
- And the results do NOT include Scout (pet-101, available)
