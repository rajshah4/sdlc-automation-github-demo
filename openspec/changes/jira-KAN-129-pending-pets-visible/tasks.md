# Tasks: Fix Pending Pets Visible in Default Search

## Implementation Tasks

- [x] **Stop 1**: Review Jira issue KAN-129 and understand customer impact
- [x] **Stop 2**: Review wiki documentation at `docs/wiki/petstore-catalog-availability.md`
- [x] **Stop 3**: Review log evidence at `docs/logs/pending-pet-visible.ndjson`
- [x] **Stop 4**: Identify root cause in `app/petstore_app/catalog.py`
- [x] **Stop 5**: Write regression test demonstrating the bug
- [x] Fix status normalization logic in `catalog.py`
- [x] Run all catalog tests to verify fix
- [ ] Create draft pull request
- [ ] Post status update to Jira with PR link

## Human Gates

- [ ] Product owner review of fix approach
- [ ] Code review approval
- [ ] QA validation in test environment
- [ ] Merge approval
- [ ] Deployment authorization

## Validation Plan

1. Run new regression test: `pytest app/tests/test_pet_catalog.py::test_search_pets_defaults_empty_status_to_available -v`
2. Run full catalog test suite: `pytest app/tests/test_pet_catalog.py -v`
3. Manual verification: `python3 -c "from app.petstore_app.catalog import search_pets; print([p.name for p in search_pets(status='')])"` should return only `['Mochi', 'Scout', 'Pip']` (not Nova)

## Success Criteria

- [x] Root cause identified and documented
- [x] Regression test fails before fix, passes after fix
- [x] All existing tests continue to pass
- [x] Manual verification confirms pending pets are not visible with empty status
- [ ] PR created with OpenSpec change link and evidence waypoints
