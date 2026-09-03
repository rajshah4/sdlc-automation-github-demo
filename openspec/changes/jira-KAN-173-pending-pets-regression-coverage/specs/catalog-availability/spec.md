# Catalog Availability Spec Delta

## ADDED Requirements

### Requirement: Default pet search must exclude pending pets

Default customer-facing catalog searches must never return pets with `status="pending"`. This requirement prevents customer confusion and operational overhead from customers attempting to adopt pets that are not yet ready.

#### Scenario: Empty query default search excludes pending pets

- **Given** the catalog contains both available pets (Mochi, Scout, Pip) and pending pets (Nova)
- **When** a user calls `search_pets()` with no parameters (using default `status="available"`)
- **Then** the results contain only the 3 available pets and Nova is excluded

#### Scenario: Search by name excludes pending pets from default results

- **Given** Nova (pet-103) exists in the catalog with `status="pending"`
- **When** a user searches by name `search_pets(query="nova")` with default status filter
- **Then** the search returns an empty list (0 results)
- **And** Nova is not visible to the customer

#### Scenario: Explicit pending status request allows finding pending pets

- **Given** Nova (pet-103) has `status="pending"`
- **When** a user explicitly requests `search_pets(query="nova", status="pending")`
- **Then** Nova is found and returned
- **And** this supports internal operations and support workflows

## Context

The `PENDING_PET_VISIBLE` error code (documented in `docs/logs/pending-pet-visible.ndjson`) indicates a catalog availability regression occurred on 2026-06-29 where pending pets became visible in customer-facing search results.

While the current filtering logic in `app/petstore_app/catalog.py` (line 50) correctly implements the status filter, the lack of explicit regression test coverage means future code changes could accidentally reintroduce this bug without detection.

## Acceptance Criteria

✅ **AC1**: Test suite includes explicit test for `search_pets()` with no parameters that verifies Nova (pet-103) is excluded

✅ **AC2**: Test suite includes explicit test for `search_pets(query="nova")` that verifies 0 results are returned

✅ **AC3**: All existing tests continue to pass

✅ **AC4**: New tests reference KAN-173 and PENDING_PET_VISIBLE in docstrings for future maintainability
