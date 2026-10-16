# Design: Explicit Pending Pet Exclusion Test

## Context

The Petstore catalog has a core availability rule: default searches return only `status="available"` pets. The backend (`catalog.py`), UI (`app.js`), and adoption validation (`adoptions.py`) all implement this correctly.

However, the test coverage for this rule is implicit rather than explicit. The test `test_search_pets_filters_by_species_and_status` verifies that `search_pets(species="dog")` returns only Scout (pet-101), which implicitly excludes Nova (pet-103, pending), but it doesn't directly assert the pending-pet-exclusion behavior.

## Problem

Historical logs show a `PENDING_PET_VISIBLE` error occurred, indicating pending pets were visible to customers. While the current code is correct, the implicit test coverage makes it easier for future changes to accidentally break this rule without immediately failing tests.

## Solution

Add an explicit regression test that:
1. Calls `search_pets()` with no status override (using the default `status="available"`)
2. Explicitly asserts that pending pets (specifically pet-103/Nova) are NOT in the results
3. Explicitly asserts that only available pets (pet-100, pet-101, pet-102) are returned
4. Names the test to clearly document what rule it enforces: `test_default_search_excludes_pending_pets`

## Implementation Details

### File: `app/tests/test_pet_catalog.py`

Add new test function after the existing `test_search_pets_filters_by_species_and_status`:

```python
def test_default_search_excludes_pending_pets() -> None:
    """Regression test: pending pets must not appear in default available-only search."""
    results = search_pets()
    result_ids = [pet.id for pet in results]
    
    # Explicitly verify Nova (pet-103, pending) is excluded
    assert "pet-103" not in result_ids, "Pending pet Nova (pet-103) must not appear in default search"
    
    # Verify only available pets are returned
    assert set(result_ids) == {"pet-100", "pet-101", "pet-102"}, \
        "Default search must return only available pets"
```

### Rationale

- **Explicit assertion**: Directly tests that `pet-103` (Nova, pending) is excluded
- **Self-documenting**: Test name and docstring clearly state the rule being enforced
- **Regression prevention**: Future changes that break this rule will immediately fail this test
- **Complements existing tests**: Works alongside `test_search_pets_can_find_pending_pets_when_requested` which verifies explicit pending searches DO work

## Alternatives Considered

1. **Modify existing test**: Could add assertions to `test_search_pets_filters_by_species_and_status`
   - **Rejected**: That test focuses on species filtering; better to have separate focused tests
   
2. **Add only negative assertion**: Could only assert `"pet-103" not in result_ids`
   - **Rejected**: Also asserting the complete set of expected IDs makes the test more robust

3. **Add comment to existing test**: Could add comment explaining implicit behavior
   - **Rejected**: Explicit test is stronger than documentation

## Decision

- Add explicit regression test `test_default_search_excludes_pending_pets` to verify pending pets are excluded from default search
- Test will explicitly assert that pet-103 (Nova, pending) is NOT in default `search_pets()` results
- Test will explicitly assert that only available pets (pet-100, pet-101, pet-102) are returned
- No production code changes - code is already correct, only test coverage gap needs to be filled

## Risks

- **None**: This is a test-only change with no production code modifications
- The test verifies existing correct behavior and prevents future regressions
- No risk of breaking support/operations workflows that explicitly request pending pets

## Validation Plan

- Run the new test in isolation: `python -m pytest app/tests/test_pet_catalog.py::test_default_search_excludes_pending_pets -v`
- Run all catalog tests: `python -m pytest app/tests/test_pet_catalog.py -v`
- Run all adoption tests: `python -m pytest app/tests/test_adoptions.py -v`
- Verify OpenSpec artifacts: `python3 skills/sdlc-story/scripts/validate_open_spec.py openspec/changes/jira-KAN-241-pending-pet-visibility/`
- Expected: All tests pass, confirming current behavior is correct and will be protected going forward
