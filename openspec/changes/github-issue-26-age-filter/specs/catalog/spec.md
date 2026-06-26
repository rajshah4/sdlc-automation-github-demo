# Catalog Spec Delta

## ADDED Requirements

### Requirement: Age-range filtering in pet search

The catalog search shall accept optional minimum and maximum age parameters to filter pets by age range.

#### Scenario: Filter pets by minimum age

- Given a catalog with pets of various ages
- When a search is performed with `min_age=15`
- Then only pets with age_months >= 15 are returned

#### Scenario: Filter pets by maximum age

- Given a catalog with pets of various ages
- When a search is performed with `max_age=20`
- Then only pets with age_months <= 20 are returned

#### Scenario: Filter pets by age range

- Given a catalog with pets of various ages
- When a search is performed with `min_age=10` and `max_age=25`
- Then only pets with age_months between 10 and 25 (inclusive) are returned

#### Scenario: Filter pets by exact age

- Given a catalog with pets of various ages
- When a search is performed with `min_age=18` and `max_age=18`
- Then only pets with age_months exactly 18 are returned

#### Scenario: Reject negative minimum age

- Given a search request
- When `min_age` is negative
- Then a ValueError is raised

#### Scenario: Reject negative maximum age

- Given a search request
- When `max_age` is negative
- Then a ValueError is raised

#### Scenario: Reject inverted age range

- Given a search request
- When `min_age` is greater than `max_age`
- Then a ValueError is raised
