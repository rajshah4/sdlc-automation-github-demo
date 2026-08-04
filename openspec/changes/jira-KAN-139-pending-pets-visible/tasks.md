# Tasks

- [x] Review Jira issue KAN-139 and extract requirements
- [x] Check wiki documentation at `docs/wiki/petstore-catalog-availability.md`
- [x] Review log evidence at `docs/logs/pending-pet-visible.ndjson`
- [x] Analyze existing `app/petstore_app/catalog.py` implementation
- [x] Review existing tests in `app/tests/test_pet_catalog.py`
- [x] Create OpenSpec-style change folder at `openspec/changes/jira-KAN-139-pending-pets-visible/`
- [x] Write proposal.md with assumptions and scope
- [x] Write specs/catalog-availability/spec.md with requirements
- [x] Write design.md with implementation approach
- [ ] Validate OpenSpec change folder structure
- [ ] Implement catalog.py fix for empty status handling
- [ ] Add regression test for empty status defaulting to available
- [ ] Run test suite to verify fix and ensure no regressions
- [ ] Create feature branch and commit changes
- [ ] Open draft PR with OpenSpec reference and evidence waypoints
- [ ] Add `openhands-review` label to trigger code review automation
- [ ] Post status update to Jira issue KAN-139
