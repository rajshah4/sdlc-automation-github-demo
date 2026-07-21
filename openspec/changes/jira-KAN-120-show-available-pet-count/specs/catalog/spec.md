# Petstore Catalog Count Spec Delta

## ADDED Requirements

### Requirement: Catalog displays count of available pets in current results

The catalog MUST display the number of available pets that match the current search and filter criteria.

#### Scenario: Default catalog shows count of all available pets

- Given the catalog has 3 available pets and 1 pending pet
- When the catalog loads with default filters
- Then the count displays "3 pets available"

#### Scenario: Count updates with species filter

- Given the catalog has 2 available dogs
- When the user filters by species "dog"
- Then the count displays "1 pet available" (Scout only, Nova is pending)

#### Scenario: Count updates with name query

- Given the user searches for "Mochi"
- When the search is executed
- Then the count displays "1 pet available"

#### Scenario: Count excludes pending pets

- Given Nova has status "pending"
- When counting available pets with species "dog"
- Then Nova is not included in the count
- And the count shows only Scout

#### Scenario: Count reflects combined filters

- Given the user filters by species "cat" and tag "indoor"
- When the search is executed
- Then the count displays "1 pet available" (Mochi)

#### Scenario: Count shows zero when no matches

- Given the user searches for a non-existent pet name
- When the search is executed
- Then the count displays "0 pets available"
