# Petstore Catalog Spec Delta

## ADDED Requirements

### Requirement: Default catalog search excludes unavailable pets

Catalog search MUST exclude pending pets from the default available-pets experience.

#### Scenario: Default available-pets search excludes pending pets

- Given Nova has status `pending`
- When catalog search is called with default options
- Then Nova is not included in the results

#### Scenario: Explicit pending-pet search still works

- Given Nova has status `pending`
- When catalog search is called with `status="pending"`
- Then Nova is included in the results

#### Scenario: Available dog search excludes pending dogs

- Given Scout is available and Nova is pending
- When catalog search is called for available dogs
- Then Scout is included and Nova is excluded
