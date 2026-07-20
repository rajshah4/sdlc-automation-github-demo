# Petstore Catalog Spec Delta

## ADDED Requirements

### Requirement: Catalog search supports optional temperament filtering

Catalog search MUST support filtering pets by temperament tag. The temperament filter is optional and combines with existing filters using AND logic. Only available pets matching the selected temperament are shown by default.

#### Scenario: Search by temperament returns matching pets

- Given Mochi has tags including "calm" and Pip has tags including "quiet"
- When catalog search is called with `temperament="calm"`
- Then Mochi is included in the results
- And Pip is not included in the results

#### Scenario: Search by temperament excludes non-matching pets

- Given Scout has tags including "active" but not "calm"
- When catalog search is called with `temperament="calm"`
- Then Scout is not included in the results

#### Scenario: Clearing the temperament filter restores normal catalog

- Given the catalog has multiple available pets with different temperaments
- When catalog search is called with `temperament=None` (or omitted)
- Then all available pets are returned (up to max_results)

#### Scenario: Temperament filter works with other filters

- Given Mochi is a cat with "calm" temperament
- And Scout is a dog with "active" temperament
- When catalog search is called with `species="cat"` and `temperament="calm"`
- Then Mochi is included in the results
- And Scout is not included in the results (filtered by species)

#### Scenario: Temperament filter respects status default

- Given Nova has "active" temperament but status is "pending"
- When catalog search is called with `temperament="active"` (using default status="available")
- Then Nova is not included in the results
- Because pending pets are excluded by default

#### Scenario: Case-insensitive temperament matching

- Given Mochi has tag "calm" (lowercase)
- When catalog search is called with `temperament="Calm"` (mixed case)
- Then Mochi is included in the results
- Because temperament matching is case-insensitive
