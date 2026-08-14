# Spec Delta: Pet Catalog — Max Adoption Fee Filter

## ADDED Requirements

### Requirement: Optional maximum adoption fee filter on catalog search

`search_pets` must accept an optional `max_fee_cents: int | None` parameter.
When supplied, results must include only pets whose `adoption_fee_cents` is less
than or equal to `max_fee_cents`. When omitted or `None`, all pets that pass
the other filters are returned (existing behavior is unchanged).

#### Scenario: Filter returns only pets within budget

- Given the catalog contains Mochi ($75 → 7500 cents), Scout ($125 → 12500 cents),
  and Pip ($45 → 4500 cents) with status="available"
- When `search_pets(max_fee_cents=8000)` is called
- Then results include Mochi and Pip only
- And Scout (12500 > 8000) is excluded

#### Scenario: Max fee exactly equal to a pet's fee includes that pet

- Given Pip has `adoption_fee_cents=4500`
- When `search_pets(max_fee_cents=4500)` is called
- Then Pip is included in results

#### Scenario: Max fee below all pets returns empty list

- When `search_pets(max_fee_cents=100)` is called
- Then the result list is empty

#### Scenario: Negative max fee raises ValueError

- When `search_pets(max_fee_cents=-1)` is called
- Then a `ValueError` is raised with a message referencing `max_fee_cents`

#### Scenario: Omitting max_fee_cents preserves existing behavior

- When `search_pets()` is called without `max_fee_cents`
- Then results are identical to the pre-feature behavior

### Requirement: UI exposes max adoption fee input in dollars

The static web UI toolbar must include a labeled number input `id="max-fee"`.
When the user enters a dollar value and clicks "Find Pets", results must include
only available pets whose fee is within the entered maximum.

#### Scenario: UI fee filter hides pets over the budget

- Given the page shows Mochi ($75), Scout ($125), and Pip ($45)
- When the user enters "100" in the max fee input and clicks Find Pets
- Then Scout ($125) is not visible
- And Mochi ($75) and Pip ($45) are visible

#### Scenario: Clearing the max fee input restores all available pets

- When the max fee input is cleared and Find Pets is clicked
- Then all available pets are shown again
