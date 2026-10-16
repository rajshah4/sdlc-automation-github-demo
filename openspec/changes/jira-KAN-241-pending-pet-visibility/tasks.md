# Tasks: Pending Pet Exclusion Test

## Checklist

- [x] Investigate issue and gather evidence
- [x] Read wiki docs (`docs/wiki/petstore-catalog-availability.md`)
- [x] Read log evidence (`docs/logs/pending-pet-visible.ndjson`)
- [x] Review backend code (`app/petstore_app/catalog.py`)
- [x] Review UI code (`app/web/app.js`)
- [x] Review adoption code (`app/petstore_app/adoptions.py`)
- [x] Review existing tests (`app/tests/test_pet_catalog.py`, `app/tests/test_adoptions.py`)
- [x] Create OpenSpec proposal
- [x] Create OpenSpec design
- [ ] Add explicit regression test `test_default_search_excludes_pending_pets` to `app/tests/test_pet_catalog.py`
- [ ] Run test suite to verify new test passes
- [ ] Validate OpenSpec artifacts with `python3 skills/sdlc-story/scripts/validate_open_spec.py`
- [ ] Create feature branch
- [ ] Commit changes
- [ ] Open draft pull request
- [ ] Add `openhands-review` label to PR
- [ ] Post status comment to Jira issue KAN-241

## Test Implementation

File: `app/tests/test_pet_catalog.py`

Location: After line 9 (after `test_search_pets_filters_by_species_and_status`)

Add:
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

## Validation Command

```bash
# Run the specific new test
python -m pytest app/tests/test_pet_catalog.py::test_default_search_excludes_pending_pets -v

# Run all catalog tests
python -m pytest app/tests/test_pet_catalog.py -v

# Validate OpenSpec artifacts
python3 skills/sdlc-story/scripts/validate_open_spec.py openspec/changes/jira-KAN-241-pending-pet-visibility/
```

## Expected Outcome

- New test passes (verifying current correct behavior)
- All existing tests continue to pass
- OpenSpec artifacts validate successfully
- Draft PR is opened with:
  - Clear description linking to Jira KAN-241
  - Evidence waypoints
  - Validation results
  - `openhands-review` label for code review handoff

## Dependencies

None - this is a standalone test addition.

## Rollback Plan

If needed, simply revert the commit adding the test. No production code changes to roll back.
