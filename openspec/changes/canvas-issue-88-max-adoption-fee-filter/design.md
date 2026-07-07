# Design

## Context

The Petstore catalog (`app/petstore_app/catalog.py`) stores `adoption_fee_cents`
as an integer. The static UI (`app/web/app.js`) stores fee as a formatted dollar
string (e.g. `"$75"`). Both surfaces are independent: the backend filter uses
integer cents; the UI converts dollar input to cents locally with a `feeToCents()`
helper.

Default `search_pets()` returns only `"available"` pets. The fee filter
compounds with that existing status filter — pending pets are never shown.

## Decision

- Add `max_fee_cents: int | None = None` to `search_pets()` signature.
- Validate `max_fee_cents >= 0`; raise `ValueError("max_fee_cents must be >= 0")` otherwise.
- Add filter predicate before `matches.append(pet)`:
  `if max_fee_cents is not None and pet.adoption_fee_cents > max_fee_cents: continue`
- In `app.js`, add `feeToCents(feeStr)` that strips `$` and returns `Math.round(parseFloat(feeStr) * 100)`.
- Read `#max-fee` input value; convert to cents only when non-empty.
- Add `&& (maxFeeCents === null || feeToCents(pet.fee) <= maxFeeCents)` to the filter chain.
- Wire an `input` listener on `#max-fee` so fee edits refresh results without clicking Search.
- Add `<input id="max-fee" type="number" min="0" step="1" placeholder="Any">` inside `.toolbar` in `index.html`.

## Risks

| Risk | Severity | Mitigation |
|------|----------|------------|
| Fee format mismatch: backend cents vs UI dollar string | Medium | `feeToCents()` helper isolates the conversion |
| Negative fee input from user | Low | HTML `min="0"` prevents browser-side negatives; backend raises `ValueError` |

## Validation Plan

```bash
# Focused backend unit tests
python3 -m pytest -q app/tests/test_pet_catalog.py

# Full suite regression
python3 -m pytest -q
```
