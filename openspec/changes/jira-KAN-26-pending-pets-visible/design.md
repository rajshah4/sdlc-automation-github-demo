# Design

## Context

The Petstore catalog stores pet availability in the `status` field. The system has two layers:

1. **`catalog.py`**: Contains the `search_pets()` function with correct status filtering logic (defaults to `status="available"`)
2. **`cloud_run_app.py`**: Contains the Flask-like HTTP server with `/api/pets` endpoint

The bug is at line 239 in `cloud_run_app.py`: the `/api/pets` endpoint calls `visible_pets()` instead of using `catalog.search_pets()`. The `visible_pets()` function is designed for incident simulation, not production catalog behavior.

## Decision

- Change the `/api/pets` endpoint to use `catalog.search_pets()` instead of `visible_pets()`
- Preserve default `status="available"` catalog search behavior
- Support optional query parameter `status` to allow explicit pending-pet searches for support workflows
- Keep the `visible_pets()` function and incident simulation system unchanged (used only for demo home page rendering)
- Add API-level regression tests for the `/api/pets` endpoint

## Implementation

**File: `app/petstore_app/cloud_run_app.py`**

Change line 237-239 from:
```python
if path == "/api/pets":
    log_catalog_regression_if_present(request_id)
    return 200, {"pets": [pet_to_dict(pet) for pet in visible_pets()]}, "application/json"
```

To:
```python
if path == "/api/pets":
    from .catalog import search_pets
    status = (query.get("status") or ["available"])[0]
    pets = search_pets(status=status)
    return 200, {"pets": [pet_to_dict(pet) for pet in pets]}, "application/json"
```

This change:
- Uses the existing `search_pets()` function which has correct filtering
- Defaults to `status="available"` (only adoptable pets)
- Allows explicit `status=pending` for support workflows
- Removes the incident mode logic from the API endpoint (keeps it only in the home page rendering)

## Risks

- **Low risk**: The change is narrow and uses existing tested catalog logic
- **Residual**: The home page HTML rendering still uses `visible_pets()` for incident simulation; this is intentional for the demo but means the HTML view and API can diverge in incident mode
- **Mitigation**: The API behavior is now deterministic and correct; incident simulation affects only the demo home page

## Validation Plan

1. Run existing catalog tests to ensure `search_pets()` still works correctly
2. Add new API-level tests in `test_cloud_run_app.py` to verify:
   - `/api/pets` returns only available pets by default
   - `/api/pets` excludes pet-103 (Nova) from default results
   - `/api/pets?status=pending` returns pending pets when explicitly requested
3. Run the full pytest suite before opening the PR
