# Search UI Spec Delta

## ADDED Requirements

### Requirement: Enter key triggers search from pet name input

#### Scenario: User presses Enter in the pet name field

- Given the pet name input field has focus
- When the user presses the Enter key
- Then the search executes with the current name and species filter values
- And the results list updates to show matching available pets

#### Scenario: Enter key respects existing filters

- Given the user has selected a species filter
- And the user has typed a pet name
- When the user presses Enter in the pet name field
- Then the search applies both the name and species filters
- And only available pets matching both criteria are shown

### Requirement: Enter key triggers search from species dropdown

#### Scenario: User presses Enter in the species field

- Given the species dropdown has focus
- When the user presses the Enter key
- Then the search executes with the current name and species filter values
- And the results list updates to show matching available pets

### Requirement: Enter key behavior matches button click

#### Scenario: Keyboard and mouse produce identical results

- Given the same search inputs (name and species)
- When the user presses Enter
- Then the results match exactly what clicking "Find Pets" would show
- And the availability rules (pending pets excluded) are respected
