# Tasks: Filter pets by maximum adoption fee

## Implementation checklist

- [x] Add `max_fee_cents` keyword-only parameter to `search_pets` in `catalog.py`
- [x] Validate that `max_fee_cents` is non-negative when supplied
- [x] Add `feeCents` integer field to each pet entry in `app.js`
- [x] Add max-fee number input to toolbar in `index.html`
- [x] Wire max-fee filter into `renderResults` in `app.js`
- [x] Add focused backend tests: match, exclusion, edge values, negative guard
- [x] Run `pytest app/tests/test_pet_catalog.py` – all pass
- [x] Run full test suite `pytest app/tests/` – all pass

## Human gates

- [ ] Human reviews code diff on the draft PR
- [ ] Human (or QA automation) verifies UI in browser and provides screenshot
- [ ] Human approves and merges

## Validation plan

1. `pytest app/tests/test_pet_catalog.py -v` – targeted pass
2. `pytest app/tests/ -v` – full suite pass
3. Manual browser test: open `app/web/index.html`, enter `50` in Max fee field,
   verify only Pip ($45) appears; clear field, verify Mochi, Scout, Pip appear.
