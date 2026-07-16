# Catalog Availability Spec Delta

## ADDED Requirements

### Requirement: Default search must exclude pending pets

Default catalog searches that do not specify status must return only available pets. Pending pets must not appear in default search results even if they match other criteria (name, species, tags).

#### Scenario: Default search without parameters excludes pending pets

- Given the Petstore catalog contains available pets (Mochi, Scout, Pip) and a pending pet (Nova)
- When a customer calls `search_pets()` without any parameters
- Then the results include only available pets (Mochi, Scout, Pip)
- And the results do not include the pending pet (Nova/pet-103)

#### Scenario: Default search with species filter excludes pending pets

- Given Nova (pet-103) is a dog with status="pending"
- And Scout (pet-101) is a dog with status="available"
- When a customer searches for `search_pets(species="dog")`
- Then the results include only Scout (pet-101)
- And the results do not include Nova (pet-103)

#### Scenario: Explicit pending search can find pending pets when requested

- Given Nova (pet-103) is a dog with status="pending"
- When support explicitly searches `search_pets(species="dog", status="pending")`
- Then the results include Nova
- And available dogs are excluded

### Requirement: Pending pets cannot be adopted

Adoption orders must reject pets with status other than "available".

#### Scenario: Attempting to adopt a pending pet is rejected

- Given Nova (pet-103) has status="pending"
- When an adopter attempts `create_adoption_order("pet-103", "customer@example.com")`
- Then the operation raises ValueError with message "pet is not available for adoption"
