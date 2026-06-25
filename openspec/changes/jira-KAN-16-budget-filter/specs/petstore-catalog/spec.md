# Petstore Catalog UI Spec Delta

## Context

The backend Petstore Catalog Search capability already supports filtering by maximum adoption fee (`max_adoption_fee_cents` parameter). This spec delta covers the UI layer changes to expose this capability to families searching for pets.

## ADDED Requirements

### Requirement: UI provides budget filter input

The pet search UI MUST provide an input field for families to specify their maximum adoption budget in dollars.

#### Scenario: Budget input field is visible and accessible

- Given a family visits the petstore search page
- When the page loads
- Then a "Maximum Budget" input field is visible alongside name and species filters

#### Scenario: Budget filter narrows search results

- Given available pets with varying adoption fees
- When a family enters a maximum budget (e.g., $75)
- And clicks "Find Pets"
- Then only pets at or below that budget are displayed

#### Scenario: Empty budget shows all pets

- Given available pets
- When no budget is entered
- And "Find Pets" is clicked
- Then all available pets are displayed (no fee filtering)

#### Scenario: Budget combines with other filters

- Given available pets
- When a family selects species "dog" and budget $100
- And clicks "Find Pets"
- Then only dogs with adoption fees at or below $100 are displayed

### Requirement: Dollar-to-cents conversion

The UI MUST convert user-entered dollar amounts to integer cents before filtering, consistent with the backend data model.

#### Scenario: Dollar input converts to cents correctly

- Given a user enters $75 in the budget field
- When filtering is applied
- Then the filter checks against 7500 cents

### Requirement: Graceful handling of edge cases

The UI MUST handle invalid or edge-case budget inputs without breaking functionality.

#### Scenario: Non-numeric input is ignored

- Given a user enters invalid text in the budget field
- When "Find Pets" is clicked
- Then no budget filter is applied (shows all available pets)

#### Scenario: Zero or negative budget is handled

- Given a user enters $0 or negative value
- When "Find Pets" is clicked
- Then no pets are displayed (since all adoption fees are positive)
