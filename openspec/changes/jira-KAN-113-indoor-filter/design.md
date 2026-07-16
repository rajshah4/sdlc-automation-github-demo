# Design

## Context

The Petstore catalog already has:
- Tag-based filtering in `catalog.py` via the `tag` parameter
- Two pets with the "indoor" tag: Mochi (cat) and Pip (rabbit)
- A static UI with name and species filters
- Default behavior that shows only available pets (excludes pending)

The acceptance criteria require a UI control that filters by the "indoor" tag and works alongside existing filters.

## Decision

- Add a checkbox labeled "Indoor only" to the UI filter controls
- When checked, pass `tag="indoor"` to the existing backend filter logic
- Wire the checkbox in `app.js` to filter the pets array by the "indoor" tag
- Maintain the existing available-only default behavior
- Use a `<label>` element with proper for/id association for accessibility
- Place the control between the species dropdown and the search button for logical flow

## Risks

- Risk: UI change might not be smoke-tested in CI
  - Mitigation: Include manual UI smoke test in validation plan; document in PR
- Risk: Tag filter is case-sensitive in backend
  - Mitigation: Backend already normalizes tags to lowercase; no change needed
- Risk: Multiple tag filtering (AND logic) is not supported
  - Mitigation: This is a non-goal; document limitation if needed later

## Validation Plan

- Run focused backend tests: `python3 -m pytest -q app/tests/test_pet_catalog.py`
- Run full test suite: `python3 -m pytest -q`
- Manual UI smoke test: Serve static UI and verify checkbox toggles indoor-only results
- Verify checkbox works with name filter (e.g., "Mochi" + indoor only)
- Verify checkbox works with species filter (e.g., "cat" + indoor only)
