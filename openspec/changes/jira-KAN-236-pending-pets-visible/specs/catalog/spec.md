# Catalog Spec Delta

## ADDED Requirements

### Requirement: Default pet search excludes pending pets

Default catalog searches must return only pets with status="available". Pending pets must never appear in results unless explicitly requested.

#### Scenario: Default search excludes pending pets

- Given pets exist with both "available" and "pending" status
- When a caller searches without specifying status
- Then only pets with status="available" are returned
- And pets with status="pending" are excluded

#### Scenario: Species search excludes pending pets

- Given multiple dogs exist, some available and some pending
- When a caller searches for species="dog" without specifying status
- Then only available dogs are returned
- And pending dogs like Nova (pet-103) are excluded

#### Scenario: Empty status parameter excludes all pets

- Given the search function receives an empty string for status
- When the search is executed
- Then no pets are returned
- And the status filter is enforced (not bypassed)

### Requirement: Explicit pending searches continue working

Support and operations workflows that explicitly request pending pets must continue to work.

#### Scenario: Explicit pending search returns pending pets

- Given a caller explicitly requests status="pending"
- When the search is executed
- Then only pending pets are returned
- And available pets are excluded
