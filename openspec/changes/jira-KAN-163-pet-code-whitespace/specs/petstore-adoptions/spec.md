# Petstore Adoptions Spec Delta

## ADDED Requirements

### Requirement: Adoption order creation trims whitespace from pet codes

Adoption order creation MUST trim leading and trailing whitespace from pet codes before validation, making the system resilient to copy-paste errors while maintaining all existing pet availability and validation checks.

#### Scenario: Pet code with leading whitespace succeeds

- Given support agent copies pet code `" pet-100"` with leading space
- When adoption order is created with pet_id=`" pet-100"`
- Then adoption order is created successfully
- And order references pet "Mochi" (cat, available)

#### Scenario: Pet code with trailing whitespace succeeds

- Given pet code `"pet-101 "` is copied with trailing whitespace
- When adoption order is created with pet_id=`"pet-101 "`
- Then adoption order is created successfully
- And order references pet "Scout" (dog, available)

#### Scenario: Pet code with surrounding whitespace succeeds

- Given pet code `" pet-102 "` has both leading and trailing spaces
- When adoption order is created with pet_id=`" pet-102 "`
- Then adoption order is created successfully
- And order references pet "Pip" (rabbit, available)

#### Scenario: Whitespace does not bypass availability checks

- Given pending pet code `" pet-103 "` with whitespace
- When adoption order is created with pet_id=`" pet-103 "`
- Then request fails with availability error
- And error indicates pet cannot be adopted (status=pending)

#### Scenario: Whitespace does not create false matches

- Given invalid pet code `" pet-999 "` with whitespace
- When adoption order is created with pet_id=`" pet-999 "`
- Then request fails with ValueError("pet_id was not found")
- And whitespace does not cause incorrect pet matching
