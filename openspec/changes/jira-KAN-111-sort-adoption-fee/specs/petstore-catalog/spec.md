# Petstore Catalog Spec Delta

## ADDED Requirements

### Requirement: Sort available pets by adoption fee in ascending order

#### Scenario: Sort results by adoption fee ascending

- Given multiple available pets with different adoption fees
- When searching with `sort_by="fee_asc"`
- Then results are ordered by `adoption_fee_cents` from lowest to highest

#### Scenario: Sorting preserves status filter

- Given pets with status "available" and "pending"
- When searching with `status="available"` and `sort_by="fee_asc"`
- Then only available pets are returned, sorted by fee ascending

### Requirement: Sort available pets by adoption fee in descending order

#### Scenario: Sort results by adoption fee descending

- Given multiple available pets with different adoption fees
- When searching with `sort_by="fee_desc"`
- Then results are ordered by `adoption_fee_cents` from highest to lowest

### Requirement: Default catalog behavior unchanged

#### Scenario: No sorting when sort_by not provided

- Given multiple available pets
- When searching without `sort_by` parameter
- Then results are returned in default order (no sorting applied)

### Requirement: Invalid sort values rejected

#### Scenario: Invalid sort_by value raises error

- Given a search request
- When `sort_by` is set to an invalid value (e.g., "name", "invalid")
- Then a `ValueError` is raised with a descriptive message
