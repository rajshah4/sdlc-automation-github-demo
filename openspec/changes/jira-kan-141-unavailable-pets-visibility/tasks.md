# Tasks: Fix unavailable pets visibility

## Implementation Tasks

- [x] Create OpenSpec change folder with proposal, design, spec, and tasks
- [x] Validate the bug exists in `catalog.py` line 50
- [x] Fix status normalization in `catalog.py` to handle empty strings
- [x] Add regression test for empty status parameter
- [x] Run existing unit tests to ensure no regressions
- [ ] Create draft pull request with evidence and validation results
- [ ] Add `openhands-review` label to trigger code review automation

## Validation Plan

1. **Unit Tests**: Run `pytest app/tests/test_pet_catalog.py -v`
   - All existing tests must pass ✅
   - New regression test must pass ✅

2. **Integration**: Verify the fix handles the expected call patterns
   - `search_pets()` - defaults to available ✅
   - `search_pets(status="")` - now correctly returns only available ✅
   - `search_pets(status="available")` - returns available ✅
   - `search_pets(status="pending")` - returns pending (for ops workflows) ✅

3. **UI Test** (if time permits): Run Playwright test to confirm no UI regression
   - `node app/web/tests/catalog-search.playwright.mjs`

## Evidence Checklist

- [x] Issue link: Jira KAN-141
- [x] Docs checked: `docs/wiki/petstore-catalog-availability.md`
- [x] Logs checked: `docs/logs/pending-pet-visible.ndjson`
- [x] Root cause identified: `catalog.py` line 41 (status normalization)
- [x] Tests added: Regression test for empty status
- [x] All unit tests pass (6/6 catalog tests, 4/4 adoption tests)
- [ ] PR link: Will be added after PR creation
