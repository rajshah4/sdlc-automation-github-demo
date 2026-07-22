# Petstore Catalog Spec Delta

## ADDED Requirements

### Requirement: Default search excludes pending pets

The default pet catalog search must return only pets with `status="available"` and must not include pets with other statuses such as `pending` or `adopted`.

#### Scenario: Default search without explicit status parameter

- Given a catalog containing pets with various statuses including available and pending
- When a user searches with default parameters (no status specified)
- Then only pets with `status="available"` are returned
- And pets with `status="pending"` are excluded from results

#### Scenario: Species filter with default status

- Given a catalog containing Nova (dog, pending) and Scout (dog, available)
- When a user searches for dogs using default status
- Then only Scout is returned
- And Nova (pending) is excluded

#### Scenario: Explicit pending search still works

- Given a catalog containing both available and pending pets
- When a user explicitly searches with `status="pending"`
- Then only pending pets are returned
- And this supports operational workflows that need to see pending pets

## MODIFIED Requirements

None. The existing behavior specification is correct; the implementation had a bug.

## REMOVED Requirements

None.
