# Catalog Search Spec Delta

## ADDED Requirements

### Requirement: Search accepts optional maximum adoption fee

The catalog search must support filtering pets by an optional maximum adoption fee to help families find pets within their budget.

#### Scenario: Pets within budget are included

- Given a catalog containing Mochi ($75.00) and Scout ($125.00)
- When searching with max_adoption_fee_cents=7500
- Then Mochi is included in results
- And Scout is excluded from results

#### Scenario: Pets at exact budget limit are included

- Given a pet with adoption_fee_cents=7500
- When searching with max_adoption_fee_cents=7500
- Then the pet is included in results

#### Scenario: All pets excluded when budget is too low

- Given a catalog where all pets cost more than $10
- When searching with max_adoption_fee_cents=1000
- Then the result list is empty

#### Scenario: No filter applied when max fee is omitted

- Given default search behavior
- When searching without max_adoption_fee_cents
- Then all available pets are returned (existing behavior)

### Requirement: Invalid negative fees are rejected

The search must reject negative maximum adoption fee values to prevent nonsensical queries.

#### Scenario: Negative fee cap raises error

- Given any search query
- When max_adoption_fee_cents is negative (e.g., -100)
- Then a ValueError is raised with a clear message

### Requirement: Budget filtering preserves status defaults

Budget filtering must compose correctly with existing status filtering.

#### Scenario: Default status filtering still applies

- Given a pending pet within budget
- When searching with max_adoption_fee_cents but no explicit status
- Then the pending pet is excluded (default status="available")

#### Scenario: Explicit status request with budget filter

- Given a pending pet within budget
- When searching with max_adoption_fee_cents and status="pending"
- Then the pending pet is included in results
