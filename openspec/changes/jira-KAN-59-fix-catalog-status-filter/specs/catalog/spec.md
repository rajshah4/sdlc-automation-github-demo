# Catalog Status Filter Spec Delta

## MODIFIED Requirements

### Requirement: Default pet search returns only available pets

#### Scenario: Search with default status parameter

- Given the catalog contains pets with various statuses (available, pending)
- When a caller invokes `search_pets()` with default parameters
- Then only pets with `status="available"` are returned
- And pending pets are excluded from results

#### Scenario: Search with explicit empty status string

- Given the catalog contains pets with various statuses
- When a caller invokes `search_pets(status="")`
- Then the search treats empty string as "available"
- And pending pets are excluded from results

#### Scenario: Search with explicit "available" status

- Given the catalog contains pets with various statuses
- When a caller invokes `search_pets(status="available")`
- Then only pets with `status="available"` are returned
- And pending pets are excluded from results

#### Scenario: Search with explicit "pending" status

- Given the catalog contains pets with various statuses
- When a caller invokes `search_pets(status="pending")`
- Then only pets with `status="pending"` are returned
- And available pets are excluded from results

## Acceptance Criteria

- ✅ Default search excludes pending pets
- ✅ Empty status string defaults to available-only filtering
- ✅ Explicit "pending" search still works for support workflows
- ✅ Nova (pet-103) does not appear in default available search
- ✅ Regression test added to prevent future status filter bypass
