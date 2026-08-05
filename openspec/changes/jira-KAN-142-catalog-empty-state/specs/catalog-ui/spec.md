# Catalog UI Spec Delta

## ADDED Requirements

### Requirement: Clear empty-state message when filters exclude all items

#### Scenario: User applies filters that produce no results

- Given the user has applied filters (name search and/or species selection) on the catalog page
- When the filtered results are empty (no pets match)
- Then the UI displays "No available pets match this search." with a "Clear filters" button

#### Scenario: User clicks the "Clear filters" button

- Given the user sees the empty-state message with the "Clear filters" button
- When the user clicks the "Clear filters" button
- Then all filter inputs are reset to their default values (name cleared, species set to "Any")
- And the results list updates to show all available pets

#### Scenario: Empty state is focused on the catalog page only

- Given this is a UI-only change
- When filters produce no results
- Then the change affects only the frontend catalog display
- And no backend changes are needed
