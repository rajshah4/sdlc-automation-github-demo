# Catalog Age Filter Spec Delta

## ADDED Requirements

### Requirement: Search pets by minimum age

#### Scenario: Filter for pets at least 12 months old

- Given a catalog with pets of various ages
- When searching with `min_age_months=12`
- Then only pets with `age_months >= 12` are returned

#### Scenario: Filter for pets at least 18 months old

- Given a catalog with pets including Mochi (18 months), Scout (28 months), Pip (9 months), Nova (14 months)
- When searching with `min_age_months=18`
- Then results include only Mochi and Scout

### Requirement: Search pets by maximum age

#### Scenario: Filter for pets up to 15 months old

- Given a catalog with pets of various ages
- When searching with `max_age_months=15`
- Then only pets with `age_months <= 15` are returned

#### Scenario: Filter for young pets up to 10 months old

- Given a catalog with pets including Mochi (18 months), Scout (28 months), Pip (9 months), Nova (14 months)
- When searching with `max_age_months=10`
- Then results include only Pip

### Requirement: Search pets by age range

#### Scenario: Filter for pets between 10 and 20 months old

- Given a catalog with pets of various ages
- When searching with `min_age_months=10` and `max_age_months=20`
- Then only pets with `10 <= age_months <= 20` are returned

#### Scenario: Combine age filter with other filters

- Given a catalog with multiple species at different ages
- When searching for dogs with `min_age_months=10` and `max_age_months=20`
- Then only dogs within the age range are returned

### Requirement: Validate age filter inputs

#### Scenario: Reject negative minimum age

- Given any catalog state
- When searching with `min_age_months=-5`
- Then a ValueError is raised with message about valid age range

#### Scenario: Reject negative maximum age

- Given any catalog state
- When searching with `max_age_months=-1`
- Then a ValueError is raised with message about valid age range

#### Scenario: Reject inverted age range

- Given any catalog state
- When searching with `min_age_months=20` and `max_age_months=10`
- Then a ValueError is raised with message about min <= max

### Requirement: Age filter is optional

#### Scenario: Default search without age filter

- Given a catalog with pets of various ages
- When searching without age parameters
- Then all available pets are returned (existing behavior unchanged)
