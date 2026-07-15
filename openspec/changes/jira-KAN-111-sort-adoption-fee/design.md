# Design

## Context

The Petstore catalog module (`app/petstore_app/catalog.py`) provides a `search_pets()` function that filters pets by query, species, status, and tag. The function uses a simple in-memory tuple of `Pet` dataclass instances.

Current filtering behavior:
- Default status is `"available"` (excludes pending pets)
- Results are limited by `max_results` (1-50)
- No sorting is applied; results are returned in tuple order

The `Pet` dataclass includes `adoption_fee_cents` as an integer field representing the adoption fee in cents.

## Decision

Add an optional `sort_by` parameter to `search_pets()`:
- Type: `str | None = None`
- Accepted values: `"fee_asc"`, `"fee_desc"`, or `None`
- Implementation: After filtering, sort the matches list by `adoption_fee_cents`
  - `"fee_asc"`: `sorted(matches, key=lambda p: p.adoption_fee_cents)`
  - `"fee_desc"`: `sorted(matches, key=lambda p: p.adoption_fee_cents, reverse=True)`
- Validation: Raise `ValueError` for invalid `sort_by` values before filtering

This approach:
- Keeps the change minimal (one parameter, simple sorting logic)
- Preserves all existing behavior when `sort_by` is not provided
- Works naturally with existing filters (species, status, tag, query)
- Uses Python's built-in `sorted()` with a lambda key function

## Risks

- **Breaking change risk**: Low. The new parameter is optional with a default of `None`, so existing calls remain unchanged.
- **Performance**: Negligible. The in-memory PETS tuple has only 4 items; sorting is instant.
- **Test coverage**: Must cover ascending, descending, default (no sort), and invalid values.

## Validation Plan

Run focused catalog tests:
```bash
pytest app/tests/test_pet_catalog.py -v
```

Expected new test coverage:
- `test_search_pets_sort_by_fee_asc`: Verify ascending order
- `test_search_pets_sort_by_fee_desc`: Verify descending order
- `test_search_pets_default_no_sort`: Verify default behavior unchanged
- `test_search_pets_invalid_sort_by`: Verify `ValueError` for invalid values
