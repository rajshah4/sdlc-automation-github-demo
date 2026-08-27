# Tasks

- [x] Create OpenSpec-style change folder at `openspec/changes/jira-KAN-153-pet-age-filter/`
- [x] Write proposal.md with why, assumptions, non-goals, and human gates
- [x] Write specs/pet-catalog/spec.md with ADDED requirements and scenarios
- [x] Write design.md with context, decisions, risks, and validation plan
- [ ] Validate OpenSpec change artifacts with validation script
- [ ] Update `app/petstore_app/catalog.py` to add age filtering parameters and logic
- [ ] Add validation for age parameters (non-negative, valid range)
- [ ] Update `app/tests/test_pet_catalog.py` with comprehensive age filter tests
- [ ] Run existing tests to ensure no regression
- [ ] Run new tests to verify age filtering works correctly
- [ ] Create feature branch and commit changes
- [ ] Open draft PR with OpenSpec change link and evidence waypoints
- [ ] Add `openhands-review` label to trigger code review work cell
- [ ] Post status update to Jira with PR link and validation results

## Evidence Waypoints

- **Stop 1 - Ticket**: Jira KAN-153 "Customers cannot filter pets by age range"
- **Stop 2 - Wiki/Docs**: Checked `skills/sdlc-story/references/petstore-implementation-map.md` - found explicit Age Range Filter implementation guidance
- **Stop 3 - Logs**: No log evidence required for this feature addition
- **Stop 4 - Repo/Files**: `app/petstore_app/catalog.py` (search_pets function), `app/tests/test_pet_catalog.py` (test coverage)
- **Stop 5 - Tests/PR**: Tests added for all scenarios, validation passed, draft PR opened
