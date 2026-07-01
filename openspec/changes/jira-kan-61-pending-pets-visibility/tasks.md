# Tasks: Pending Pets Visibility Fix

## Implementation Tasks

- [x] Analyze ticket and scout results from docs, logs, and repo scouts
- [x] Verify backend catalog filter logic is correct
- [x] Verify frontend UI filter logic is correct  
- [x] Add regression test `test_default_search_excludes_pending_pets()`
- [x] Run backend tests to verify fix
- [x] Create OpenSpec change artifacts
- [ ] Open GitHub pull request with KAN-61 reference
- [ ] Add openhands-qa label for QA automation
- [ ] Human review and approval

## Validation Plan

### Backend Tests
```bash
cd /workspace/project/sdlc-automation-github-demo
python3 -m pytest app/tests/test_pet_catalog.py -v
```

Expected: All 6 tests pass, including new `test_default_search_excludes_pending_pets`

### Frontend Tests (Optional)
The existing Playwright test at `app/web/tests/catalog-search.playwright.mjs` already validates:
- Line 154: Default view shows only Mochi, Scout, Pip (excludes Nova)
- Line 171-176: Searching for "nova" shows empty state

## Human Gates

- **PR Review**: Human must review test coverage and approve merge
- **Merge Decision**: Human must merge to main after review
- **Deployment**: Human controls when changes go to production

## Residual Risks

- **Low**: Test-only change with no behavior modification
- **Monitoring**: The `PENDING_PET_VISIBLE` error code in test assertions matches the observability pattern from logs
