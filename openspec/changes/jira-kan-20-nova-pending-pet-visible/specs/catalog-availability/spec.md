# Catalog Availability Spec Delta

## ADDED Requirements

### Requirement: Customer-facing catalog API must exclude pending pets

The `/api/pets` endpoint represents the customer-facing available pets catalog and must return only pets with `status="available"`, never pending pets.

#### Scenario: Default catalog request excludes pending pets

- Given Nova (pet-103) has status="pending"
- When a customer requests the pets API at `/api/pets`
- Then the response must not include Nova or any pending pets
- And only pets with status="available" must be returned

#### Scenario: Pending pets never visible regardless of system mode

- Given the system is in any operational mode (healthy or incident simulation)
- When a customer requests the pets API at `/api/pets`
- Then the response must exclude all pending pets
- And only available pets must be returned

## MODIFIED Requirements

### Requirement: visible_pets() must always filter by available status

The `visible_pets()` helper function must consistently return only available pets, maintaining the catalog availability rule as the single source of truth.

#### Scenario: visible_pets excludes pending pets in all modes

- Given the catalog contains pets with mixed statuses (available, pending)
- When `visible_pets()` is called
- Then only pets with status="available" are returned
- And pending pets like Nova (pet-103) are excluded
