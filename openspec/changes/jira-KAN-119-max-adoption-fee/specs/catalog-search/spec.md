# Catalog Search Spec Delta

## ADDED Requirements

### Requirement: Support maximum adoption fee filtering

The catalog search must support an optional maximum adoption fee parameter so adopters can find pets within their budget.

#### Scenario: Filter pets by maximum fee (matching)

- Given a catalog with pets having various adoption fees
- When a user searches with `max_adoption_fee_cents=10000` (i.e., $100)
- Then only pets with `adoption_fee_cents <= 10000` are returned

#### Scenario: Filter pets by maximum fee (exclusion)

- Given a catalog with pets having various adoption fees
- When a user searches with `max_adoption_fee_cents=8000` (i.e., $80)
- Then pets with `adoption_fee_cents > 8000` are excluded from results

#### Scenario: Reject invalid negative maximum fees

- Given the catalog search function
- When a user provides a negative `max_adoption_fee_cents` value
- Then a ValueError is raised with a message indicating invalid fee

#### Scenario: Maximum fee filter is optional

- Given the catalog search function
- When a user searches without specifying `max_adoption_fee_cents`
- Then all available pets are returned (no fee filtering applied)

### Requirement: UI exposes maximum adoption fee filter

The catalog UI must provide an input field for users to specify their maximum adoption fee budget.

#### Scenario: UI displays maximum fee input

- Given the petstore catalog UI
- When a user views the search form
- Then a "Max Adoption Fee" input field is visible

#### Scenario: UI filters pets by maximum fee

- Given the petstore catalog UI with pets displayed
- When a user enters a maximum fee value and searches
- Then only pets at or below that fee are displayed
