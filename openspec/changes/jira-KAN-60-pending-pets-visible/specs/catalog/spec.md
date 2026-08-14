# Catalog Availability Spec Delta

## ADDED Requirements

### Requirement: Default pet search returns only available pets

Default catalog search (with no status parameter) must exclude all pending pets from results.

#### Scenario: Default search with no filters

- Given the catalog contains both available and pending pets
- When a search is performed with no status parameter
- Then only pets with status="available" are returned
- And pets with status="pending" are excluded

#### Scenario: Nova (pet-103) excluded from default search

- Given Nova (pet-103) has status="pending"
- When a default search is performed
- Then Nova must not appear in the results
- And the PENDING_PET_VISIBLE error must not occur

#### Scenario: All available pets included by default

- Given pets Mochi (pet-100), Scout (pet-101), and Pip (pet-102) have status="available"
- When a default search is performed with no filters
- Then all three available pets are included in the results

### Requirement: Explicit pending searches still work

Support and operations teams must be able to explicitly search for pending pets.

#### Scenario: Explicit pending pet search

- Given Nova (pet-103) has status="pending"
- When a search is performed with status="pending"
- Then Nova appears in the results
- And no available pets appear in the results

## Test Coverage Requirements

- Test default search behavior without arguments
- Test explicit exclusion of known pending pet (Nova/pet-103)
- Test inclusion of all available pets
- Preserve existing test for explicit pending pet searches
