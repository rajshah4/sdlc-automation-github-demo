# Petstore Adoptions Spec Delta

## ADDED Requirements

### Requirement: Pet code inputs must be normalized to remove leading/trailing whitespace

Pet codes with accidental leading or trailing spaces should be accepted and correctly matched against the catalog.

#### Scenario: Pet code with leading whitespace

- Given a valid pet code is `"pet-100"`
- When an adopter submits `" pet-100"` (with leading space)
- Then the pet is found and adoption validation proceeds normally

#### Scenario: Pet code with trailing whitespace

- Given a valid pet code is `"pet-100"`
- When an adopter submits `"pet-100 "` (with trailing space)
- Then the pet is found and adoption validation proceeds normally

#### Scenario: Pet code with both leading and trailing whitespace

- Given a valid pet code is `"pet-100"`
- When an adopter submits `" pet-100 "` (with both leading and trailing spaces)
- Then the pet is found and adoption validation proceeds normally

#### Scenario: Pet code with internal whitespace remains invalid

- Given a valid pet code is `"pet-100"`
- When an adopter submits `"pet 100"` (with internal space)
- Then the pet is not found (internal whitespace is not normalized)
- And a `ValueError` is raised with message `"pet_id was not found"`

#### Scenario: Empty or whitespace-only input is invalid

- Given valid pet codes exist in the catalog
- When an adopter submits `"   "` (only whitespace)
- Then the pet is not found
- And a `ValueError` is raised with message `"pet_id was not found"`

## UNCHANGED Requirements

### Requirement: Pending pets cannot be adopted

This requirement continues to work as before.

#### Scenario: Pending pet rejection still works with normalized input

- Given pet `"pet-103"` (Nova) has status `"pending"`
- When an adopter submits `" pet-103 "` (with whitespace)
- Then the pet is found (whitespace is normalized)
- And adoption is rejected because the pet is pending
- And a `ValueError` is raised with message `"Pet pet-103 is not available"`
