# Catalog Age Filtering Spec Delta

## ADDED Requirements

### Requirement: Search pets by minimum age

#### Scenario: Filter pets older than minimum age
- Given a catalog with pets of various ages
- When searching with `min_age_months=15`
- Then only pets with age >= 15 months are returned

#### Scenario: Minimum age at boundary
- Given a catalog with pets at exactly 15 months
- When searching with `min_age_months=15`
- Then pets with exactly 15 months are included

### Requirement: Search pets by maximum age

#### Scenario: Filter pets younger than maximum age
- Given a catalog with pets of various ages
- When searching with `max_age_months=20`
- Then only pets with age <= 20 months are returned

#### Scenario: Maximum age at boundary
- Given a catalog with pets at exactly 20 months
- When searching with `max_age_months=20`
- Then pets with exactly 20 months are included

### Requirement: Search pets by age range

#### Scenario: Filter pets within age range
- Given a catalog with pets of various ages
- When searching with `min_age_months=10` and `max_age_months=20`
- Then only pets with age between 10 and 20 months (inclusive) are returned

#### Scenario: Combine age filter with other filters
- Given a catalog with pets of various species and ages
- When searching with `species="dog"` and `min_age_months=15`
- Then only dogs with age >= 15 months are returned

### Requirement: Validate age parameters

#### Scenario: Reject negative minimum age
- Given any catalog state
- When searching with `min_age_months=-1`
- Then a ValueError is raised with message about invalid age

#### Scenario: Reject negative maximum age
- Given any catalog state
- When searching with `max_age_months=-1`
- Then a ValueError is raised with message about invalid age

#### Scenario: Reject inverted age range
- Given any catalog state
- When searching with `min_age_months=20` and `max_age_months=10`
- Then a ValueError is raised with message about invalid range

### Requirement: Preserve existing behavior

#### Scenario: Default search excludes pending pets
- Given a catalog with available and pending pets
- When searching with age filters but no explicit status
- Then only available pets matching the age criteria are returned

#### Scenario: Age filter is optional
- Given any catalog state
- When searching without age parameters
- Then all pets matching other criteria are returned (existing behavior)
