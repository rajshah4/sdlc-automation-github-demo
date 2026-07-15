# Catalog Spec Delta

## ADDED Requirements

### Requirement: Default catalog search excludes pending pets

The default pet catalog search must return only pets with `status="available"`. Pending pets must not appear unless explicitly requested.

#### Scenario: Default search returns only available pets

- Given a catalog containing pets with mixed statuses (available, pending)
- When a user performs a default search without specifying status
- Then only pets with `status="available"` are returned
- And pending pets are excluded from the results

#### Scenario: Available status filter excludes pending pets

- Given a catalog containing "Scout" (available) and "Nova" (pending), both dogs
- When a user searches for dogs with `status="available"`
- Then only "Scout" is returned
- And "Nova" is not in the results

#### Scenario: Explicit pending search returns pending pets

- Given a catalog containing "Nova" (pending dog)
- When a user searches for dogs with `status="pending"`
- Then "Nova" is returned
- And the search honors the explicit pending status request

## CHANGED Requirements

### Requirement: Status filter must be consistently applied

The catalog `search_pets()` function has a default `status="available"` parameter, but the filtering logic incorrectly allows the filter to be bypassed when the normalized status is an empty string.

#### Scenario: Empty string status should not bypass filter

- Given a catalog with available and pending pets
- When search_pets is called with any status parameter
- Then the status filter must be applied consistently
- And the default "available" status must always filter pending pets

## Validation

- Run existing test `test_search_pets_filters_by_species_and_status` to verify available-only default
- Run existing test `test_search_pets_can_find_pending_pets_when_requested` to verify explicit pending searches work
- Add new regression test `test_default_search_excludes_pending_pets` to ensure pending pets never appear in default results
