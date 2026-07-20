# Tasks

- [x] Review Jira ticket KAN-116 and understand the issue.
- [x] Check wiki/docs for availability rules (`docs/wiki/petstore-catalog-availability.md`).
- [x] Check logs for evidence (`docs/logs/pending-pet-visible.ndjson` - error code `PENDING_PET_VISIBLE`).
- [x] Identify the bug in `app/petstore_app/catalog.py` (empty status bypasses filter).
- [x] Create OpenSpec-style change folder at `openspec/changes/jira-KAN-116-pending-pets-visible/`.
- [x] Write proposal, design, and tasks documents.
- [ ] Create spec delta for catalog behavior.
- [ ] Implement the fix: normalize empty status to "available".
- [ ] Add regression test for empty status string.
- [ ] Run focused catalog tests.
- [ ] Run full test suite.
- [ ] Create feature branch and commit changes.
- [ ] Open draft PR with evidence waypoints and human review notes.
- [ ] Add `openhands-qa` label to PR for automated validation.
