# Catalog Search Spec Delta

## ADDED Requirements

### Requirement: Filter pets by maximum adoption fee

The catalog search must accept an optional maximum adoption fee constraint and return only pets whose adoption fee is less than or equal to the specified maximum.

#### Scenario: Include pets within budget

- Given a search with `max_fee_cents=10000` (equals $100.00)
- When the catalog contains pets with fees of $75, $125, $45, and $110
- Then results include only pets with fees of $75 and $45
- And pets with fees of $125 and $110 are excluded

#### Scenario: Exclude pets above budget

- Given a search with `max_fee_cents=5000` (equals $50.00)
- When the catalog contains pets with fees of $75, $125, $45, and $110
- Then results include only the pet with a fee of $45
- And all pets with fees above $50 are excluded

#### Scenario: No max fee specified returns all matching pets

- Given a search without `max_fee_cents` specified
- When the catalog contains pets with various fees
- Then all pets matching other criteria are returned
- And no fee-based filtering is applied

#### Scenario: Reject negative max fee values

- Given a search with `max_fee_cents=-100`
- When the search is executed
- Then a ValueError is raised
- And the error message indicates that negative fees are not allowed

#### Scenario: Zero max fee excludes all pets with fees

- Given a search with `max_fee_cents=0`
- When the catalog contains pets with positive adoption fees
- Then no pets are returned
- And the search completes without error

### Requirement: UI provides max adoption fee input

The static web UI must provide a simple input control for users to specify their maximum budget.

#### Scenario: User enters max fee and filters results

- Given the user opens the Petstore UI
- When the user enters "100" in the max adoption fee field
- And clicks "Find Pets"
- Then only pets with fees at or below $100 are displayed
- And pets with higher fees are hidden

#### Scenario: Empty max fee input shows all pets

- Given the user has previously entered a max fee
- When the user clears the max adoption fee field
- And clicks "Find Pets"
- Then all available pets matching other criteria are shown
- And no fee-based filtering is applied
