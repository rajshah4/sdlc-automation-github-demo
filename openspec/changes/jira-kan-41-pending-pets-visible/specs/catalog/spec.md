# Catalog Spec Delta

## ADDED Requirements

### Requirement: Default visible pets must exclude pending status

The default available pets list must only return pets with status "available" and must never return pets with status "pending".

#### Scenario: Default visible pets query excludes pending pets

- Given the catalog contains pets with various statuses including "available" and "pending"
- And Nova (pet-103) has status "pending"
- When the system calls `visible_pets()` without any status override
- Then the returned list contains only pets with status "available"
- And Nova is not in the returned list

#### Scenario: Pending pet cannot appear in default available list

- Given Nova (pet-103) exists in the catalog with status "pending"
- When a customer views the default available pets experience
- Then Nova does not appear in the results
- And no pending pets appear in the results

## MODIFIED Requirements

None - this change restores the original intended behavior.

## REMOVED Requirements

### Requirement: Incident mode simulation exposes pending pets (REMOVED)

The previous incident simulation logic that returned all pets regardless of status when `current_mode() == INCIDENT_MODE` is being removed. This was causing the bug reported by customers.
