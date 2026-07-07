# Catalog Spec Delta

## ADDED Requirements

### Requirement: Search pets by minimum age

When an adopter specifies a minimum age, the catalog must return only pets at or above that age threshold.

#### Scenario: Filter by minimum age

- Given the catalog contains pets of various ages
- When the adopter searches with `min_age_months=15`
- Then only pets with `age_months >= 15` are returned
- And younger pets are excluded from results

### Requirement: Search pets by maximum age

When an adopter specifies a maximum age, the catalog must return only pets at or below that age threshold.

#### Scenario: Filter by maximum age

- Given the catalog contains pets of various ages
- When the adopter searches with `max_age_months=20`
- Then only pets with `age_months <= 20` are returned
- And older pets are excluded from results

### Requirement: Search pets by age range

When an adopter specifies both minimum and maximum age, the catalog must return only pets within that inclusive range.

#### Scenario: Filter by age range

- Given the catalog contains pets of various ages
- When the adopter searches with `min_age_months=10` and `max_age_months=20`
- Then only pets with `10 <= age_months <= 20` are returned
- And pets outside this range are excluded

### Requirement: Age range validation

The catalog must reject invalid age parameters to prevent user errors.

#### Scenario: Reject negative minimum age

- Given an adopter attempts to search with `min_age_months=-1`
- When the search executes
- Then a ValueError is raised with a message indicating ages must be non-negative

#### Scenario: Reject negative maximum age

- Given an adopter attempts to search with `max_age_months=-5`
- When the search executes
- Then a ValueError is raised with a message indicating ages must be non-negative

#### Scenario: Reject inverted age range

- Given an adopter attempts to search with `min_age_months=30` and `max_age_months=10`
- When the search executes
- Then a ValueError is raised with a message indicating min cannot exceed max

### Requirement: Optional age filtering

Age filters must be optional to maintain backward compatibility with existing search behavior.

#### Scenario: No age filter returns all status-matching pets

- Given the adopter does not specify any age filters
- When the search executes with default parameters
- Then all pets matching the status filter are returned
- And no age filtering is applied

#### Scenario: Single boundary filter is valid

- Given the adopter specifies only `min_age_months` or only `max_age_months`
- When the search executes
- Then the single boundary is applied correctly
- And no error is raised
