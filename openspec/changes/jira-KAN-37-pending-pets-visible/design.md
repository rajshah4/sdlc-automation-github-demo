# Design

## Context

The Petstore catalog search function `search_pets()` in `app/petstore_app/catalog.py` filters pets by name, species, status, and tag. The function has a default parameter `status: str = "available"` which should ensure that only available pets are returned when no status is specified.

However, the filtering logic on line 50 has a bug:
```python
if normalized_status and normalized_status != pet.status:
    continue
```

This condition uses short-circuit evaluation. When `normalized_status` is falsy (empty string after `.strip()`), the entire condition evaluates to False, and the status filter is skipped. This allows pending pets to appear in searches where status is explicitly set to an empty string.

The existing test `test_search_pets_filters_by_species_and_status()` passes because it relies on the default parameter value "available", which is truthy and triggers proper filtering. However, if code elsewhere calls `search_pets(status="")`, the filter is bypassed.

## Decision

- Change the status filtering logic from `if normalized_status and normalized_status != pet.status:` to `if normalized_status != pet.status:`
- This ensures that status filtering always happens, even when normalized_status is an empty string.
- Empty strings will be compared against pet.status (which is never empty), causing those pets to be filtered out.
- The default behavior remains unchanged: `status="available"` filters to available pets only.
- Explicit pending searches continue to work: `status="pending"` returns only pending pets.

## Risks

- **Risk:** Changing comparison logic could introduce edge cases with other falsy values (None, etc.)
- **Mitigation:** The function signature specifies `status: str = "available"`, ensuring status is always a string. The `.strip().lower()` transformation on line 41 ensures it's always a normalized string, never None.

- **Risk:** Breaking existing tests or behavior
- **Mitigation:** Run all existing catalog tests to verify no regressions. Add new tests to prove the fix works.

## Validation Plan

- Run existing tests: `python3 -m pytest -q app/tests/test_pet_catalog.py`
- Add new regression test: verify that `search_pets(status="")` excludes pending pets
- Add test: verify that `search_pets()` (no status arg) excludes pending pets explicitly
- Run full test suite: `python3 -m pytest -q app/tests/`
