# Catalog Spec Delta

## ADDED Requirements

### Requirement: Filter pets by minimum age

#### Scenario: Search for pets at least 12 months old

- Given a catalog with pets of varying ages
- When an adopter searches with `min_age_months=12`
- Then only pets with `age_months >= 12` are returned

#### Scenario: Search for pets at least 0 months old

- Given a catalog with pets of varying ages
- When an adopter searches with `min_age_months=0`
- Then all pets matching other criteria are returned (0 is the minimum valid age)

### Requirement: Filter pets by maximum age

#### Scenario: Search for pets up to 18 months old

- Given a catalog with pets of varying ages
- When an adopter searches with `max_age_months=18`
- Then only pets with `age_months <= 18` are returned

### Requirement: Filter pets by age range

#### Scenario: Search for pets between 10 and 20 months old

- Given a catalog with pets of varying ages
- When an adopter searches with `min_age_months=10` and `max_age_months=20`
- Then only pets with `10 <= age_months <= 20` are returned

### Requirement: Validate age range parameters

#### Scenario: Reject negative minimum age

- Given the pet search API
- When an adopter provides `min_age_months=-1`
- Then a `ValueError` is raised with message "age values must be non-negative"

#### Scenario: Reject negative maximum age

- Given the pet search API
- When an adopter provides `max_age_months=-5`
- Then a `ValueError` is raised with message "age values must be non-negative"

#### Scenario: Reject inverted age range

- Given the pet search API
- When an adopter provides `min_age_months=24` and `max_age_months=12`
- Then a `ValueError` is raised with message "min_age_months cannot be greater than max_age_months"

### Requirement: Preserve default search behavior

#### Scenario: Age filtering works with status filtering

- Given a catalog with available and pending pets of varying ages
- When an adopter searches with `min_age_months=10` and default `status="available"`
- Then only available pets with `age_months >= 10` are returned (pending pets remain excluded)
