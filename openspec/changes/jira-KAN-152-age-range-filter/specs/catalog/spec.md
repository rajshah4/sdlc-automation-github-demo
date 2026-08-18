# Catalog Age Filter Spec Delta

## ADDED Requirements

### Requirement: Customers can filter pets by minimum age

#### Scenario: Filter returns only pets at or above minimum age

- Given a catalog with pets of various ages
- When a customer searches with min_age_months=15
- Then only pets with age_months >= 15 are returned
- And pets below the minimum age are excluded

#### Scenario: Minimum age works with other filters

- Given a catalog with pets of various ages, species, and statuses
- When a customer searches with species="dog" and min_age_months=20
- Then only dogs with age_months >= 20 are returned
- And the default status="available" filter still applies

### Requirement: Customers can filter pets by maximum age

#### Scenario: Filter returns only pets at or below maximum age

- Given a catalog with pets of various ages
- When a customer searches with max_age_months=20
- Then only pets with age_months <= 20 are returned
- And pets above the maximum age are excluded

### Requirement: Customers can specify both minimum and maximum age

#### Scenario: Filter returns pets within age range

- Given a catalog with pets of various ages
- When a customer searches with min_age_months=10 and max_age_months=20
- Then only pets with 10 <= age_months <= 20 are returned
- And pets outside the range are excluded

### Requirement: Age filters validate input

#### Scenario: Negative minimum age is rejected

- Given a customer attempts to search
- When min_age_months is negative
- Then a ValueError is raised with a clear message

#### Scenario: Negative maximum age is rejected

- Given a customer attempts to search
- When max_age_months is negative
- Then a ValueError is raised with a clear message

#### Scenario: Inverted range is rejected

- Given a customer attempts to search
- When min_age_months > max_age_months
- Then a ValueError is raised indicating invalid range

### Requirement: Age filters are optional

#### Scenario: Search works without age filters

- Given existing search behavior
- When no age parameters are provided
- Then search works as before with no age filtering
- And all existing filters continue to work

## UNCHANGED Requirements

- Default status filter remains "available"
- Pending pets only appear when status="pending" is explicitly requested
- max_results validation (1-50) unchanged
- Species, tag, and name filtering unchanged
