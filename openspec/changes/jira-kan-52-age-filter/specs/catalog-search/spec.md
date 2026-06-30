# Catalog Search Spec Delta

## ADDED Requirements

### Requirement: Filter pets by minimum age

#### Scenario: Search with minimum age filter

- Given a catalog with pets of various ages
- When a user searches with `min_age_months=18`
- Then only pets with age >= 18 months are returned

#### Scenario: Reject negative minimum age

- Given a catalog search
- When a user provides `min_age_months=-1`
- Then a validation error is raised

### Requirement: Filter pets by maximum age

#### Scenario: Search with maximum age filter

- Given a catalog with pets of various ages
- When a user searches with `max_age_months=12`
- Then only pets with age <= 12 months are returned

#### Scenario: Reject negative maximum age

- Given a catalog search
- When a user provides `max_age_months=-1`
- Then a validation error is raised

### Requirement: Filter pets by age range

#### Scenario: Search with both minimum and maximum age

- Given a catalog with pets of various ages
- When a user searches with `min_age_months=10` and `max_age_months=20`
- Then only pets with age between 10 and 20 months (inclusive) are returned

#### Scenario: Reject inverted age range

- Given a catalog search
- When a user provides `min_age_months=20` and `max_age_months=10`
- Then a validation error is raised

### Requirement: Age filter combines with existing filters

#### Scenario: Filter by species and age range

- Given a catalog with pets of various species and ages
- When a user searches for dogs with `min_age_months=10` and `max_age_months=30`
- Then only dogs within the age range are returned

#### Scenario: Age filter respects availability status

- Given a catalog with available and pending pets
- When a user searches with age filters but no explicit status
- Then only available pets within the age range are returned (default behavior)
