# Tasks: KAN-64 Pending Pets Fix

## Implementation

- [x] Examine scout results for docs, logs, and repo context
- [x] Verify Nova (pet-103) is marked as pending in both backend and frontend
- [x] Refactor `app/web/app.js` filter to check status first with early return
- [x] Add `test_default_search_excludes_pending_pets()` regression test in `app/tests/test_pet_catalog.py`
- [x] Run backend tests to verify fix
- [ ] Create OpenSpec change artifacts (proposal, design, tasks, spec)
- [ ] Validate OpenSpec artifacts with validation script
- [ ] Commit changes to implementation branch
- [ ] Open pull request with Jira reference
- [ ] Add `openhands-qa` label for automated QA validation

## Validation

- [x] Backend pytest tests pass (6/6 tests including new regression test)
- [ ] UI Playwright tests verify default view excludes Nova
- [ ] QA agent validates the fix in a fresh conversation

## Human Gates

- [ ] Code review approval
- [ ] QA validation pass
- [ ] Merge approval
