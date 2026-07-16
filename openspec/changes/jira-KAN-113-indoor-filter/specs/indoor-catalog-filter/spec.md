# Indoor Catalog Filter Spec Delta

## ADDED Requirements

### Requirement: Indoor-only filter control in catalog UI

#### Scenario: Filter enabled shows only indoor-friendly pets

- Given the catalog contains pets with various tags including "indoor"
- When an adopter enables the "Indoor only" control
- Then only available pets tagged "indoor" are displayed
- And pending pets remain excluded from results

#### Scenario: Filter disabled shows all available pets

- Given the catalog contains multiple available pets
- When an adopter disables or does not enable the "Indoor only" control
- Then all available pets are displayed regardless of tags
- And pending pets remain excluded from results

#### Scenario: Indoor filter works with name filter

- Given an adopter has entered a pet name query
- When the adopter enables the "Indoor only" control
- Then only available pets matching both the name query AND the "indoor" tag are displayed

#### Scenario: Indoor filter works with species filter

- Given an adopter has selected a species filter
- When the adopter enables the "Indoor only" control
- Then only available pets matching both the species AND the "indoor" tag are displayed

#### Scenario: Indoor filter has accessible label

- Given the catalog UI displays filter controls
- When an adopter views the "Indoor only" control
- Then the control has an accessible label element
- And the label is associated with the input control
