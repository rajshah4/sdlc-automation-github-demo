# Pet Catalog Spec Delta

## ADDED Requirements

### Requirement: Filter pets by minimum age

Users can specify a minimum age in months to exclude pets younger than the threshold.

#### Scenario: Filter pets older than 12 months

- Given the pet catalog contains pets with various ages
- When a user searches with `min_age_months=12`
- Then only pets with age_months >= 12 are returned

#### Scenario: Minimum age filter composes with species filter

- Given the pet catalog contains dogs of various ages
- When a user searches with `species="dog"` and `min_age_months=20`
- Then only dogs with age_months >= 20 are returned

### Requirement: Filter pets by maximum age

Users can specify a maximum age in months to exclude pets older than the threshold.

#### Scenario: Filter pets younger than 18 months

- Given the pet catalog contains pets with various ages
- When a user searches with `max_age_months=18`
- Then only pets with age_months <= 18 are returned

### Requirement: Filter pets by age range

Users can specify both minimum and maximum age to find pets within a specific age range.

#### Scenario: Filter pets between 10 and 20 months old

- Given the pet catalog contains pets with various ages
- When a user searches with `min_age_months=10` and `max_age_months=20`
- Then only pets with 10 <= age_months <= 20 are returned

### Requirement: Validate age filter parameters

The system must reject invalid age filter values to prevent incorrect search results.

#### Scenario: Reject negative minimum age

- Given a user attempts to search pets
- When the search includes `min_age_months=-1`
- Then the system raises a ValueError indicating age must be non-negative

#### Scenario: Reject negative maximum age

- Given a user attempts to search pets
- When the search includes `max_age_months=-5`
- Then the system raises a ValueError indicating age must be non-negative

#### Scenario: Reject inverted age range

- Given a user attempts to search pets
- When the search includes `min_age_months=24` and `max_age_months=12`
- Then the system raises a ValueError indicating min_age cannot exceed max_age

### Requirement: Age filters are optional

Age filtering should not be required; existing searches without age parameters continue to work.

#### Scenario: Search without age filters returns all matching pets

- Given the pet catalog contains pets with various ages
- When a user searches without age parameters
- Then all pets matching other criteria are returned regardless of age
