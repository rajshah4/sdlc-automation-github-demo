# Catalog Availability Spec Delta

## Context

Per `docs/wiki/petstore-catalog-availability.md`:
- Default customer-facing catalog search must show only pets with `status="available"`
- Pending pets must not appear in default available-pets experience
- Operations staff may explicitly request `status="pending"` when needed

## VERIFIED Requirements

### Requirement: Default catalog excludes pending pets

#### Scenario: Customer searches without specifying status

- Given a customer visits the catalog page
- When they search without specifying a status filter
- Then only pets with `status="available"` appear in results
- And pending pets like Nova (pet-103) do not appear

#### Scenario: Customer searches by species without specifying status

- Given a customer searches for dogs
- When they do not specify a status filter
- Then only available dogs appear (Scout/pet-101)
- And pending dogs (Nova/pet-103) do not appear

### Requirement: Operations staff can view pending pets when explicitly requested

#### Scenario: Operations searches for pending pets

- Given an operations staff member needs to investigate a case
- When they explicitly search with `status="pending"`
- Then pending pets (Nova/pet-103) appear in results
- And available pets do not appear

## Evidence

- Wiki: `docs/wiki/petstore-catalog-availability.md`
- Log: `docs/logs/pending-pet-visible.ndjson` with error code `PENDING_PET_VISIBLE`
- Test pet: Nova (pet-103) with `status="pending"`
- Backend: `app/petstore_app/catalog.py` line 31 default parameter `status: str = "available"`
- Backend: `app/petstore_app/catalog.py` line 50 filter `if normalized_status and normalized_status != pet.status`
- Frontend: `app/web/app.js` line 17 filter `pet.status === "available"`
