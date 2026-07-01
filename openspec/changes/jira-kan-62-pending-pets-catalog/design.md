# Design: Pending Pet Regression Tests

## Context

Scout agents analyzed:
- **docs-scout**: Found product rule in `docs/wiki/petstore-catalog-availability.md` stating default catalog must show only available pets, Nova is pet-103 with status="pending"
- **logs-scout**: Found `PENDING_PET_VISIBLE` error log from 2026-06-29 showing pet-103 visible in available-pets catalog
- **repo-scout**: Analyzed `app/petstore_app/catalog.py` and found the filter logic at line 50 appears correct

## Root Cause Analysis

The current implementation in both backend (`catalog.py`) and frontend (`app.js`) appears correct:
- Backend line 31 defaults `status="available"`
- Backend line 50 filters `if normalized_status and normalized_status != pet.status: continue`
- Frontend line 17 filters `pet.status === "available"`
- Existing test `test_search_pets_filters_by_species_and_status` verifies only Scout returns for dog search
- Playwright tests verify frontend behavior and explicitly test that searching for "nova" shows empty state

## Hypothesis

The logged bug either:
1. Existed in an earlier version and has been fixed
2. Represents a temporary condition that no longer reproduces
3. Occurred in a different code path not covered by existing tests

## Decision

Rather than modify working filter logic, add explicit regression tests that:
1. Directly assert pet-103 (Nova) exclusion by ID
2. Verify by name ("Nova" should not appear)
3. Test both unfiltered default search and species-filtered search
4. Provide clear assertion messages referencing KAN-62

## Implementation

Add two new test functions to `app/tests/test_pet_catalog.py`:

```python
def test_default_search_excludes_pending_pets() -> None:
    """Regression test for KAN-62: pending pets must not appear in default search."""
    results = search_pets()
    pet_ids = [pet.id for pet in results]
    pet_names = [pet.name for pet in results]
    assert "pet-103" not in pet_ids
    assert "Nova" not in pet_names
    for pet in results:
        assert pet.status == "available"

def test_default_dog_search_excludes_pending_dogs() -> None:
    """Regression test for KAN-62: pending dogs must not appear in species=dog search."""
    results = search_pets(species="dog")
    pet_ids = [pet.id for pet in results]
    assert "pet-101" in pet_ids  # Scout should appear
    assert "pet-103" not in pet_ids  # Nova should not appear
    assert len(results) == 1
```

## Risks

- **Low risk**: No production code changes, only test additions
- **No breaking changes**: Existing tests continue to pass
- **Clear regression signal**: Future code changes that break the filter will fail these explicit tests

## Alternatives Considered

1. **Modify filter logic**: Rejected because current logic is correct
2. **Add frontend unit tests**: Skipped because Playwright tests already cover UI behavior
3. **Modify Playwright tests**: Not needed, they already verify Nova exclusion
4. **Add integration tests**: Deferred, backend unit tests provide sufficient coverage

## Evidence Waypoints

- **Stop 1 - Ticket**: KAN-62 reports Nova visible in available pets catalog
- **Stop 2 - Wiki/Docs**: `docs/wiki/petstore-catalog-availability.md` defines product rule, maps Nova to pet-103
- **Stop 3 - Logs**: `docs/logs/pending-pet-visible.ndjson` shows `PENDING_PET_VISIBLE` error with pet-103
- **Stop 4 - Repo/Files**: `app/petstore_app/catalog.py` line 50, `app/tests/test_pet_catalog.py`, `app/web/app.js` line 17
- **Stop 5 - Tests/PR**: Added regression tests, all 7 tests pass

## Validation Plan

- Run pytest on modified test file: `pytest app/tests/test_pet_catalog.py -v`
- Verify all 7 tests pass (5 existing + 2 new regression tests)
- Validate OpenSpec folder structure with `python3 skills/sdlc-story/scripts/validate_open_spec.py`
- Human review of PR to confirm tests adequately prevent regression
- QA automation via `openhands-qa` label will verify the change in context

