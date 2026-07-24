# Tasks: Fix Pending Pets Visible in Default Search

## Implementation Tasks

- [x] Create OpenSpec change folder and artifacts
- [ ] Modify `app/petstore_app/catalog.py` line 41 to default empty status to "available"
- [ ] Add regression test for empty status handling
- [ ] Add edge case test for whitespace status handling
- [ ] Run test suite and verify all tests pass
- [ ] Create draft pull request with evidence waypoints

## Validation Tasks

- [ ] Verify pending pets (pet-103/Nova) excluded from `search_pets(species="dog", status="")`
- [ ] Verify pending pets still findable with explicit `search_pets(status="pending")`
- [ ] Verify all existing tests pass
- [ ] Verify new regression tests pass

## Human Gates

- [ ] **Code Review Required:** Human reviewer must approve the fix
- [ ] **QA Validation Required:** Independent testing must confirm pending pets no longer appear in default search
- [ ] **Merge Approval Required:** Human must approve merge to main
- [ ] **Deployment Approval Required:** Human must approve production deployment

## Evidence Checklist

- [x] Stop 1 - Ticket: Jira KAN-126 reviewed
- [x] Stop 2 - Wiki/Docs: `docs/wiki/petstore-catalog-availability.md` checked
- [x] Stop 3 - Logs: `docs/logs/pending-pet-visible.ndjson` analyzed
- [x] Stop 4 - Repo/Files: `app/petstore_app/catalog.py` root cause identified
- [ ] Stop 5 - Tests/PR: Tests written, validation run, PR created
