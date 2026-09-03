# Design

## Context

The Petstore catalog search function (`app/petstore_app/catalog.py:search_pets()`) has a default parameter `status="available"` (line 31) and filtering logic at line 50 that correctly excludes pets whose status doesn't match the requested status.

Current behavior verification:
- ✅ `search_pets()` returns 3 pets (pet-100, pet-101, pet-102) - Nova excluded
- ✅ `search_pets(species="dog")` returns only Scout (pet-101) - Nova excluded
- ✅ `search_pets(query="nova")` returns empty list - Nova excluded
- ✅ `search_pets(query="nova", status="pending")` finds Nova - explicit pending access works

The product requirement from `docs/wiki/petstore-catalog-availability.md`:
> Default customer-facing catalog search must show only pets with `status="available"`. Support and operations workflows may explicitly request `status="pending"` when investigating a case, but pending pets must not appear in the default available-pets experience.

## Decision

**Add focused regression test coverage without changing application code**

The filtering logic is correct and working. The gap is test coverage that explicitly validates the PENDING_PET_VISIBLE regression cannot be reintroduced. We will:

1. **Add `test_search_pets_default_excludes_pending_pets()`**: Validates that a zero-parameter `search_pets()` call returns exactly 3 available pets and excludes Nova (pet-103)

2. **Add `test_search_pets_by_name_excludes_pending_pets()`**: Validates that searching for "nova" with default status returns empty results, proving customers cannot discover pending pets by name search

3. **Reference KAN-173 and PENDING_PET_VISIBLE in test docstrings**: Makes the regression context discoverable for future maintainers

## Risks and Mitigations

**Risk**: Tests could become brittle if pet fixture data changes
- **Mitigation**: Tests reference specific pet IDs (pet-103) and check for presence/absence, not exact counts in all cases

**Risk**: Adding tests without changing code might seem redundant to reviewers
- **Mitigation**: PR description explains the regression coverage gap and links to log evidence from docs/logs/pending-pet-visible.ndjson

**Risk**: Tests might pass even if the bug is reintroduced (false negative)
- **Mitigation**: Tests explicitly check Nova (pet-103) is absent and use assertions that would fail if status filtering is removed

## Validation Plan

1. Run new tests individually to confirm they pass:
   ```bash
   cd /workspace/project/sdlc-automation-github-demo
   python3 -m pytest app/tests/test_pet_catalog.py::test_search_pets_default_excludes_pending_pets -v
   python3 -m pytest app/tests/test_pet_catalog.py::test_search_pets_by_name_excludes_pending_pets -v
   ```

2. Run full catalog test suite to ensure no regressions:
   ```bash
   python3 -m pytest app/tests/test_pet_catalog.py -v
   ```

3. Manual verification that breaking the filter causes tests to fail:
   - Temporarily comment out line 50-51 in `catalog.py` (the status filter)
   - Verify new tests fail
   - Restore the filter
   - Verify tests pass again
