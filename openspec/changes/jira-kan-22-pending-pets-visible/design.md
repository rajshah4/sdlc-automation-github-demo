# Design

## Context

The Petstore catalog stores pet availability in the `status` field. The `catalog.py` module provides a `search_pets()` function with correct default filtering (status="available"). However, the `/api/pets` endpoint in `cloud_run_app.py` uses a custom `visible_pets()` function instead of leveraging the catalog's proven search logic.

## Current Implementation

- `catalog.py`: Contains `search_pets()` with `status="available"` default parameter
- `cloud_run_app.py`: Contains `visible_pets()` function that manually filters PETS
- `/api/pets` endpoint: Uses `visible_pets()` instead of `search_pets()`
- Tests confirm `search_pets()` works correctly for both available and pending searches

## Decision

- Refactor `/api/pets` endpoint to use `search_pets()` from catalog.py for consistent filtering logic
- Preserve `status="available"` as the default catalog search behavior
- Maintain the incident mode simulation (INCIDENT_MODE) which is used for demo purposes
- Add regression test to confirm pending pets don't appear in default API results
- Preserve explicit `status="pending"` searches for support workflows

## Implementation Approach

1. Import `search_pets` in `cloud_run_app.py`
2. Update `/api/pets` endpoint to call `search_pets()` instead of `visible_pets()`
3. Keep `visible_pets()` for the HTML home page rendering (maintains demo incident mode)
4. Add regression test for `/api/pets` endpoint behavior

## Risks

- **Low risk**: Using `search_pets()` is more robust as it's the proven catalog logic
- **Mitigation**: Preserve `visible_pets()` for home page to maintain demo incident simulation
- Support workflows that explicitly request `status="pending"` are unaffected

## Validation Plan

- Run focused catalog tests for default pending-pet exclusion and explicit pending searches
- Run cloud run app tests to verify endpoint behavior
- Add new test specifically for `/api/pets` endpoint excluding pending pets
- Run the full pytest suite before opening the PR
