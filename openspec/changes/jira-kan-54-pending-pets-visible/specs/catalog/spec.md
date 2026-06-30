# Specification: Pet Catalog Availability

## MODIFIED Requirements

### Requirement: Default catalog API excludes pending pets

The `/api/pets` endpoint must return only pets with `status="available"` by default. Pending pets should not appear in the customer-facing catalog experience.

**Current behavior**: The `visible_pets()` function returns ALL pets when in INCIDENT_MODE, violating availability rules.

**Fixed behavior**: The `visible_pets()` function always filters to `status="available"` pets only.

#### Scenario: API pets endpoint returns only available pets

**Given** the Petstore API is running  
**And** pet-103 (Nova) has `status="pending"`  
**When** a client calls `GET /api/pets`  
**Then** the response includes only pets with `status="available"`  
**And** Nova (pet-103) is excluded from the results

#### Scenario: Pending pets remain searchable when explicitly requested

**Given** the catalog has pets with `status="pending"`  
**When** a client calls `search_pets(status="pending")`  
**Then** the response includes pending pets  
**And** Nova appears in the results

## ADDED Requirements

None - this change fixes existing requirements.

## REMOVED Requirements

None - all existing functionality is preserved.
