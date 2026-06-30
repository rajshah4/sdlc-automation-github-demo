# Tasks: Fix Pending Pets Visible Bug

## Evidence Waypoints

- [x] Stop 1 - Ticket: Jira KAN-53 reports customers seeing pets that are not available yet
- [x] Stop 2 - Wiki/Docs: Checked `docs/wiki/petstore-catalog-availability.md` - confirms default search must exclude pending pets
- [x] Stop 3 - Logs: Checked `docs/logs/pending-pet-visible.ndjson` - found `PENDING_PET_VISIBLE` error code with `pet-103` (Nova)
- [x] Stop 4 - Repo/Files: Identified bug in `app/petstore_app/catalog.py` line 50 - status filter bypassed when empty string
- [ ] Stop 5 - Tests/PR: Add regression test, run validation, create draft PR

## Implementation Tasks

- [x] Create OpenSpec change folder at `openspec/changes/jira-KAN-53-pending-pets-visible/`
- [x] Write proposal.md
- [x] Write specs/catalog/spec.md
- [x] Write design.md
- [x] Write tasks.md
- [ ] Validate OpenSpec artifacts with `python3 skills/sdlc-story/scripts/validate_open_spec.py`
- [ ] Fix status filter bug in `app/petstore_app/catalog.py`
- [ ] Add regression test in `app/tests/test_pet_catalog.py`
- [ ] Run test suite to verify fix
- [ ] Create feature branch
- [ ] Commit changes
- [ ] Open draft PR with evidence waypoints
- [ ] Add `openhands-qa` label to trigger QA automation
- [ ] Post status to Jira KAN-53

## Acceptance Criteria

- [ ] Default `search_pets()` call returns only available pets (Scout, Mochi, Pip)
- [ ] Default search excludes Nova (pet-103, status=pending)
- [ ] Explicit `search_pets(status="pending")` still returns pending pets
- [ ] All existing tests pass
- [ ] New regression test passes
- [ ] No changes to API contracts or function signatures

## Human Review Gates

- Human must review PR before merge
- Human must approve merge
- Human controls deployment timing
