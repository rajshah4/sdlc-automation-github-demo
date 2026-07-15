# Catalog Filter Spec Delta

## ADDED Requirements

### Requirement: Filter pets by maximum age

Adopters can optionally filter available pets by maximum age to find pets that fit their household.

#### Scenario: Return pets within age limit

- Given a catalog with pets of various ages
- When searching with `max_age_months=20`
- Then only pets aged 20 months or younger are returned
- And pets older than 20 months are excluded

#### Scenario: Maximum age filter is optional

- Given a catalog with pets of various ages
- When searching without specifying `max_age_months`
- Then all pets matching other criteria are returned
- And the default behavior is unchanged

#### Scenario: Reject negative age values

- Given a catalog search request
- When `max_age_months` is negative (e.g., `-5`)
- Then a ValueError is raised
- And the error message indicates invalid age

#### Scenario: Age filter preserves status filtering

- Given a catalog with available and pending pets
- When searching with `max_age_months=30` and default status
- Then only available pets within the age limit are returned
- And pending pets are still excluded by default

#### Scenario: Zero age is valid

- Given a catalog search request
- When `max_age_months=0`
- Then only pets aged 0 months are returned
- And no error is raised
