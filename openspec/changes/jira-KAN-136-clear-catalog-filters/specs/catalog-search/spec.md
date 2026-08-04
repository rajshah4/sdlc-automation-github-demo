# Catalog Search Spec Delta

## ADDED Requirements

### Requirement: Clear all catalog filters

Users must be able to reset all catalog filters to their default state with a single action.

#### Scenario: Clear filters returns to default state

- Given a user has entered "Scout" in the name field
- And selected "dog" in the species dropdown
- When the user clicks the "Clear Filters" button
- Then the name field is empty
- And the species dropdown shows "Any"
- And the results list displays all available pets

#### Scenario: Clear filters with empty filters has no adverse effect

- Given no filters are applied (name is empty, species is "Any")
- When the user clicks the "Clear Filters" button
- Then the name field remains empty
- And the species dropdown remains on "Any"
- And all available pets continue to display

#### Scenario: Clear filters triggers search automatically

- Given a user has filtered to show only cats
- And the results show 1 pet (Mochi)
- When the user clicks the "Clear Filters" button
- Then the results update immediately without requiring a separate "Find Pets" click
- And all 3 available pets are displayed (Mochi, Scout, Pip)
