# Catalog Availability Spec Delta

## ADDED Requirements

### Requirement: Default catalog search excludes pending pets

The default pet catalog search must return only pets with `status="available"`, even when the status parameter is explicitly set to an empty string or omitted.

#### Scenario: Empty status parameter excludes pending pets

- Given the catalog contains pet-103 (Nova) with status="pending"
- And the catalog contains pet-101 (Scout) with status="available"
- When a user searches with `search_pets(species="dog", status="")`
- Then the results must include only Scout
- And the results must not include Nova

#### Scenario: Default status parameter excludes pending pets

- Given the catalog contains pet-103 (Nova) with status="pending"
- And the catalog contains pet-101 (Scout) with status="available"
- When a user searches with `search_pets(species="dog")`
- Then the results must include only Scout
- And the results must not include Nova

### Requirement: Explicit pending search continues to work

Support and operations workflows can explicitly request pending pets.

#### Scenario: Explicit pending status returns pending pets

- Given the catalog contains pet-103 (Nova) with status="pending"
- When a user searches with `search_pets(species="dog", status="pending")`
- Then the results must include Nova
- And the results must not include available dogs

## UNCHANGED Requirements

### Requirement: Species and tag filtering

Existing species and tag filtering behavior remains unchanged.

### Requirement: Max results validation

Existing max_results validation (1-50 range) remains unchanged.
