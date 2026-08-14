# Catalog Filter Spec Delta

## ADDED Requirements

### Requirement: Filter pets by minimum age

#### Scenario: Search returns only pets at or above minimum age

- Given pets with ages 9, 14, 18, and 28 months
- When searching with `min_age_months=15`
- Then only pets aged 18 and 28 months are returned

#### Scenario: Pets at exact minimum age boundary are included

- Given a pet aged exactly 18 months
- When searching with `min_age_months=18`
- Then the pet is included in results

### Requirement: Filter pets by maximum age

#### Scenario: Search returns only pets at or below maximum age

- Given pets with ages 9, 14, 18, and 28 months
- When searching with `max_age_months=15`
- Then only pets aged 9 and 14 months are returned

#### Scenario: Pets at exact maximum age boundary are included

- Given a pet aged exactly 18 months
- When searching with `max_age_months=18`
- Then the pet is included in results

### Requirement: Filter pets by age range

#### Scenario: Search returns only pets within the specified range

- Given pets with ages 9, 14, 18, and 28 months
- When searching with `min_age_months=10` and `max_age_months=20`
- Then only pets aged 14 and 18 months are returned

### Requirement: Validate age filter parameters

#### Scenario: Reject negative minimum age

- Given a search request with `min_age_months=-1`
- When the search is executed
- Then a `ValueError` is raised with message "min_age_months must be >= 0"

#### Scenario: Reject negative maximum age

- Given a search request with `max_age_months=-1`
- When the search is executed
- Then a `ValueError` is raised with message "max_age_months must be >= 0"

#### Scenario: Reject inverted age range

- Given a search request with `min_age_months=20` and `max_age_months=10`
- When the search is executed
- Then a `ValueError` is raised with message "min_age_months must be <= max_age_months"

### Requirement: Age filters are optional

#### Scenario: No age filter when parameters are None

- Given all available pets
- When searching with `min_age_months=None` and `max_age_months=None`
- Then all available pets are returned (no age filtering)
