# Pet Search Spec Delta

## ADDED Requirements

### Requirement: Search pets by minimum age

#### Scenario: Find pets older than or equal to minimum age

- Given a catalog with pets of varying ages
- When searching with `min_age_months=15`
- Then only pets with age_months >= 15 are returned

#### Scenario: Reject negative minimum age

- Given a catalog search request
- When `min_age_months` is negative
- Then the search raises ValueError

### Requirement: Search pets by maximum age

#### Scenario: Find pets younger than or equal to maximum age

- Given a catalog with pets of varying ages
- When searching with `max_age_months=20`
- Then only pets with age_months <= 20 are returned

#### Scenario: Reject negative maximum age

- Given a catalog search request
- When `max_age_months` is negative
- Then the search raises ValueError

### Requirement: Search pets by age range

#### Scenario: Find pets within age range

- Given a catalog with pets of varying ages
- When searching with `min_age_months=10` and `max_age_months=20`
- Then only pets with 10 <= age_months <= 20 are returned

#### Scenario: Reject inverted age range

- Given a catalog search request
- When `min_age_months` > `max_age_months`
- Then the search raises ValueError

### Requirement: Age filtering preserves other filters

#### Scenario: Age range combined with status filter

- Given a catalog with available and pending pets
- When searching with `min_age_months=10` and default status="available"
- Then only available pets within the age range are returned
- And pending pets are excluded regardless of age
