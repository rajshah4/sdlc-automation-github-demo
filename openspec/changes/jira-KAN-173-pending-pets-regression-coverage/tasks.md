# Tasks

- [x] Read Jira issue KAN-173 and understand customer impact
- [x] Check wiki docs (`docs/wiki/petstore-catalog-availability.md`) for product requirements
- [x] Review log evidence (`docs/logs/pending-pet-visible.ndjson`) for PENDING_PET_VISIBLE error
- [x] Investigate catalog.py and app.js filtering logic - confirmed both are correct
- [x] Verify current behavior with manual testing - Nova correctly excluded from default searches
- [x] Identify test coverage gap - missing explicit regression tests for default and name-based searches
- [x] Create OpenSpec-style change artifacts in `openspec/changes/jira-KAN-173-pending-pets-regression-coverage/`
- [x] Validate change folder structure with `scripts/validate_open_spec.py`
- [ ] Add `test_search_pets_default_excludes_pending_pets()` to `app/tests/test_pet_catalog.py`
- [ ] Add `test_search_pets_by_name_excludes_pending_pets()` to `app/tests/test_pet_catalog.py`
- [ ] Run new tests to verify they pass
- [ ] Run full test suite to ensure no regressions
- [ ] Create implementation branch
- [ ] Open draft pull request with evidence waypoints and OpenSpec change reference
- [ ] Add `openhands-review` label to trigger code review automation
