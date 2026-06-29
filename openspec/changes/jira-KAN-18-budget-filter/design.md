# Design

## Context

The Petstore demo has:
- Backend catalog search in `app/petstore_app/catalog.py` with `max_adoption_fee_cents` parameter already implemented
- Static UI in `app/web/index.html` and `app/web/app.js` using client-side filtering
- Pet data duplicated in both backend (PETS tuple) and frontend (pets array)
- Backend uses integer cents; frontend displays dollar strings like "$75"
- Existing comprehensive backend tests in `app/tests/test_pet_catalog.py`

The Jira ticket uses business language ("families need to filter pets by adoption budget") which maps to the adoption fee filtering capability based on `docs/wiki/pet-discovery-affordability.md`.

## Decision

- Add a number input field labeled "Max Budget" to the HTML search controls
- Add `feeCents` property to the frontend pets array to enable numeric filtering
- Update `renderResults()` to filter by `maxBudget * 100` (converting dollars to cents)
- Treat empty or zero budget as "no limit" to preserve default behavior
- Keep the displayed fee strings unchanged (e.g., "$75") for visual consistency

## Implementation Details

### HTML Change

Add input field after the species selector:
```html
<label>
  Max Budget ($)
  <input id="max-budget" type="number" min="0" step="1" placeholder="Any">
</label>
```

### JavaScript Changes

1. Add `feeCents` to pet data:
   - Mochi: 7500 cents ($75)
   - Scout: 12500 cents ($125)
   - Pip: 4500 cents ($45)
   - Nova: 11000 cents ($110)

2. Update filter logic in `renderResults()`:
   ```javascript
   const maxBudget = parseFloat(document.querySelector("#max-budget").value) || 0;
   const maxBudgetCents = maxBudget > 0 ? maxBudget * 100 : Infinity;
   ```

3. Add fee filter condition:
   ```javascript
   && pet.feeCents <= maxBudgetCents
   ```

## Risks

- **Cents/dollars conversion**: Mitigated by using explicit conversion factor (100) and testing with known values
- **Data duplication**: Frontend and backend pet data remain independent; acceptable for static demo
- **No input validation for negatives**: HTML `min="0"` provides client-side protection; parseFloat fallback to 0 prevents negative filters
- **Decimal input**: `step="1"` hints whole dollars but doesn't enforce; filter works correctly with decimals (e.g., 75.50)

## Validation Plan

- Run existing backend tests to confirm no regression: `pytest app/tests/test_pet_catalog.py -v`
- Manual UI verification:
  - Load `app/web/index.html` in browser
  - Enter "100" in Max Budget field → expect Mochi ($75) and Pip ($45), exclude Scout ($125)
  - Enter "50" → expect only Pip ($45)
  - Leave empty → expect all available pets (Mochi, Scout, Pip)
  - Combine with species "dog" and budget "100" → expect no results (Scout is $125)

## Evidence Checklist

- [ ] Backend tests pass
- [ ] UI displays budget input field
- [ ] Budget filter correctly excludes high-fee pets
- [ ] Empty budget shows all available pets
- [ ] Budget combines correctly with species filter
- [ ] Displayed fee strings remain readable
