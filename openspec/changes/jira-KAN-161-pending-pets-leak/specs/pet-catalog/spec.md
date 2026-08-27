# Pet Catalog Spec Delta

## ADDED Requirements

### Requirement: Default catalog search excludes pending pets

#### Scenario: Customer searches without specifying status

- Given pet-103 "Nova" has `status="pending"`
- When a customer performs a default search (no explicit status parameter)
- Then Nova must not appear in the search results
- And only pets with `status="available"` are shown

#### Scenario: Backend search called without status parameter

- Given the backend `search_pets()` function
- When called with no explicit `status` parameter
- Then it defaults to `status="available"`
- And returns only available pets

#### Scenario: Frontend filtering with hardcoded pets

- Given the frontend pets array includes pet-103 with `status="pending"`
- When the search filter is applied
- Then pending pets are excluded from results
- And only `status === "available"` pets are displayed

### Requirement: Pending pets are visible only when explicitly requested

#### Scenario: Operations explicitly requests pending pets

- Given pet-103 "Nova" has `status="pending"`
- When `search_pets(status="pending")` is called
- Then Nova appears in the results
- And this is the expected behavior for operations staff

### Requirement: Handle edge cases defensively

#### Scenario: Pet with null or undefined status

- Given a pet with `status=null` or `status=undefined`
- When default catalog search is performed
- Then that pet must not appear in available pets
- And the system gracefully handles the edge case

#### Scenario: Pet with empty string status

- Given a pet with `status=""`
- When default catalog search is performed
- Then that pet must not appear in available pets
- And only pets with explicit `status="available"` are shown

## MODIFIED Requirements

None - This fix strengthens existing requirements rather than changing them.

## REMOVED Requirements

None
