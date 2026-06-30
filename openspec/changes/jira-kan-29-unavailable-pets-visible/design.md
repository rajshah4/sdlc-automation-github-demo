# Design

## Context

The Petstore catalog uses `app/petstore_app/catalog.py::search_pets()` to filter pets by query, species, status, and tag. The function has a default parameter `status="available"`, which should ensure that default searches only return available pets.

However, the current implementation has a logic flaw in the status filter:

```python
if normalized_status and normalized_status != pet.status:
    continue
```

The condition `if normalized_status` evaluates to `False` when `status=""` (empty string), causing the filter to be skipped entirely. This means callers passing an empty string for status will receive all pets regardless of status, violating the availability requirement.

Additionally, the test `test_search_pets_filters_by_species_and_status()` only verifies that species filtering works, relying implicitly on the default status parameter. It doesn't explicitly test the empty-string case that causes the bug.

## Decision

- Change the status filter condition from `if normalized_status` to `if normalized_status != "available"` to ensure default available-only behavior even with empty strings
- Add a regression test that explicitly verifies empty-string status parameters return only available pets
- Add a test that confirms pending pets never appear in default species searches
- Keep the existing test for explicit `status="pending"` searches to ensure operations workflows remain functional

## Risks

- Risk: Changing filter logic could break existing callers that rely on empty-string bypass behavior
  - Mitigation: Review shows no callers intentionally pass empty strings; the default parameter value is the intended API surface
- Risk: Tests might not cover all edge cases
  - Mitigation: Add focused regression tests for the empty-string case and species+default-status combination

## Validation Plan

- Run `python3 -m pytest app/tests/test_pet_catalog.py -v` to verify all catalog tests pass
- Verify new test `test_search_pets_empty_status_excludes_pending()` fails before fix and passes after
- Verify test `test_search_pets_default_status_excludes_pending_from_species_search()` passes with fix
- Ensure existing test `test_search_pets_can_find_pending_pets_when_requested()` still passes
