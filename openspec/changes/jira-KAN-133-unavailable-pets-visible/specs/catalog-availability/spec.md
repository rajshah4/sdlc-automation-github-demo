# Petstore Catalog Availability Spec Delta

## ADDED Requirements

### Requirement: Empty status string defaults to available

When the status parameter is an empty string or contains only whitespace, the search function MUST default to showing only available pets.

#### Scenario: Empty status string shows only available pets

- Given Nova has status `pending` and Scout has status `available`
- When catalog search is called with `status=""`
- Then only available pets are returned
- And Nova is not included in the results

#### Scenario: Whitespace-only status string shows only available pets

- Given Nova has status `pending`
- When catalog search is called with `status="  "`
- Then only available pets are returned
- And Nova is not included in the results

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
