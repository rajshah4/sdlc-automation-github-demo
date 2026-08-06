# Catalog Training Filter Spec Delta

## ADDED Requirements

### Requirement: Filter pets by training level

Catalog search must support an optional training level filter that returns only pets with the specified training level tag.

#### Scenario: Filter by basic training level

- Given the Petstore catalog contains pets with various training levels
- When a user searches with `training_level="basic"`
- Then only pets with "basic" training tag are returned
- And pets with other training levels are excluded
- And pets without training level tags are excluded

#### Scenario: Filter by intermediate training level

- Given the Petstore catalog contains pets with various training levels
- When a user searches with `training_level="intermediate"`
- Then only pets with "intermediate" training tag are returned
- And pets with other training levels are excluded

#### Scenario: Filter by advanced training level

- Given the Petstore catalog contains pets with various training levels
- When a user searches with `training_level="advanced"`
- Then only pets with "advanced" training tag are returned
- And pets with other training levels are excluded

#### Scenario: No training level filter applied

- Given the Petstore catalog contains pets with various training levels
- When a user searches without specifying training_level parameter
- Then all pets matching other criteria are returned
- And training level does not affect results

#### Scenario: Filter respects existing status filter

- Given the Petstore catalog contains available and pending pets
- When a user searches with `training_level="basic"` and default status="available"
- Then only available pets with basic training are returned
- And pending pets are excluded regardless of training level

#### Scenario: Combine training level with other filters

- Given the Petstore catalog contains pets with various species and training levels
- When a user searches with `species="dog"` and `training_level="basic"`
- Then only dogs with basic training are returned
- And other species are excluded
- And dogs with other training levels are excluded
