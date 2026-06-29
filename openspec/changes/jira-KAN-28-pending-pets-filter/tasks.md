# Tasks

- [x] Create OpenSpec-style change folder at openspec/changes/jira-KAN-28-pending-pets-filter/
- [x] Document proposal with assumptions, non-goals, and impact
- [x] Write spec delta with requirements and acceptance criteria
- [x] Document design decision and validation plan
- [x] Identify the bug: empty status parameter bypasses filtering
- [x] Reproduce the bug with test case
- [ ] Implement the fix: normalize empty status to "available"
- [ ] Add regression test for empty status parameter
- [ ] Run existing tests to verify no regressions
- [ ] Run new test to verify fix works
- [ ] Create feature branch
- [ ] Commit changes with evidence waypoints
- [ ] Open draft PR with OpenSpec artifacts and validation results
- [ ] Post status to Jira issue KAN-28
- [ ] Add openhands-qa label for QA work cell handoff

## Evidence Waypoints

### Stop 1 - Ticket
- Jira issue KAN-28: "Available pets list still shows unavailable animals"
- Business language: Support hearing from customers about pets that shouldn't be offered
- Key clue: "not available yet" suggests pending status

### Stop 2 - Wiki/Docs
- Checked: `docs/wiki/petstore-catalog-availability.md`
- Found: Default search must show only status="available"
- Found: Nova is pet-103 with status="pending"
- Found: PENDING_PET_VISIBLE is the error code for this regression

### Stop 3 - Logs
- Checked: `docs/logs/pending-pet-visible.ndjson`
- Found: Error code PENDING_PET_VISIBLE
- Found: Component petstore-web, operation web.available_pets
- Found: Pending pet IDs: ["pet-103"]

### Stop 4 - Repo/Files
- Repository: sdlc-automation-github-demo
- Bug location: `app/petstore_app/catalog.py` line 41-42, 50
- Root cause: Empty status parameter bypasses filter due to falsy check
- Fix: Normalize empty status to "available" using `or "available"` pattern

### Stop 5 - Tests/PR
- Tests to add: test_search_pets_excludes_pending_with_empty_status
- Tests to run: app/tests/test_pet_catalog.py
- PR: To be created after implementation
