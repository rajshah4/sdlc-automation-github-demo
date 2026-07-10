# Catalog Filter Spec Delta

## ADDED Requirements

### Requirement: Status filter must always be enforced when status parameter is provided

#### Scenario: Empty status string should not bypass status filter

- Given a pet catalog with both available and pending pets
- When search_pets is called with status="" (empty string)
- Then the function should treat empty string as requiring exact match, returning no results OR default to "available" behavior

#### Scenario: Default search returns only available pets

- Given a pet catalog containing pets with various status values
- When search_pets is called with default parameters (status="available")
- Then only pets with status="available" are returned
- And pets with status="pending" are excluded

#### Scenario: Explicit status filter works correctly

- Given a pet catalog with available and pending pets
- When search_pets is called with status="pending"
- Then only pets with status="pending" are returned
- And pets with status="available" are excluded

## MODIFIED Behavior

### Previous Behavior

The status filter used a truthy check (`if normalized_status and ...`) which caused empty strings to bypass the filter entirely. This allowed all pets, including pending ones, to be returned when status="" was passed.

### New Behavior

The status filter always applies when a status parameter value is present. Empty strings are normalized and treated as literal values, preventing the bypass of status filtering.
