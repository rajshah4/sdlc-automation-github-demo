# Design

## Context

The Petstore catalog module (`app/petstore_app/catalog.py`) provides a
`search_pets()` function that filters pets by name query, species, status, tag,
and max adoption fee. Each pet has an `age_months: int` field, but there is
currently no way to filter by age.

Adopters often search for pets by life stage (puppy/kitten, adult, senior)
because different ages match different lifestyles and experience levels.

The UI (`app/web/index.html` and `app/web/app.js`) already has a toolbar with
search controls and filters. We'll add age filtering controls there.

## Decision

- Add `min_age_months: int | None = None` and `max_age_months: int | None = None` parameters to `search_pets()`.
- Validate that both parameters are non-negative when provided.
- Validate that `min_age_months <= max_age_months` when both are provided.
- Apply the age filter after other filters in the search logic.
- Add a simple age category selector in the UI (e.g., radio buttons or a select dropdown) that maps to age ranges:
  - "Any" (no filter) → `min_age_months=None, max_age_months=None`
  - "Puppy/Kitten (0-12 months)" → `min_age_months=0, max_age_months=12`
  - "Adult (1-7 years)" → `min_age_months=13, max_age_months=84`
  - "Senior (7+ years)" → `min_age_months=85, max_age_months=None`
- Keep the filter logic simple: a pet matches if `min_age_months <= pet.age_months <= max_age_months`.

## Risks

- **Risk**: Overlapping or confusing age categories.
  - **Mitigation**: Use clear, standard age ranges that don't overlap.
- **Risk**: Changing the function signature might break existing callers.
  - **Mitigation**: The parameters are optional with default `None`, so all existing calls remain valid.
- **Risk**: Invalid input (negative ages, inverted ranges).
  - **Mitigation**: Raise `ValueError` with clear messages for validation failures.

## Validation Plan

- Run `pytest app/tests/test_pet_catalog.py -v` to verify new age filter tests pass.
- Manually inspect `app/web/index.html` in a browser to confirm the age filter UI appears and functions correctly.
- Verify that searching with age filters returns only matching pets.
