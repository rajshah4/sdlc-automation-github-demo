# Catalog API Availability Filtering Spec Delta

## ADDED Requirements

### Requirement: API endpoint excludes unavailable pets from default catalog

The `/api/pets` API endpoint MUST return only available pets by default, excluding pending pets from the customer-facing catalog.

#### Scenario: Default API catalog call excludes pending pets

- Given Nova (pet-103) has status `pending`
- When a client calls `/api/pets` with no query parameters
- Then the response includes pet-100, pet-101, and pet-102
- And the response does NOT include pet-103

#### Scenario: Explicit pending-pet API search still works for support

- Given Nova (pet-103) has status `pending`
- When a support client calls `/api/pets?status=pending`
- Then the response includes pet-103
- And the response does NOT include available pets

#### Scenario: Available dog API search excludes pending dogs

- Given Scout (pet-101) is available and Nova (pet-103) is pending
- When a client calls `/api/pets?status=available` filtered by species=dog
- Then Scout is included in the results
- And Nova is excluded from the results

## MODIFIED Requirements

### Requirement: API endpoint uses catalog search logic

The `/api/pets` API endpoint MUST use the existing `search_pets()` function from `catalog.py` to ensure consistent status filtering across all catalog surfaces.

#### Scenario: API endpoint delegates to catalog search

- Given the `/api/pets` endpoint receives a request
- When the endpoint processes the request
- Then it calls `catalog.search_pets()` with appropriate status parameter
- And returns the filtered results as JSON
