# Catalog Availability Filter Spec Delta

## ADDED Requirements

### Requirement: Default search excludes non-available pets

The default pet search returns only pets with `status="available"`.

#### Scenario: Customer searches without specifying status

- Given the catalog contains pets with various statuses (available, pending)
- When a customer searches for pets without specifying a status parameter
- Then only pets with `status="available"` are returned
- And pending pets like Nova (pet-103) are excluded from results

### Requirement: Empty status parameter treated as available-only

When the status parameter is an empty string or contains only whitespace, the search treats it as a request for available pets only.

#### Scenario: Search with empty status string

- Given the catalog contains pet-101 (Scout, available) and pet-103 (Nova, pending)
- When a search executes with `status=""`
- Then only available pets are returned
- And pending pets are excluded from results

#### Scenario: Search with whitespace status string

- Given the catalog contains pet-101 (Scout, available) and pet-103 (Nova, pending)
- When a search executes with `status="  "`
- Then only available pets are returned
- And pending pets are excluded from results

### Requirement: Explicit pending status shows pending pets

When the status parameter is explicitly set to "pending", the search returns only pending pets (for support/operations use cases).

#### Scenario: Support agent searches for pending pets

- Given the catalog contains pet-101 (Scout, available) and pet-103 (Nova, pending)
- When a support agent searches with `status="pending"`
- Then only pending pets are returned
- And Nova (pet-103) is included in results
- And Scout (pet-101) is excluded from results
