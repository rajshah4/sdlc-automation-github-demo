# Adoption Validation Spec Delta

## ADDED Requirements

### Requirement: Pet codes with whitespace must be accepted

Adoption requests must succeed when pet codes have accidental leading or trailing whitespace, matching the same normalization behavior that catalog search already uses.

#### Scenario: Leading whitespace in pet code

- Given a valid available pet with code "pet-100"
- When an adoption order is created with " pet-100" (leading space)
- Then the order is created successfully with the correct pet

#### Scenario: Trailing whitespace in pet code

- Given a valid available pet with code "pet-100"
- When an adoption order is created with "pet-100 " (trailing space)
- Then the order is created successfully with the correct pet

#### Scenario: Both leading and trailing whitespace

- Given a valid available pet with code "pet-100"
- When an adoption order is created with "  pet-100  " (spaces on both ends)
- Then the order is created successfully with the correct pet

### Requirement: Invalid pet codes must still fail

Whitespace normalization must not mask validation errors for genuinely invalid pet codes.

#### Scenario: Unknown pet code (after normalization)

- Given no pet exists with code "pet-999"
- When an adoption order is created with " pet-999 " (spaces around invalid code)
- Then the order fails with "pet_id was not found"

#### Scenario: Pending pet (after normalization)

- Given a pending pet with code "pet-103"
- When an adoption order is created with " pet-103 " (spaces around pending pet)
- Then the order fails with "pet is not available for adoption"
