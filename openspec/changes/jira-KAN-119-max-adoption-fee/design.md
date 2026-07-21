# Design

## Context

The Petstore catalog uses `catalog.py` with a `search_pets()` function that filters pets by query, species, status, tag, and max_results. Adoption fees are stored as integer cents in the `Pet` dataclass (`adoption_fee_cents`). The UI is a static HTML/JS interface that mirrors backend filtering logic.

Current pets and their fees:
- Mochi (cat): 7500 cents ($75)
- Scout (dog): 12500 cents ($125)
- Pip (rabbit): 4500 cents ($45)
- Nova (dog, pending): 11000 cents ($110)

## Decision

- Add an optional `max_adoption_fee_cents: int | None = None` parameter to `search_pets()`.
- When provided, filter pets to include only those with `adoption_fee_cents <= max_adoption_fee_cents`.
- Validate that `max_adoption_fee_cents` is not negative; raise `ValueError` if invalid.
- Update the UI to add a "Max Adoption Fee" input field (dollar format) that converts to cents for backend logic.
- Keep the implementation minimal — no new dependencies, no schema changes, no auth changes.

## Risks

- **Fee representation mismatch**: The UI displays dollars but the backend uses cents. Mitigation: Clearly convert dollars to cents in the UI logic (multiply by 100).
- **Validation edge cases**: Empty or non-numeric UI input. Mitigation: UI handles empty input as "no filter"; non-numeric values are ignored or cause no filter to be applied.
- **Boundary testing**: Pets exactly at the maximum fee should be included. Mitigation: Use `<=` operator and add explicit test cases.

## Validation Plan

- Run `pytest app/tests/test_pet_catalog.py` to verify new test cases pass.
- Manually inspect `app/web/index.html` and `app/web/app.js` to confirm UI changes render correctly.
- Validate OpenSpec-style change folder with `python3 skills/sdlc-story/scripts/validate_open_spec.py openspec/changes/jira-KAN-119-max-adoption-fee`.
