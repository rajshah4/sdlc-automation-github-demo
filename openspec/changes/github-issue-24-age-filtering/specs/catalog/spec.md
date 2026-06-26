# Catalog Search Spec Delta

## ADDED Requirements

### Requirement: Filter pets by minimum age

#### Scenario: Search returns only pets meeting minimum age

- Given a catalog with pets of varying ages
- When a user searches with `min_age_months=12`
- Then only pets with `age_months >= 12` are returned

#### Scenario: Negative minimum age is rejected

- Given a user attempts to search
- When `min_age_months` is negative
- Then a `ValueError` is raised

### Requirement: Filter pets by maximum age

#### Scenario: Search returns only pets meeting maximum age

- Given a catalog with pets of varying ages
- When a user searches with `max_age_months=20`
- Then only pets with `age_months <= 20` are returned

#### Scenario: Negative maximum age is rejected

- Given a user attempts to search
- When `max_age_months` is negative
- Then a `ValueError` is raised

### Requirement: Filter pets by age range

#### Scenario: Search returns pets within specified range

- Given a catalog with pets of varying ages
- When a user searches with `min_age_months=10` and `max_age_months=20`
- Then only pets with `10 <= age_months <= 20` are returned

#### Scenario: Inverted range is rejected

- Given a user attempts to search
- When `min_age_months > max_age_months`
- Then a `ValueError` is raised

### Requirement: Age filtering preserves existing filter behavior

#### Scenario: Age filter works with status filter

- Given the default status filter is "available"
- When a user searches with age filters
- Then only available pets within the age range are returned

#### Scenario: Age filter works with species filter

- Given a user searches for dogs with age filter
- When `species="dog"` and `min_age_months=20`
- Then only dogs with `age_months >= 20` are returned
