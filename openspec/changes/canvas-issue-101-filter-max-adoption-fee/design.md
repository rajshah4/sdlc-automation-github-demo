# Design: Filter pets by maximum adoption fee

## Backend – `search_pets` signature change

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

**Guard:** if `max_fee_cents` is supplied and is negative, raise `ValueError`.

**Filter predicate added inside the loop:**

```python
if max_fee_cents is not None and pet.adoption_fee_cents > max_fee_cents:
    continue
```

This is the narrowest possible change: one new keyword-only parameter, one
validation check, one filter line. No other logic is touched.

## Frontend – `index.html` input

Add to the toolbar `<section>`:

```html
<label>
  Max fee ($)
  <input id="max-fee" type="number" min="0" step="1" placeholder="any">
</label>
```

Using `type="number"` enables browser validation of numeric input without
requiring custom JavaScript validation.

## Frontend – `app.js` filter

```js
const maxFeeDollars = parseFloat(document.querySelector("#max-fee").value);
const maxFeeCents = isNaN(maxFeeDollars) || maxFeeDollars <= 0
  ? null
  : Math.floor(maxFeeDollars * 100);
```

Filter predicate added to `pets.filter`:

```js
&& (maxFeeCents === null || pet.feeCents <= maxFeeCents)
```

The static pet data in `app.js` already stores `fee` as a display string
(`"$75"`). We need to add a `feeCents` integer field to each entry to enable
numeric comparison. This is the only structural change to the pet data object.

## Data consistency note

`catalog.py` uses `adoption_fee_cents`; `app.js` uses `feeCents`. Both must
agree on the same values (Mochi 7500, Scout 12500, Pip 4500, Nova 11000).

## Human gates

- Code review by a human before merge.
- QA must verify the UI filter in a browser (screenshot evidence required by
  the Petstore product rules for UI-visible changes).
- No merge without human approval.
