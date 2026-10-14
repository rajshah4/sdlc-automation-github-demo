# Catalog Availability Spec Delta

## MODIFIED Requirements

### Requirement: Default pet search returns only available pets

#### Scenario: Empty status string does not bypass availability filter

- Given a pet catalog with both available and pending pets
- When a search is performed with an empty status string
- Then only pets with status="available" are returned
- And pending pets are excluded from results

#### Scenario: Explicit pending search continues to work

- Given a pet catalog with both available and pending pets
- When a search is performed with status="pending"
- Then only pets with status="pending" are returned
- And available pets are excluded from results

#### Scenario: Default search excludes Nova

- Given Nova (pet-103) has status="pending"
- When a default species search for dogs is performed
- Then Scout (pet-101) is returned
- And Nova (pet-103) is not returned

## UNCHANGED Requirements

### Requirement: Explicit status searches work correctly

- Support and operations workflows can explicitly request status="pending"
- Tag-based and species-based filters continue to work as before
- Query string matching on pet names remains unchanged
