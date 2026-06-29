# Design

## Context

The Petstore catalog stores pet availability in the `status` field. Per `docs/wiki/petstore-catalog-availability.md`, default customer-facing search must return only `status="available"` pets. Support and operations workflows may explicitly request `status="pending"` pets when needed.

The current `visible_pets()` function in `cloud_run_app.py` has a conditional that returns ALL pets (including pending ones) when the system is in `INCIDENT_MODE`. This was likely intended for demo/SRE simulation purposes, but it violates the core catalog availability rule.

## Decision

- Fix `visible_pets()` in `cloud_run_app.py` to always filter to `status="available"` pets.
- Remove the incident mode bypass logic (lines 93-94) that returns unfiltered pets.
- Preserve the incident detection and logging infrastructure for observability purposes.
- Update test expectations to reflect correct filtering behavior.
- Preserve explicit `status="pending"` searches in the `search_pets()` API function (already working correctly).

## Implementation

### Before (lines 92-95 in cloud_run_app.py):
```python
def visible_pets() -> list[Pet]:
    if current_mode() == INCIDENT_MODE:
        return list(PETS)  # BUG: Returns ALL pets including pending
    return [pet for pet in PETS if pet.status == "available"]
```

### After:
```python
def visible_pets() -> list[Pet]:
    return [pet for pet in PETS if pet.status == "available"]
```

This is the smallest safe fix: remove the conditional bypass and always apply the correct filter.

## Risks

- **Low risk**: The change makes the catalog filter unconditionally correct. The incident mode infrastructure (health checks, logging, banners) remains functional for observability.
- **Test impact**: `test_bad_catalog_filter_exposes_pending_pet` will need updating because it currently expects the broken behavior. The test name suggests it's testing the incident simulation, not production behavior.
- **No impact** to explicit pending-pet searches via the `search_pets()` API function, which already works correctly.

## Validation Plan

1. Run `pytest app/tests/test_cloud_run_app.py::test_visible_pets_excludes_pending_by_default -v` to confirm default behavior stays correct.
2. Update and run `test_bad_catalog_filter_exposes_pending_pet` to reflect corrected expectations.
3. Run `pytest app/tests/test_pet_catalog.py -v` to confirm catalog API behavior is unaffected.
4. Run full test suite: `pytest app/tests/ -v`
5. Verify no Nova (pet-103) appears in default catalog results.
