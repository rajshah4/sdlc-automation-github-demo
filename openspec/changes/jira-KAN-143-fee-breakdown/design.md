# Design

## Context

The Petstore app currently displays only a single total adoption fee for each pet. The Pet dataclass in `app/petstore_app/catalog.py` has an `adoption_fee_cents` field that stores the total as an integer (cents). The frontend in `app/web/app.js` displays this as a formatted dollar amount (e.g., "$75").

Adopters need to see what they're paying for: the base adoption fee, vaccination costs, and microchip costs. This transparency helps adopters understand the value and make informed decisions.

Key constraints:
- Money is represented as integer cents throughout the system (product rule)
- The static UI should remain dependency-free and simple
- Changes must be minimal and focused on the fee breakdown feature
- Default search behavior (available pets only) must not be affected

## Decision

- **Backend**: Add three new fields to the Pet dataclass: `base_fee_cents`, `vaccination_fee_cents`, and `microchip_fee_cents`
- **Backend**: Update the existing PETS tuple with realistic fee breakdowns that sum to the current `adoption_fee_cents` values
- **Frontend**: Modify the pet display in `app.js` to show the breakdown instead of just the total
- **Frontend**: Update the pet data structure in `app.js` to include breakdown fields
- **Frontend**: Add CSS styling if needed to make the breakdown readable without cluttering the UI
- **Tests**: Add test cases to verify breakdown fields exist and that values are consistent

The fee breakdown is stored data, not computed. This keeps the implementation simple and allows flexibility for different pets to have different fee structures based on their individual needs.

## Risks

- **Risk**: Existing code might assume `adoption_fee_cents` is the only fee field
  - **Mitigation**: Review existing tests and code to ensure they continue to work with new fields added
  
- **Risk**: Frontend and backend data might become inconsistent if updated separately
  - **Mitigation**: Update both frontend and backend in the same PR, with tests to verify consistency

- **Risk**: Fee breakdown might not sum exactly to the total due to rounding or data entry errors
  - **Mitigation**: Keep all values as integer cents; ensure test data has correct sums

- **Risk**: UI might become cluttered with additional fee information
  - **Mitigation**: Use clean, simple layout; show breakdown on same line or in expandable detail area

## Validation Plan

- Run backend tests: `python3 -m pytest -q app/tests/test_pet_catalog.py`
- Run all app tests: `python3 -m pytest -q app/tests/`
- Start local UI server: `python3 -m http.server 4173 --directory app/web`
- Manual verification: Open browser to http://localhost:4173 and verify fee breakdown displays correctly for each pet
- Verify existing functionality: Confirm that pet search and filtering still work as expected
