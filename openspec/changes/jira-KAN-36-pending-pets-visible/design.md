# Design

## Context

The Petstore catalog has two implementations:
1. `catalog.py`: Contains `search_pets()` function that correctly filters by status (default: "available")
2. `cloud_run_app.py`: Contains `visible_pets()` function that bypasses status filter when in incident mode

The web endpoints (`/api/pets` and `/`) currently use `visible_pets()` which returns all pets when `current_mode() == "bad_catalog_filter"`. This incident mode is controlled by runtime configuration and is meant for demo/testing purposes.

The issue is that customer-facing endpoints should never expose pending pets, regardless of runtime mode. The `search_pets()` function in `catalog.py` is the correct implementation and source of truth.

Per `docs/wiki/petstore-catalog-availability.md`:
- Default customer catalog must show only status="available" pets
- Support workflows can explicitly request status="pending" 
- Nova (pet-103) has status="pending"
- `PENDING_PET_VISIBLE` error code indicates this regression

## Decision

- Replace `visible_pets()` calls with `search_pets()` in customer-facing endpoints
- Keep `visible_pets()` function for incident simulation if needed for other demo purposes
- Use `search_pets()` without arguments for home page (default status="available")
- Use `search_pets()` for `/api/pets` endpoint (default status="available")
- Preserve existing `search_pets(status="pending")` capability for explicit staff queries

This is the minimal change that fixes the customer issue while preserving existing correct behavior and test infrastructure.

## Risks

- **Risk**: Incident mode logs may still emit if the mode is set, even though catalog is now correctly filtered.
  - **Mitigation**: The fix ensures correct catalog behavior. Incident simulation can be adjusted separately if needed.

- **Risk**: Other endpoints or UI paths might also use `visible_pets()`.
  - **Mitigation**: Review all uses of `visible_pets()` in `cloud_run_app.py`. Currently only `/api/pets` and home page (`/`) use it for catalog display.

- **Risk**: Removing incident mode behavior might break demo scripts that expect it.
  - **Mitigation**: Not removing incident mode, just fixing the catalog to use correct filter. Demo can still simulate incidents through logs/status endpoints.

## Validation Plan

1. Run existing catalog tests: `python3 -m pytest -q app/tests/test_pet_catalog.py`
2. Add new regression test verifying default search excludes pending pets
3. Run all tests: `python3 -m pytest -q`
4. Manual verification if needed: Start server and check `/api/pets` returns only available pets
