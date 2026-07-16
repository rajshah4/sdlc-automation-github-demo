# Catalog Availability Spec Delta

## ADDED Requirements

### Requirement: Empty status parameter must default to available-only search

When a search request provides an empty string for the status parameter, the catalog must treat it as `status="available"` rather than disabling the status filter.

#### Scenario: Empty status string excludes pending pets

- Given Nova (pet-103) has status="pending"
- When search_pets(status="") is called
- Then Nova must not appear in the results
- And only pets with status="available" are returned

#### Scenario: Explicit pending status still works

- Given Nova (pet-103) has status="pending"
- When search_pets(status="pending") is called
- Then Nova must appear in the results

#### Scenario: Default search excludes pending pets

- Given Nova (pet-103) has status="pending"
- When search_pets() is called without status parameter
- Then Nova must not appear in the results
- And only pets with status="available" are returned

## UNCHANGED Requirements

### Requirement: Explicit status override works as specified

When a caller explicitly requests a specific status (e.g., "pending"), the catalog must return only pets matching that status.

#### Scenario: Support can search for pending pets

- Given support workflow needs to review pending cases
- When search_pets(status="pending") is called
- Then only pending pets are returned
- And available pets are excluded
