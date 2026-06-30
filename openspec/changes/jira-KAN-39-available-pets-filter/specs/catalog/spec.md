# Catalog Availability Spec Delta

## ADDED Requirements

### Requirement: Default catalog search must filter to available pets only

#### Scenario: Default search with no status parameter

- Given the petstore has pets with mixed statuses (available, pending)
- When a client calls `search_pets()` with default parameters
- Then only pets with `status="available"` are returned

#### Scenario: Default search with empty status string

- Given the petstore has pets with mixed statuses
- When a client calls `search_pets(status="")` with an empty status string
- Then only pets with `status="available"` are returned

#### Scenario: Nova (pet-103) does not appear in default available results

- Given Nova is pet-103 with `status="pending"`
- When a client calls `search_pets()` with default parameters
- Then Nova does not appear in the results

#### Scenario: Explicit pending search still works

- Given Nova is pet-103 with `status="pending"`
- When a client calls `search_pets(status="pending")`
- Then Nova appears in the results

### Requirement: Empty status parameter defaults to available filter

#### Scenario: Empty string status parameter

- Given a catalog search is performed
- When `status=""` is provided explicitly
- Then the search treats it as `status="available"`

## UNCHANGED Requirements

### Requirement: Explicit status search works for any valid status

#### Scenario: Search for pending pets

- Given the petstore has pending pets
- When a client calls `search_pets(status="pending")`
- Then only pets with `status="pending"` are returned
