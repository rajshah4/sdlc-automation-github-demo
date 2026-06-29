# Design

## Context

The Petstore app has two layers of catalog logic:

1. **catalog.py**: Core `search_pets()` function with proper status filtering (default: `status="available"`)
2. **cloud_run_app.py**: Web API with `visible_pets()` helper that currently returns ALL pets in INCIDENT_MODE

The `/api/pets` endpoint (line 237-239) uses `visible_pets()` which violates the catalog availability rule when the system is in INCIDENT_MODE. The wiki (docs/wiki/petstore-catalog-availability.md) explicitly states:

> Default customer-facing catalog search must show only pets with status="available".

Nova (pet-103) has status="pending" and is documented in the wiki as a test case for catalog regression detection.

## Decision

- Change `visible_pets()` function (lines 92-95 in cloud_run_app.py) to always filter by `status="available"`, removing the INCIDENT_MODE bypass
- This ensures the `/api/pets` endpoint never returns pending pets
- The incident detection logic remains unchanged - it can still log PENDING_PET_VISIBLE errors when misconfigured, but won't actually expose pending pets to customers
- Add a regression test to `test_cloud_run_app.py` verifying pending pets are excluded from `/api/pets` responses

## Alternative Considered

We could modify only the `/api/pets` endpoint to call `search_pets()` from catalog.py instead of `visible_pets()`. However, fixing `visible_pets()` at the source is safer because:
- It ensures consistency across all callers (home page rendering, API endpoint)
- It makes the single source of truth (available-only) explicit
- It prevents future endpoints from accidentally using the wrong helper

## Risks

- **Incident simulation behavior**: The INCIDENT_MODE is used for demo purposes to simulate catalog regressions. After this fix, INCIDENT_MODE won't actually expose pending pets. This is acceptable because:
  - The primary goal is protecting customers from seeing pending pets
  - The incident detection and logging logic remains functional
  - Demo scenarios can still show the detection and remediation flow
  
- **Test coverage**: The existing test `test_bad_catalog_filter_exposes_pending_pet` will need to be updated or removed since it explicitly tests the broken behavior we're fixing.

## Validation Plan

1. Run existing catalog tests: `pytest app/tests/test_pet_catalog.py -v`
2. Run cloud run app tests: `pytest app/tests/test_cloud_run_app.py -v`
3. Add regression test verifying `/api/pets` never returns pending pets
4. Manual verification: Start the app and verify Nova is not visible in the pets list
