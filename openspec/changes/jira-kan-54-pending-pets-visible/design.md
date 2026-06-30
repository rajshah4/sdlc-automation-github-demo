# Design

## Context

The Petstore application has two layers for pet availability:
1. **Catalog layer** (`catalog.py`): `search_pets()` function with `status="available"` default
2. **Web API layer** (`cloud_run_app.py`): `/api/pets` endpoint using `visible_pets()` function

The bug is in the web API layer. The `visible_pets()` function bypasses the catalog search and returns ALL pets when `current_mode() == INCIDENT_MODE`, ignoring the product rule that default searches must show only available pets.

## Root Cause

In `cloud_run_app.py` lines 92-95:
```python
def visible_pets() -> list[Pet]:
    if current_mode() == INCIDENT_MODE:
        return list(PETS)  # BUG: Returns ALL pets including pending
    return [pet for pet in PETS if pet.status == "available"]
```

The `/api/pets` endpoint uses this function directly instead of using `search_pets()` from the catalog module.

## Decision

**Fix the `visible_pets()` function to always return only available pets**, regardless of incident mode. The incident detection and logging should remain, but the actual pet list returned must respect availability rules.

Alternative considered but rejected:
- Replace `visible_pets()` with `search_pets()` - this would require larger refactoring
- Remove incident mode entirely - this is a demo feature and should remain

## Implementation

Change `visible_pets()` to:
```python
def visible_pets() -> list[Pet]:
    return [pet for pet in PETS if pet.status == "available"]
```

Keep incident detection for logging and status reporting, but don't let it affect which pets are returned.

## Risks

- **Low risk**: The change is a simple filter fix
- **Incident detection remains**: The `incident()` function and logging still detect when pending pets would have been shown
- **Support workflows unaffected**: Explicit `search_pets(status="pending")` calls still work

## Validation Plan

1. Add regression test: `test_api_pets_excludes_pending_pets()`
2. Verify existing test `test_search_pets_can_find_pending_pets_when_requested()` still passes
3. Run full test suite: `pytest app/tests/`
4. Manual verification: Check that Nova (pet-103) doesn't appear in `/api/pets` response
