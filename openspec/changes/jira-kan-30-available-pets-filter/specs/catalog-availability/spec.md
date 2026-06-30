# Catalog Availability Filter Spec Delta

## ADDED Requirements

### Requirement: Default search must exclude pending pets

Default catalog searches must return only pets with `status="available"`, excluding pets with `status="pending"`.

#### Scenario: Default search without status parameter

- Given: Pet catalog with mixed status pets including pet-103 (Nova) with status="pending"
- When: User searches with default parameters `search_pets()`
- Then: Only available pets are returned and pet-103 is excluded

#### Scenario: Species filter with default status

- Given: Pet catalog with available dog (Scout/pet-101) and pending dog (Nova/pet-103)
- When: User searches for dogs with default status `search_pets(species="dog")`
- Then: Only Scout (pet-101) is returned and Nova (pet-103) is excluded

## MODIFIED Requirements

### Requirement: Explicit pending search must still work

Operations teams must be able to explicitly request pending pets when investigating cases.

#### Scenario: Explicit pending pet search

- Given: Pet catalog with pending dog Nova (pet-103)
- When: Operations team explicitly requests pending pets `search_pets(species="dog", status="pending")`
- Then: Only Nova (pet-103) is returned
