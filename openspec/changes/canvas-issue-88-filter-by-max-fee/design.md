# Design: Filter pets by maximum adoption fee

## Context

The Petstore catalog search supports filtering by name, species, status, and tag.
Adoption fees are already modelled as `adoption_fee_cents` (integer cents) on every
`Pet`. There is no way for coordinators to narrow results by price, which means they
must manually skip pets outside a family's budget.

## Decision

Extend `search_pets` with one new optional keyword argument rather than a new
function. This is the narrowest possible surface change; callers that omit the
argument are unaffected.

## Approach

Extend `search_pets` with one new optional keyword argument rather than a new
function. This is the narrowest possible surface change; callers that omit the
argument are unaffected.

```python
def search_pets(
    query: str = "",
    *,
    species: str | None = None,
    status: str = "available",
    tag: str | None = None,
    max_fee_cents: int | None = None,
    max_results: int = 10,
) -> list[Pet]:
```

Guard: if `max_fee_cents is not None and max_fee_cents < 0`, raise `ValueError`.

Filter step (appended after existing tag filter, before slice):

```python
if max_fee_cents is not None:
    matches = [p for p in matches if p.adoption_fee_cents <= max_fee_cents]
```

## UI Change

`index.html` gets a labeled number input after the species selector:

```html
<label>
  Max adoption fee ($)
  <input id="max-fee" type="number" min="0" step="1" placeholder="any">
</label>
```

`app.js` reads the input and passes it to the inline filter:

```js
const maxFeeDollars = parseFloat(document.querySelector("#max-fee").value);
const maxFeeCents = !isNaN(maxFeeDollars) ? Math.round(maxFeeDollars * 100) : null;
// ...
&& (maxFeeCents === null || pet.feeCents <= maxFeeCents)
```

The `pets` array in `app.js` already carries fee strings (`"$75"`). We add a
parallel integer `feeCents` field to each pet object so the filter works
without string parsing in the hot loop.

## Data consistency

The UI fee values mirror `adoption_fee_cents` in `catalog.py`:

| Pet  | Backend cents | UI feeCents |
|------|--------------|-------------|
| Mochi | 7500 | 7500 |
| Scout | 12500 | 12500 |
| Pip  | 4500 | 4500 |
| Nova | 11000 | 11000 |

## Risks

- None material; filter is additive and opt-in.
- Floating-point dollar→cent conversion uses `Math.round` to avoid off-by-one
  on inputs like `$4.50`.

## Validation Plan

1. `pytest app/tests/test_pet_catalog.py` — four new focused tests:
   - fee match (Mochi and Pip returned for max_fee_cents=8000)
   - exact boundary is inclusive (Pip returned for max_fee_cents=4500)
   - no match (empty list for max_fee_cents=100)
   - negative fee raises ValueError
2. `app/web/tests/catalog-search.playwright.mjs` — two new browser scenarios:
   - entering $100 hides Scout and shows Mochi and Pip
   - clearing the field restores the full available-pet list
3. All 13 existing tests continue to pass.
