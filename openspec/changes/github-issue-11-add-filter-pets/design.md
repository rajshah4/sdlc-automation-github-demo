# Design

## Context

The Petstore catalog already stores adoption fees as integer cents in the `Pet` dataclass (`adoption_fee_cents` field). The `search_pets()` function accepts multiple optional filters (species, status, tag) and validates the `max_results` parameter. The static UI provides a simple search interface with species filtering.

Product rules:
- Default pet search returns only available pets
- Money is represented as integer cents
- UI-visible changes need UI evidence, not only unit tests

## Decision

- Add `max_fee_cents: int | None = None` parameter to `search_pets()` function
- Validate that `max_fee_cents`, if provided, is non-negative (reject negative values with ValueError)
- Filter pets where `pet.adoption_fee_cents <= max_fee_cents` when the parameter is provided
- Add a number input field to `app/web/index.html` for "Max Adoption Fee (dollars)"
- Update `app/web/app.js` to parse the dollar amount, convert to cents, and filter the client-side pet list accordingly
- Keep the UI dependency-free (no frameworks, plain HTML/CSS/JS)

## Risks

- **Input validation**: Negative fees could bypass filters if not validated. Mitigation: Add explicit validation that raises ValueError for negative values.
- **Currency confusion**: Users might confuse dollars and cents. Mitigation: Label the UI field as "dollars" and convert to cents in the backend/frontend logic.
- **Edge case (zero fee)**: A max fee of zero should exclude all pets with fees. This is correct behavior and requires no special handling.
- **Backward compatibility**: Existing searches without the fee parameter must continue to work. Mitigation: Make the parameter optional with a default of `None`.

## Validation Plan

- Run focused backend tests: `python3 -m pytest -q app/tests/test_pet_catalog.py::test_search_pets_filters_by_max_fee`
- Run full backend test suite: `python3 -m pytest -q app/tests/test_pet_catalog.py`
- Serve static UI: `python3 -m http.server 4173 --directory app/web`
- Manual UI smoke test: Open browser, enter max fee, verify filtering works
- Automated UI validation (if available): `python3 skills/sdlc-qa/scripts/static_ui_smoke.py --url http://localhost:4173`
