# Petstore Catalog Spec Delta

## ADDED Requirements

### Requirement: Default catalog search excludes pending pets

Catalog search MUST exclude pending pets from the default available-pets experience.

#### Scenario: Default available-pets search excludes pending pets

- Given Nova has status `pending`
- When catalog search is called with default options
- Then Nova is not included in the results
- And Mochi, Scout, and Pip (all available) are included

#### Scenario: Explicit pending-pet search still works

- Given Nova has status `pending`
- When catalog search is called with `status="pending"`
- Then Nova is included in the results
- And available pets are not included

#### Scenario: Available dog search excludes pending dogs

- Given Scout is available and Nova is pending
- When catalog search is called for available dogs (`species="dog"`)
- Then Scout is included and Nova is excluded

