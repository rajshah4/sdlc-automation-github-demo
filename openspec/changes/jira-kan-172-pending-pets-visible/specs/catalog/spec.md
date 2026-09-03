# Catalog Spec Delta

## ADDED Requirements

### Requirement: Default catalog search excludes pending pets

The default pet catalog search must return only pets with status "available". Pending pets should only be visible when explicitly requested via `status="pending"`.

#### Scenario: Default search with no status parameter

- Given the catalog contains both available and pending pets
- When a customer searches with default parameters
- Then only available pets are returned
- And pending pets are excluded from results

#### Scenario: Search with empty status string

- Given the catalog contains both available and pending pets
- When a customer searches with `status=""`
- Then only available pets are returned
- And pending pets are excluded from results

#### Scenario: Search with whitespace-only status string

- Given the catalog contains both available and pending pets
- When a customer searches with `status="  "`
- Then only available pets are returned
- And pending pets are excluded from results

#### Scenario: Explicit pending pet search

- Given the catalog contains both available and pending pets
- When support staff explicitly searches with `status="pending"`
- Then only pending pets are returned
- And available pets are excluded from results

## MODIFIED Requirements

### Requirement: Status filtering behavior must be consistent

Previously, the status filter could be bypassed by passing empty or whitespace-only strings. This behavior is now fixed to ensure consistent filtering.

#### Scenario: Status filter cannot be bypassed

- Given the catalog contains both available and pending pets
- When any status value that is empty or whitespace-only is passed
- Then the filter treats it as "available"
- And pending pets are never returned in default searches
