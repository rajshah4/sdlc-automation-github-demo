# Design

## Context

The Petstore catalog search function (`search_pets` in `app/petstore_app/catalog.py`) currently supports filtering by query text, species, status, and tag. Each pet has an `age_months` field that is not yet exposed as a search filter.

Existing validation:
- `max_results` must be between 1 and 50.
- Default status is `"available"` to exclude pending pets from general browsing.

## Decision

- Add an optional `max_age_months: int | None = None` parameter to `search_pets()`.
- Validate that `max_age_months`, if provided, is non-negative (raise ValueError for negative values).
- Filter the pet list to exclude pets where `pet.age_months > max_age_months`.
- Place the age filter after other filters in the loop to maintain existing filter order.
- Preserve all existing behavior when `max_age_months` is not provided.

## Risks

- **Risk**: Confusion if age is misunderstood as years instead of months.
  - **Mitigation**: Use clear parameter name `max_age_months` and document in docstring.
- **Risk**: Zero age might be treated as "no filter" instead of literal zero.
  - **Mitigation**: Distinguish `None` (no filter) from `0` (literal zero months) explicitly.

## Validation Plan

Run focused catalog tests:
```bash
python3 -m pytest -xvs app/tests/test_pet_catalog.py -k age
```

Run full catalog test suite:
```bash
python3 -m pytest -q app/tests/test_pet_catalog.py
```

Verify no regressions in other tests:
```bash
python3 -m pytest -q app/tests/
```
