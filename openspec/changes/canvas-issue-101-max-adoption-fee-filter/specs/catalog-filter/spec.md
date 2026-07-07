# catalog-filter Spec Delta

## ADDED Requirements

### Requirement: search_pets accepts an optional max_fee_cents filter

`search_pets()` must accept an optional `max_fee_cents: int | None` keyword
argument (default `None`). When supplied, any pet whose `adoption_fee_cents`
exceeds `max_fee_cents` must be excluded from results.

#### Scenario: filter returns only pets at or below the threshold

- Given the pet catalog contains Mochi ($75), Scout ($125), and Pip ($45) as available
- When `search_pets(max_fee_cents=12000)` is called
- Then the result includes Mochi and Pip and excludes Scout

#### Scenario: exact fee boundary is inclusive

- Given Mochi has `adoption_fee_cents=7500`
- When `search_pets(max_fee_cents=7500)` is called
- Then Mochi is included in the result

#### Scenario: negative max_fee_cents raises ValueError

- Given any call to `search_pets`
- When `max_fee_cents=-1` is supplied
- Then `ValueError` is raised with a message mentioning `max_fee_cents`

#### Scenario: no upper bound when max_fee_cents is None

- Given `max_fee_cents` is not supplied
- When `search_pets()` is called
- Then all available pets are returned regardless of adoption fee

---

### Requirement: UI exposes a max fee dollar input

The toolbar in `app/web/index.html` must contain a numeric input for max fee
in dollars. Changing or clearing the input immediately re-filters visible pets.

#### Scenario: entering a dollar amount hides pets above that fee

- Given the UI is loaded and all available pets are visible
- When the user enters "100" in the max fee input and the page re-renders
- Then Scout ($125) is hidden and Mochi ($75) and Pip ($45) remain visible

#### Scenario: clearing the input restores all available pets

- Given the max fee input has a value that hides Scout
- When the user clears the max fee input
- Then Scout reappears in the results
