# Catalog Availability Spec Delta

## ADDED Requirements

### Requirement: Default search excludes pending pets

Default pet search must return only pets with `status="available"`. Pending pets must not appear in customer-facing search results unless explicitly requested.

#### Scenario: Customer searches for available dogs

- Given Nova (pet-103) has `status="pending"`
- And Scout (pet-101) has `status="available"`
- When a customer searches for dogs without specifying status
- Then the results must include Scout
- And the results must NOT include Nova

#### Scenario: Default search returns only available pets

- Given the customer provides no search filters
- When the default search executes with `status="available"` (default)
- Then only pets with `status="available"` appear in results
- And pending pets remain hidden

#### Scenario: Pending pet visibility is a regression error

- Given a default search executes
- When a pending pet appears in the results
- Then this is a `PENDING_PET_VISIBLE` catalog availability regression

### Requirement: Pending pets can be found when explicitly requested

Admin tools and internal workflows must be able to search for pending pets by explicitly specifying `status="pending"`.

#### Scenario: Admin searches for pending dogs

- Given Nova (pet-103) has `status="pending"`
- When an admin searches with `status="pending"` and `species="dog"`
- Then the results must include Nova
