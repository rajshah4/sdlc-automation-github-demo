# Catalog Spec Delta

## ADDED Requirements

### Requirement: Default catalog search returns only available pets

The default pet catalog search must exclude pets that are not ready for adoption.

#### Scenario: Default search excludes pending pets

- Given the catalog contains both available and pending pets
- When a customer searches for pets without specifying a status
- Then only pets with `status="available"` are returned
- And pending pets are not visible in the results

#### Scenario: Explicit pending search still works for operations

- Given support staff need to view pending pets for case investigation
- When operations explicitly requests `status="pending"` 
- Then pending pets are returned as requested
- And this does not affect the default customer experience

#### Scenario: Website home page shows only available pets

- Given the website displays the available pets list on the home page
- When a customer visits the home page
- Then only available pets are shown
- And pending pets like Nova (pet-103) are not visible

## CHANGED Requirements

### Requirement: Catalog filter must be reliable in healthy mode

Previously, the `visible_pets()` function could show all pets including pending ones when in incident mode. This change ensures that in healthy mode, only available pets are visible.

#### Scenario: Healthy mode filters correctly

- Given the application is running in healthy mode
- When the `/api/pets` endpoint is called
- Then the `visible_pets()` function returns only available pets
- And the `PENDING_PET_VISIBLE` error is not logged

## Evidence

- **Wiki**: `docs/wiki/petstore-catalog-availability.md` confirms default search must show only `status="available"` pets.
- **Logs**: `docs/logs/pending-pet-visible.ndjson` shows `PENDING_PET_VISIBLE` error code (pet-103/Nova visible).
- **Known mapping**: Nova is pet-103 with `status="pending"` and should not appear in default results.
