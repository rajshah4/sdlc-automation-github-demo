# Catalog Spec Delta

## ADDED Requirements

### Requirement: Filter pets by minimum age

Customers can specify a minimum age threshold to exclude pets younger than the specified age.

#### Scenario: Find pets at least 12 months old

- Given a catalog containing pets of various ages
- When a customer searches with `min_age_months=12`
- Then only pets with age_months >= 12 are returned

#### Scenario: Minimum age of zero is treated as no filter

- Given a catalog containing pets of various ages
- When a customer searches with `min_age_months=0`
- Then all pets matching other criteria are returned (no age filtering applied)

### Requirement: Filter pets by maximum age

Customers can specify a maximum age threshold to exclude pets older than the specified age.

#### Scenario: Find pets no older than 18 months

- Given a catalog containing pets of various ages
- When a customer searches with `max_age_months=18`
- Then only pets with age_months <= 18 are returned

#### Scenario: Maximum age of zero excludes all pets

- Given a catalog containing pets of various ages
- When a customer searches with `max_age_months=0`
- Then no pets are returned (only newborns with age_months=0 would match)

### Requirement: Filter pets by age range

Customers can specify both minimum and maximum age to find pets within a specific age window.

#### Scenario: Find young adult pets (12-24 months)

- Given a catalog containing pets of various ages
- When a customer searches with `min_age_months=12` and `max_age_months=24`
- Then only pets with 12 <= age_months <= 24 are returned

### Requirement: Validate age filter parameters

The system rejects invalid age filter values to prevent errors and unexpected results.

#### Scenario: Reject negative minimum age

- Given a search request with `min_age_months=-1`
- When the search is executed
- Then a ValueError is raised with message about negative age

#### Scenario: Reject negative maximum age

- Given a search request with `max_age_months=-5`
- When the search is executed
- Then a ValueError is raised with message about negative age

#### Scenario: Reject inverted age range

- Given a search request with `min_age_months=24` and `max_age_months=12`
- When the search is executed
- Then a ValueError is raised with message about inverted range

### Requirement: Age filtering works with existing filters

Age filters combine with species, status, and tag filters to narrow results.

#### Scenario: Filter by species and age range

- Given a catalog with dogs of various ages
- When a customer searches for `species="dog"` with `min_age_months=10` and `max_age_months=20`
- Then only dogs within the age range are returned

#### Scenario: Age filtering respects default status=available

- Given a catalog with available and pending pets of various ages
- When a customer searches with `min_age_months=12`
- Then only available pets at least 12 months old are returned (pending pets excluded by default)
