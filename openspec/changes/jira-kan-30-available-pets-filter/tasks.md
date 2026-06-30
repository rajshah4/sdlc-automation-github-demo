# Tasks: Fix Available Pets Catalog Filter

## Implementation Checklist

- [x] Create OpenSpec change folder and artifacts
- [x] Document evidence waypoints (ticket, wiki, logs, repo files)
- [x] Fix catalog filter logic in `app/petstore_app/catalog.py`
- [x] Add regression test `test_search_pets_excludes_pending_by_default`
- [x] Run test suite to verify fix
- [x] Validate OpenSpec artifacts
- [ ] Create PR with evidence and human gates
- [ ] Add `openhands-qa` label to trigger QA work cell
- [ ] Post summary to Jira KAN-30

## Human Gates

- [ ] **Code Review**: Human reviewer must approve the logic change
- [ ] **QA Validation**: QA work cell must verify the fix works as expected
- [ ] **Merge Approval**: Human must approve and merge the PR
- [ ] **Deployment Decision**: Human must decide when/if to deploy to production

## Evidence Checklist

- [x] Stop 1 - Ticket: Jira KAN-30 captured
- [x] Stop 2 - Wiki/Docs: `docs/wiki/petstore-catalog-availability.md` checked
- [x] Stop 3 - Logs: `docs/logs/pending-pet-visible.ndjson` with `PENDING_PET_VISIBLE` error found
- [x] Stop 4 - Repo/Files: Implementation complete in catalog.py
- [x] Stop 5 - Tests/PR: Tests passing, PR ready to create
