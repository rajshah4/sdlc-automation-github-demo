# Catalog Visibility Spec Delta

## ADDED Requirements

### Requirement: Only available pets are visible to customers

#### Scenario: Normal operation shows only available pets

- Given the system is in healthy mode
- When a customer requests the pet catalog
- Then only pets with status "available" are returned
- And pets with status "pending" are excluded

#### Scenario: Incident mode does not expose pending pets

- Given the system is in incident mode
- When a customer requests the pet catalog
- Then only pets with status "available" are returned
- And pets with status "pending" are excluded

#### Scenario: Incident mode still enables observability

- Given the system is in incident mode
- When the health check endpoint is called
- Then the system reports degraded status
- And logs include incident details
- But customer-facing catalog remains filtered to available pets only

## MODIFIED Requirements

### Requirement: Incident mode affects observability, not business logic

Previously, incident mode changed both logging behavior and the catalog filter. Now incident mode only affects:
- Health check status (returns 500 instead of 200)
- Log severity and incident markers
- Error banners in the UI

Incident mode no longer affects which pets are returned by `visible_pets()`.
