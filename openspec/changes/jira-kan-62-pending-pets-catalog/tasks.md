# Tasks: KAN-62 Pending Pet Regression Tests

## Prerequisites

- [x] Review ticket KAN-62
- [x] Review docs-scout results from conversation ebfc96522ac94ceaa16301a24d0e144c
- [x] Review logs-scout results from conversation b3614de4f9424f25be7a4b83ad517ed5
- [x] Review repo-scout results from conversation f3dbc00ff7514b27b2b48aca061388f2
- [x] Verify product rule in `docs/wiki/petstore-catalog-availability.md`
- [x] Verify error log in `docs/logs/pending-pet-visible.ndjson`
- [x] Inspect `app/petstore_app/catalog.py` filter implementation
- [x] Inspect `app/tests/test_pet_catalog.py` existing test coverage
- [x] Verify Playwright tests in `app/web/tests/catalog-search.playwright.mjs`

## Implementation

- [x] Create implementation branch `fix/kan-62-pending-pets-in-catalog`
- [x] Create OpenSpec change folder `openspec/changes/jira-kan-62-pending-pets-catalog/`
- [x] Write `proposal.md`
- [x] Write `specs/catalog-availability/spec.md`
- [x] Write `design.md`
- [x] Write `tasks.md`
- [x] Add `test_default_search_excludes_pending_pets()` to `app/tests/test_pet_catalog.py`
- [x] Add `test_default_dog_search_excludes_pending_dogs()` to `app/tests/test_pet_catalog.py`
- [x] Run pytest to verify all tests pass
- [ ] Validate OpenSpec change folder structure
- [ ] Commit changes with Jira key in commit message
- [ ] Push branch to origin
- [ ] Open GitHub pull request
- [ ] Add `openhands-qa` label to PR

## Validation

- [x] Run `pytest app/tests/test_pet_catalog.py -v` → 7 tests passed
- [ ] Validate with `python3 skills/sdlc-story/scripts/validate_open_spec.py openspec/changes/jira-kan-62-pending-pets-catalog`

## Human Gates

- [ ] Human review of PR
- [ ] Human approval to merge
- [ ] Human merge to main

## Success Criteria

- All existing tests continue to pass
- Two new regression tests pass
- Tests explicitly verify pet-103 (Nova) exclusion
- OpenSpec change documentation is complete and valid
- PR includes evidence waypoints
- PR references KAN-62
