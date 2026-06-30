# Design

## Context

The Petstore application has a catalog module (`app/petstore_app/catalog.py`) and a Cloud Run web application (`app/petstore_app/cloud_run_app.py`). The catalog module provides a `search_pets()` function with a `status` parameter that defaults to `"available"`.

The Cloud Run app has a `visible_pets()` function that is used by the website and `/api/pets` endpoint. Currently, in healthy mode, this function returns all available pets correctly, but the implementation relies on filtering in the `visible_pets()` function rather than using the catalog's built-in status filter.

According to the wiki (`docs/wiki/petstore-catalog-availability.md`), default catalog searches must show only `status="available"` pets. Log evidence (`docs/logs/pending-pet-visible.ndjson`) shows error code `PENDING_PET_VISIBLE` indicating that pet-103 (Nova, a pending pet) was visible in the available-pets experience.

## Decision

- **No changes needed to `catalog.py`**: The `search_pets()` function already defaults to `status="available"`, which is the correct behavior.
- **Fix `visible_pets()` in `cloud_run_app.py`**: The current implementation returns a filtered list in healthy mode, which is correct. The issue is that the web application is calling `visible_pets()` directly instead of using the catalog's `search_pets()` function.
- **Use the catalog's search function**: Modify the `/api/pets` endpoint and related code to use `catalog.search_pets()` which properly defaults to available pets.

Upon closer inspection of the code:
- Line 92-95 in `cloud_run_app.py`: `visible_pets()` returns all PETS in incident mode, but filters to available in healthy mode
- Line 239: The `/api/pets` endpoint uses `visible_pets()` which correctly filters

The actual bug is that `visible_pets()` is correctly implemented, but we should ensure consistency and use the catalog module's search function which already has the right default behavior.

## Risks

- **Risk**: Changing the API behavior might break existing clients.
  - **Mitigation**: The change restores intended behavior; pending pets should never have been visible by default. Explicit status filters still work.

- **Risk**: Operations staff might lose access to pending pets.
  - **Mitigation**: The `search_pets(status="pending")` call still works for operations workflows.

## Validation Plan

1. Run existing tests: `python -m pytest app/tests/test_pet_catalog.py -v`
2. Add new test: Verify that default search excludes pending pets
3. Add new test: Verify that `/api/pets` endpoint returns only available pets
4. Run full test suite: `python -m pytest app/tests/ -v`
