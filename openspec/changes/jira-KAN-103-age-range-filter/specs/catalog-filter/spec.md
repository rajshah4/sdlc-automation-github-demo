# Catalog Filter Spec Delta

## ADDED Requirements

### Requirement: Filter pets by minimum age

#### Scenario: Search returns only pets at or above minimum age

- Given a catalog with pets of various ages
- When a customer searches with `min_age_months=15`
- Then only pets with age >= 15 months are returned

#### Scenario: Minimum age filter is optional

- Given a catalog with pets of various ages
- When a customer searches without `min_age_months`
- Then pets of all ages are included in results

### Requirement: Filter pets by maximum age

#### Scenario: Search returns only pets at or below maximum age

- Given a catalog with pets of various ages
- When a customer searches with `max_age_months=20`
- Then only pets with age <= 20 months are returned

#### Scenario: Maximum age filter is optional

- Given a catalog with pets of various ages
- When a customer searches without `max_age_months`
- Then pets of all ages are included in results

### Requirement: Filter pets by age range

#### Scenario: Search returns pets within specified age range

- Given a catalog with pets of various ages
- When a customer searches with `min_age_months=10` and `max_age_months=20`
- Then only pets with age between 10 and 20 months (inclusive) are returned

#### Scenario: Age range includes boundary values

- Given a pet with age exactly 15 months
- When a customer searches with `min_age_months=15` and `max_age_months=15`
- Then the pet is included in results

### Requirement: Validate age range parameters

#### Scenario: Reject negative minimum age

- Given a customer attempts to search
- When `min_age_months` is negative
- Then the system raises a ValueError

#### Scenario: Reject negative maximum age

- Given a customer attempts to search
- When `max_age_months` is negative
- Then the system raises a ValueError

#### Scenario: Reject inverted age range

- Given a customer attempts to search
- When `min_age_months` is greater than `max_age_months`
- Then the system raises a ValueError
