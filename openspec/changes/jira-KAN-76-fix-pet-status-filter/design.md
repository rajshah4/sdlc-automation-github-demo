# Design

## Context

The Petstore catalog has a `search_pets` function that filters pets by multiple criteria including status. By design, it defaults to returning only "available" pets. However, the current implementation has a bug where passing an empty string for status bypasses the filter entirely.

The problematic code is in `app/petstore_app/catalog.py` line 53:

```python
if normalized_status and normalized_status != pet.status:
    continue
```

When `normalized_status` is an empty string, it evaluates to `False`, causing the entire status filter to be skipped.

## Decision

- Change the status filter condition from `if normalized_status and ...` to `if normalized_status != pet.status:`
- This ensures the filter is always applied, treating empty string as a literal value to match
- Since no pet has an empty string status, passing `status=""` will correctly return no results
- This is a minimal one-line change that fixes the bypass vulnerability

## Alternative Considered

We could normalize empty status to "available", but this adds complexity and may hide bugs in calling code. The simpler fix is to treat empty string as a literal filter value.

## Risks

- **Breaking change risk**: Low. If any code currently passes `status=""` expecting all pets, it will break. However, this is likely unintentional and represents a bug exploitation.
- **Test coverage**: The existing tests don't cover the empty string case, so this bug went undetected. Adding explicit test coverage mitigates future regressions.

## Validation Plan

1. Add a new test case `test_search_pets_empty_status_returns_no_results` to verify empty string behavior
2. Run existing test suite to ensure no regressions: `python3 -m pytest app/tests/test_pet_catalog.py -v`
3. Manual verification: confirm `search_pets(status="")` returns empty list
4. Manual verification: confirm default `search_pets()` still returns only available pets
