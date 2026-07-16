# Design

## Context

The Petstore catalog search function `search_pets()` in `app/petstore_app/catalog.py` already defaults `status="available"` and correctly filters results to exclude pending pets. The adoption order creation in `app/petstore_app/adoptions.py` already validates pet status and rejects pending pets. The frontend UI in `app/web/app.js` already filters by `status === "available"`.

However, the test suite lacks explicit coverage for the default search behavior. The existing test `test_search_pets_filters_by_species_and_status()` passes `species="dog"` which implicitly relies on the default `status="available"`, but no test explicitly verifies that calling `search_pets()` with no parameters returns only available pets.

## Decision

- Add a focused regression test `test_search_pets_default_excludes_pending_pets()` that calls `search_pets()` without parameters and verifies only available pets are returned.
- Add a second test `test_search_pets_explicit_status_available_excludes_pending_pets()` that explicitly passes `status="available"` to verify the behavior is consistent.
- No backend or frontend code changes required; implementation is already correct.
- This is a test-only change to prevent future regressions.

## Risks

- **Low risk**: Adding tests does not change application behavior.
- **Mitigation**: Run full test suite to ensure no unintended side effects.

## Validation Plan

- Run `python3 -m pytest app/tests/test_pet_catalog.py -v` to verify new tests pass
- Run `python3 -m pytest app/tests/test_adoptions.py -v` to verify adoption tests still pass
- Run full test suite `python3 -m pytest -q` to ensure no regressions
