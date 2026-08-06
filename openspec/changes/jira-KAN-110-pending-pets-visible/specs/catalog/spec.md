# Catalog Availability Spec Delta

## ADDED Requirements

### Requirement: Default search excludes non-available pets

The default catalog search must return only pets with `status="available"`. Pending, adopted, or other non-available pets must not appear in default search results.

#### Scenario: Default search filters by available status

- Given a catalog containing pets with mixed statuses (available and pending)
- When a user searches without specifying status (uses default `status="available"`)
- Then only pets with `status="available"` are returned
- And pets with `status="pending"` are excluded

#### Scenario: Empty or whitespace status does not bypass filter

- Given a catalog containing pets with mixed statuses
- When a caller passes empty string or whitespace-only status
- Then the status filter must still apply
- And only pets matching the normalized status are returned

#### Scenario: Explicit pending search returns pending pets

- Given a catalog containing pets with `status="pending"`
- When a support user explicitly searches with `status="pending"`
- Then only pending pets are returned
- And this remains supported for operations workflows

## UNCHANGED Requirements

### Requirement: Species and tag filters continue to work

Species and tag filtering behavior remains unchanged. These filters work independently of status filtering.

### Requirement: Query string matching continues to work

Name-based query string matching remains unchanged and works in combination with status filtering.
