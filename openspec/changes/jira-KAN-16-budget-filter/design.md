# Design

## Context

The Petstore demo has a static UI (`app/web/`) with client-side filtering. The backend catalog search function already accepts `max_adoption_fee_cents` and has complete test coverage. The UI currently has:
- Pet name search input
- Species dropdown filter
- Status filter (hardcoded to "available")

Adoption fees are stored as integer cents in the data model to avoid floating-point precision issues with money.

## Decision

### UI Input
- Add a "Maximum Budget" input field with type="number" for dollar amounts.
- Place it between the species filter and the search button to maintain visual flow.
- Use step="1" min="0" to accept whole dollar amounts.
- Add placeholder text "$" to clarify the expected format.

### Dollar-to-Cents Conversion
- Convert user's dollar input to cents by multiplying by 100.
- Handle empty/null input gracefully (no filter applied).
- Round to nearest integer to handle edge cases.

### Filtering Logic
- Mirror backend logic: exclude pets where `adoption_fee_cents > max_adoption_fee_cents`.
- Use the pet's fee stored in cents in the data structure.
- Apply the fee filter after other filters (name, species, status) for consistency.

### Data Model
- Update the `pets` array in `app.js` to store `feeCents` alongside the display fee string.
- Keep the `fee` property for display purposes ("$75", "$125", etc.).

## Risks

- **Risk**: User enters fractional dollars (e.g., $75.99).
  - **Mitigation**: Use step="1" to discourage fractional input, multiply by 100 and round.

- **Risk**: Empty or invalid input breaks filtering.
  - **Mitigation**: Check for null/undefined/empty and skip filter if not provided.

- **Risk**: Display fee strings don't match stored cents values.
  - **Mitigation**: Verify consistency during implementation.

## Validation Plan

- Visual verification: Open `app/web/index.html` in a browser and test the budget filter.
- Test scenarios:
  - No budget: Shows all available pets (Mochi $75, Scout $125, Pip $45).
  - Budget $50: Shows only Pip ($45).
  - Budget $75: Shows Mochi ($75) and Pip ($45).
  - Budget $200: Shows all available pets.
  - Combined filters: Budget $100 + Species "dog" shows no results (Scout is $125).
- Backend tests already validate the filtering logic at the catalog layer.
