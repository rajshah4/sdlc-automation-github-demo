# Catalog Availability Spec Delta

## ADDED Requirements

### Requirement: Default pet search excludes pending pets

Default catalog searches must return only pets with `status="available"`. Pending pets must never appear in default customer-facing search results.

#### Scenario: Default search without status parameter

- Given the catalog contains pets with various statuses including available and pending
- When a search is performed with default parameters (no status specified)
- Then only pets with `status="available"` are returned
- And pets with `status="pending"` are excluded

#### Scenario: Search with empty status string

- Given the catalog contains pets with various statuses
- When a search is performed with `status=""` (empty string)
- Then the search defaults to `status="available"`
- And only available pets are returned
- And pending pets are excluded

### Requirement: Explicit pending status search works for operations

Support and operations staff must be able to explicitly search for pending pets when needed for case investigation.

#### Scenario: Explicit pending status search

- Given the catalog contains pending pets
- When a search is performed with `status="pending"`
- Then only pets with `status="pending"` are returned
- And available pets are excluded

## MODIFIED Requirements

None - this change fixes existing requirements rather than modifying them.

## REMOVED Requirements

None - no functionality is being removed.

## Evidence Correlation

- Error code: `PENDING_PET_VISIBLE`
- Log reference: `docs/logs/pending-pet-visible.ndjson`
- Known affected pet: Nova (`pet-103` with `status="pending"`)
- Wiki reference: `docs/wiki/petstore-catalog-availability.md`
