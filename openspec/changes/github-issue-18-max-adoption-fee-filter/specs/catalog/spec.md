# Catalog Spec Delta

## ADDED Requirements

### Requirement: Filter pets by maximum adoption fee

#### Scenario: Adopter searches with max fee that includes some pets

- Given pets with adoption fees of 4500, 7500, 11000, and 12500 cents exist
- When adopter searches with max_fee_cents=8000
- Then only pets with adoption_fee_cents <= 8000 are returned (4500 and 7500)

#### Scenario: Adopter searches with max fee that excludes all pets

- Given pets with adoption fees starting at 4500 cents
- When adopter searches with max_fee_cents=1000
- Then no pets are returned

#### Scenario: Adopter searches without specifying max fee

- Given the catalog contains pets with various adoption fees
- When adopter searches without max_fee_cents parameter
- Then all pets matching other criteria are returned (no fee filtering)

#### Scenario: Adopter provides negative max fee

- Given the search accepts optional max_fee_cents parameter
- When adopter provides max_fee_cents=-100
- Then a ValueError is raised with message about non-negative values

### Requirement: Max fee filter combines with existing filters

#### Scenario: Max fee filter with species filter

- Given pets of multiple species with various adoption fees
- When adopter searches for species="cat" with max_fee_cents=10000
- Then only cats with adoption_fee_cents <= 10000 are returned
