# Catalog Availability Spec Delta

## MODIFIED Requirements

### Requirement: Default pet search returns only available pets

The `search_pets()` function must filter to `status="available"` when status is not explicitly specified, is an empty string, or contains only whitespace.

#### Scenario: Empty status string defaults to available pets only

- Given the pet catalog contains Mochi (available), Scout (available), Pip (available), and Nova (pending)
- When `search_pets(status="")` is called
- Then only Mochi, Scout, and Pip are returned
- And Nova is NOT in the results

#### Scenario: Whitespace-only status defaults to available pets only

- Given the pet catalog contains Mochi (available), Scout (available), Pip (available), and Nova (pending)
- When `search_pets(status="  ")` is called
- Then only Mochi, Scout, and Pip are returned
- And Nova is NOT in the results

#### Scenario: Explicit available status returns only available pets

- Given the pet catalog contains pets with mixed statuses
- When `search_pets(status="available")` is called
- Then only pets with status="available" are returned

#### Scenario: Explicit pending status returns only pending pets

- Given the pet catalog contains Mochi (available), Scout (available), Pip (available), and Nova (pending)
- When `search_pets(status="pending")` is called
- Then only Nova is returned
- And available pets are NOT in the results
