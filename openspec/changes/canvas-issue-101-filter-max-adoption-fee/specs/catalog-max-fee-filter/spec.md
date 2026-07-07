# Spec: Catalog max adoption fee filter

**Capability:** pet catalog search
**Change type:** additive filter parameter

## Requirements

| ID | Requirement |
|----|-------------|
| R1 | `search_pets` MUST accept an optional `max_fee_cents: int | None` keyword argument. |
| R2 | When `max_fee_cents` is `None`, filtering behavior is unchanged. |
| R3 | When `max_fee_cents` is provided, only pets with `adoption_fee_cents <= max_fee_cents` are returned. |
| R4 | When `max_fee_cents` is negative, `search_pets` MUST raise `ValueError`. |
| R5 | The `status` default (`"available"`) is preserved; pending pets remain hidden in default search. |
| R6 | The UI MUST expose a numeric max-fee input (in dollars) in the search toolbar. |
| R7 | A blank or zero UI input means no cap; all affordable pets are shown. |

## Acceptance scenarios

### Scenario A – filter by max fee includes affordable pets
Given `max_fee_cents=5000`, `search_pets()` returns Pip ($45) but not Mochi ($75) or Scout ($125).

### Scenario B – filter at exact boundary includes matching pet
Given `max_fee_cents=7500`, `search_pets()` returns Mochi and Pip.

### Scenario C – filter excludes all when cap is below minimum fee
Given `max_fee_cents=4000`, `search_pets()` returns an empty list.

### Scenario D – no cap returns all available pets
Given `max_fee_cents=None`, `search_pets()` returns Mochi, Scout, and Pip (available pets).

### Scenario E – negative cap raises ValueError
Given `max_fee_cents=-1`, `search_pets()` raises `ValueError`.

### Scenario F – pending pets remain hidden
Given `max_fee_cents=20000`, Nova (pending) is not returned.

## Evidence checklist

- [ ] All six scenarios pass as automated tests
- [ ] UI screenshot showing max-fee filter in use (human QA)
