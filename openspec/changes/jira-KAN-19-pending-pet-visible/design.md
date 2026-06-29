# Design

## Context

The Petstore app has two catalog implementations:

1. **`catalog.py`** - Core catalog logic with `search_pets()` function
   - Accepts `status` parameter with default `"available"`
   - Properly filters pets by status
   - Tests confirm it works correctly

2. **`cloud_run_app.py`** - Web application surface
   - Has a `visible_pets()` helper function (lines 92-95)
   - Currently contains mode-dependent logic:
     ```python
     def visible_pets() -> list[Pet]:
         if current_mode() == INCIDENT_MODE:
             return list(PETS)  # BUG: Returns all pets including pending
         return [pet for pet in PETS if pet.status == "available"]
     ```
   - Used by both home page and `/api/pets` endpoint

The bug is in `visible_pets()` - when `current_mode() == INCIDENT_MODE`, it bypasses status filtering and returns all pets, violating the product rule that default catalog must exclude pending pets.

## Decision

**Replace the `visible_pets()` function to use the catalog module's `search_pets()` function:**

```python
def visible_pets() -> list[Pet]:
    from .catalog import search_pets
    return search_pets(status="available")
```

This approach:
- Delegates to the already-tested catalog logic
- Removes code duplication
- Enforces the product rule: default search always filters by `status="available"`
- Removes the mode-dependent bypass that caused the regression

**Alternative considered and rejected:**

Keep the inline filtering but remove the mode check:
```python
def visible_pets() -> list[Pet]:
    return [pet for pet in PETS if pet.status == "available"]
```

Rejected because it duplicates the catalog filtering logic and doesn't leverage the existing tested function.

## Risks and Mitigation

**Risk**: The change might affect incident simulation capabilities for demo purposes.

**Mitigation**: The incident mode simulation can still work through other mechanisms:
- The incident detection logic (`incident()` function) remains unchanged
- The logging for `PENDING_PET_VISIBLE` remains in place
- The fix ensures the product rule is enforced, which is the correct long-term behavior
- If incident simulation is truly needed, it should be done through a separate mechanism that doesn't violate product rules

**Risk**: Existing tests might rely on the buggy behavior.

**Mitigation**: The existing tests in `test_pet_catalog.py` confirm the correct behavior. We'll add a focused web API test to verify the fix.

## Validation Plan

1. **Unit test**: Add focused regression test in `app/tests/test_cloud_run_app.py` (or new test file) that verifies:
   - `/api/pets` endpoint returns only available pets
   - Nova (pet-103) is excluded from results
   - Scout (pet-101), Mochi (pet-100), and Pip (pet-102) are included

2. **Existing tests**: Run `pytest app/tests/test_pet_catalog.py` to confirm catalog logic remains correct

3. **Manual verification** (if time permits): Start the app and check that the home page shows only available pets
