# Catalog Availability Spec Delta

## ADDED Requirements

### Requirement: Default Search Returns Only Available Pets

#### Scenario: Customer performs default pet search

- Given the pet catalog has pets with `status="available"` and `status="pending"`
- When a customer performs a default search with no status specified
- Then only pets with `status="available"` are returned
- And pets with `status="pending"` are excluded from results

#### Scenario: Customer searches for pets by species

- Given the catalog has both available and pending dogs
- When a customer searches for dogs without specifying status
- Then only available dogs are returned
- And pending dogs like Nova (pet-103) are excluded

### Requirement: Support Can Search Pending Pets

#### Scenario: Support searches for pending pets explicitly

- Given support needs to view pets awaiting processing
- When support requests `status="pending"` explicitly
- Then pending pets are returned
- And available pets are excluded

### Requirement: Empty Status Does Not Bypass Filter

#### Scenario: Caller passes empty status string

- Given a caller passes `status=""`
- When the search is executed
- Then the default available-only behavior applies
- And pending pets are excluded from results
