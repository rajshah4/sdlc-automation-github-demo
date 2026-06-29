# Catalog Availability Spec Delta

## ADDED Requirements

### Requirement: Default catalog search must exclude pending pets

#### Scenario: Empty status parameter defaults to available filter

- Given the pet catalog contains pets with status "available" and "pending"
- When search_pets is called with status=""
- Then only pets with status="available" are returned
- And pending pets are excluded from results

#### Scenario: Whitespace-only status parameter defaults to available filter

- Given the pet catalog contains pets with status "available" and "pending"
- When search_pets is called with status="   "
- Then only pets with status="available" are returned
- And pending pets are excluded from results

#### Scenario: Explicit pending search still works

- Given the pet catalog contains pets with status "available" and "pending"
- When search_pets is called with status="pending"
- Then only pets with status="pending" are returned
- And available pets are excluded from results

## MODIFIED Requirements

### Requirement: Status parameter filtering behavior

#### Previous behavior

- Empty or whitespace-only status parameters bypassed status filtering entirely
- This allowed all pets (including pending) to be returned

#### New behavior

- Empty or whitespace-only status parameters are normalized to "available"
- This ensures pending pets are never exposed in default searches
- Explicit status values continue to work as before

## Acceptance Criteria

- [x] Empty status string (status="") filters to available pets only
- [x] Whitespace status string (status="  ") filters to available pets only
- [x] Default status (no parameter) continues to filter to available pets only
- [x] Explicit status="pending" continues to return pending pets only
- [x] Nova (pet-103, status="pending") does not appear in empty-status searches
- [x] All existing tests continue to pass
- [x] New regression test added for empty status parameter
