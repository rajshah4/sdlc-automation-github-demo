# Catalog Age Filter Spec Delta

## ADDED Requirements

### Requirement: Filter pets by minimum age

#### Scenario: Search returns only pets at or above minimum age

- Given a catalog containing pets of various ages
- When a user searches with `min_age_months=13`
- Then only pets with `age_months >= 13` appear in results

#### Scenario: Negative minimum age is rejected

- Given the search API
- When a user calls `search_pets(min_age_months=-1)`
- Then a `ValueError` is raised with message "min_age_months must be >= 0"

### Requirement: Filter pets by maximum age

#### Scenario: Search returns only pets at or below maximum age

- Given a catalog containing pets of various ages
- When a user searches with `max_age_months=12`
- Then only pets with `age_months <= 12` appear in results

#### Scenario: Negative maximum age is rejected

- Given the search API
- When a user calls `search_pets(max_age_months=-1)`
- Then a `ValueError` is raised with message "max_age_months must be >= 0"

### Requirement: Filter pets by age range

#### Scenario: Search returns only pets within the specified age range

- Given a catalog containing pets of various ages
- When a user searches with `min_age_months=13` and `max_age_months=84`
- Then only pets with `13 <= age_months <= 84` appear in results

#### Scenario: Inverted age range is rejected

- Given the search API
- When a user calls `search_pets(min_age_months=84, max_age_months=13)`
- Then a `ValueError` is raised with message "min_age_months must be <= max_age_months"

### Requirement: Age filter is optional

#### Scenario: No age filter returns pets of all ages

- Given a catalog containing pets of various ages
- When a user searches without age parameters
- Then all available pets appear in results regardless of age

#### Scenario: Omitting minimum age allows all ages up to maximum

- Given a catalog containing pets of various ages
- When a user searches with `max_age_months=12` only
- Then pets with `age_months <= 12` appear in results

#### Scenario: Omitting maximum age allows all ages from minimum

- Given a catalog containing pets of various ages
- When a user searches with `min_age_months=85` only
- Then pets with `age_months >= 85` appear in results
