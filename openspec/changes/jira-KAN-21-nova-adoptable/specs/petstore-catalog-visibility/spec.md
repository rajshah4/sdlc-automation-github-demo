# Petstore Catalog Visibility Spec Delta

## Context

This spec delta addresses the catalog regression reported in Jira KAN-21 where Nova (pet-103), a pending-status pet, incorrectly appears in the default customer-facing available-pets catalog.

## ADDED Requirements

### Requirement: Default catalog visibility excludes pending pets

**Description**: The `visible_pets()` function in the web application MUST return only pets with `status="available"` for the default customer-facing catalog experience, regardless of system mode or configuration.

**Rationale**: Per `docs/wiki/petstore-catalog-availability.md`, pending pets must not appear in default available-pets results. Only explicit searches with `status="pending"` should return pending pets, and those are handled by the separate `search_pets()` API function.

#### Scenario: Default web catalog excludes Nova (pending pet)

**Given**:
- Nova has `id="pet-103"` and `status="pending"`
- System is in any operational mode (healthy or incident)

**When**:
- `visible_pets()` is called for rendering the web catalog
- No explicit status filter is provided

**Then**:
- Nova (pet-103) is NOT included in the returned list
- Only pets with `status="available"` are returned

#### Scenario: Available pets displayed correctly in web UI

**Given**:
- Mochi (pet-100), Scout (pet-101), Pip (pet-102) have `status="available"`
- Nova (pet-103) has `status="pending"`

**When**:
- User views the default available-pets web page

**Then**:
- Mochi, Scout, and Pip are visible in the catalog
- Nova is NOT visible in the catalog
- No `PENDING_PET_VISIBLE` error is logged

#### Scenario: Explicit pending-pet API search still works

**Given**:
- Nova has `status="pending"`

**When**:
- Support staff calls `search_pets(status="pending")`

**Then**:
- Nova is included in the API results
- Support workflows can still access pending pets when explicitly requested

## MODIFIED Requirements

### Requirement: System observability preserves incident detection

**Change**: The incident mode infrastructure (health checks, error logging, status banners) remains functional for observability purposes, but does NOT bypass the catalog filter.

**Previous behavior**: When in `INCIDENT_MODE`, the system returned all pets including pending ones.

**New behavior**: The catalog filter is always correct; incident mode only affects observability signals (health check status, log messages, UI banners).

## Acceptance Criteria

- [x] `visible_pets()` always returns only available pets
- [x] Test `test_visible_pets_excludes_pending_by_default` passes
- [ ] Test `test_bad_catalog_filter_exposes_pending_pet` updated and passes with correct expectations
- [ ] Test `test_search_pets_can_find_pending_pets_when_requested` continues to pass
- [ ] Full pytest suite passes
- [ ] No `PENDING_PET_VISIBLE` errors logged in default catalog operations
