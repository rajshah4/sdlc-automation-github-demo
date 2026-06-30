# Catalog Availability Spec Delta

## ADDED Requirements

### Requirement: Default catalog API returns only available pets

#### Scenario: Customer requests catalog without specifying status

- Given a catalog with pets in various statuses including "available" and "pending"
- When a customer requests `/api/pets` without specifying a status filter
- Then only pets with status="available" are returned
- And pets with status="pending" (like Nova/pet-103) are not included

#### Scenario: Customer views home page

- Given a catalog with pets in various statuses including "available" and "pending"
- When a customer loads the home page `/`
- Then only pets with status="available" are displayed
- And pets with status="pending" (like Nova/pet-103) are not visible

### Requirement: Staff can explicitly search for pending pets

#### Scenario: Staff explicitly requests pending pets

- Given a catalog with pets in various statuses
- When staff calls `search_pets(status="pending")`
- Then only pets with status="pending" are returned
- And this capability remains available for support workflows

## MODIFIED Requirements

None. The existing requirement that `search_pets()` filters by status was already correct.

## REMOVED Requirements

None.
