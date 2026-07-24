# Catalog Availability Spec Delta

## ADDED Requirements

### Requirement: Default search must exclude pending pets

When customers perform a default pet search without explicitly requesting pending status, only pets with status="available" must be returned.

#### Scenario: Default search excludes pending pets

- Given a catalog with pets in "available" and "pending" status
- When a customer performs a default search (no status parameter or status="available")
- Then only pets with status="available" are returned
- And pets with status="pending" are excluded from the results

#### Scenario: Default species search excludes pending pets

- Given a catalog with dog pets in both "available" and "pending" status
- When a customer searches for species="dog" with default (available) status
- Then only available dogs are returned
- And pending dogs (like Nova/pet-103) are excluded from the results

#### Scenario: Explicit pending search returns pending pets

- Given a catalog with pets in "pending" status
- When support explicitly requests status="pending"
- Then only pending pets are returned
- And this capability remains functional for operations workflows

### Requirement: Empty or missing status parameter defaults to available

The status parameter must not allow unfiltered searches. When status is empty, None, or not provided, it must default to "available".

#### Scenario: Empty status string defaults to available

- Given a search request with status=""
- When the search is executed
- Then the behavior is identical to status="available"
- And pending pets are excluded from results

#### Scenario: None status defaults to available

- Given a search request with status=None
- When the search is executed
- Then the behavior is identical to status="available"
- And pending pets are excluded from results
