# Catalog Sorting Spec Delta

## ADDED Requirements

### Requirement: Sort available pets by adoption fee

The catalog search function shall support sorting available pets by adoption fee in ascending order (lowest to highest).

#### Scenario: Sort available pets by adoption fee

- Given the catalog contains multiple available pets with different adoption fees
- When a user searches with `sort_by="adoption_fee"`
- Then results are returned in ascending order by adoption fee (lowest first)

#### Scenario: Default behavior unchanged when sorting not requested

- Given the catalog contains pets
- When a user searches without specifying `sort_by`
- Then results are returned in the original order (not sorted)

#### Scenario: Sorting works with species filter

- Given the catalog contains multiple pets of the same species with different adoption fees
- When a user searches with `species="dog"` and `sort_by="adoption_fee"`
- Then only dogs are returned, sorted by adoption fee in ascending order

#### Scenario: Sorting works with tag filter

- Given the catalog contains multiple pets with the same tag and different adoption fees
- When a user searches with `tag="indoor"` and `sort_by="adoption_fee"`
- Then only pets with the "indoor" tag are returned, sorted by adoption fee in ascending order
