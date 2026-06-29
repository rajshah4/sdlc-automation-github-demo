# Catalog Search Spec Delta

## ADDED Requirements

### Requirement: Default catalog search returns only available pets

#### Scenario: Default search excludes pending pets

- Given a catalog with available and pending pets
- When a search is performed without specifying status
- Then only pets with status="available" are returned

#### Scenario: Empty status string defaults to available

- Given a catalog with available and pending pets
- When a search is performed with status="" (empty string)
- Then only pets with status="available" are returned

#### Scenario: Whitespace-only status string defaults to available

- Given a catalog with available and pending pets
- When a search is performed with status="   " (whitespace only)
- Then only pets with status="available" are returned

### Requirement: Explicit pending search remains supported

#### Scenario: Support can search for pending pets explicitly

- Given a catalog with available and pending pets
- When a search is performed with status="pending"
- Then only pets with status="pending" are returned
