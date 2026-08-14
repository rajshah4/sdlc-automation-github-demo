# Pet Search Spec Delta

## ADDED Requirements

### Requirement: Pet search supports minimum age filtering

Adopters can specify a minimum age in months to exclude younger pets from search results.

#### Scenario: Search with minimum age returns only older pets

- Given the catalog contains pets with ages 9, 14, 18, and 28 months
- When a user searches with min_age_months=15
- Then only pets aged 18 and 28 months are returned

#### Scenario: Search with minimum age zero has no effect

- Given the catalog contains available pets
- When a user searches with min_age_months=0
- Then all available pets are returned (same as default)

### Requirement: Pet search supports maximum age filtering

Adopters can specify a maximum age in months to exclude older pets from search results.

#### Scenario: Search with maximum age returns only younger pets

- Given the catalog contains pets with ages 9, 14, 18, and 28 months
- When a user searches with max_age_months=15
- Then only pets aged 9 and 14 months are returned

### Requirement: Pet search supports age range filtering

Adopters can specify both minimum and maximum age to find pets within an age range.

#### Scenario: Search with age range returns pets within range

- Given the catalog contains pets with ages 9, 14, 18, and 28 months
- When a user searches with min_age_months=10 and max_age_months=20
- Then only pets aged 14 and 18 months are returned

### Requirement: Pet search validates age filter inputs

Invalid age filter inputs are rejected with clear error messages.

#### Scenario: Negative minimum age is rejected

- Given a user attempts to search
- When min_age_months is negative
- Then a ValueError is raised with message about valid age values

#### Scenario: Negative maximum age is rejected

- Given a user attempts to search
- When max_age_months is negative
- Then a ValueError is raised with message about valid age values

#### Scenario: Inverted age range is rejected

- Given a user attempts to search
- When min_age_months > max_age_months
- Then a ValueError is raised with message about valid age range

### Requirement: Age filtering preserves existing search behavior

Age filters work correctly in combination with existing filters.

#### Scenario: Age filter combines with status filter

- Given the catalog contains available and pending pets of various ages
- When a user searches with status="available" and min_age_months=15
- Then only available pets aged 15 months or older are returned
- And pending pets are excluded regardless of age

#### Scenario: Age filter combines with species filter

- Given the catalog contains dogs and cats of various ages
- When a user searches with species="dog" and max_age_months=20
- Then only dogs aged 20 months or younger are returned
- And cats are excluded regardless of age
