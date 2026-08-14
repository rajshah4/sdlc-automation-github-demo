# Tasks: KAN-67 Pending Pet Visibility Fix

## Implementation Tasks

- [x] Create OpenSpec change folder structure
- [x] Write proposal.md with scope and assumptions
- [x] Write specs/catalog-availability/spec.md with requirements
- [x] Write design.md with evidence waypoints
- [ ] Add regression test: test_default_search_excludes_pending_nova
- [ ] Add regression test: test_species_search_excludes_pending  
- [ ] Run all catalog tests with pytest
- [ ] Verify tests pass
- [ ] Commit changes to feature branch
- [ ] Open draft PR with evidence and test results
- [ ] Add openhands-qa label to trigger QA automation

## Validation Tasks

- [ ] Backend tests: `uv run pytest app/tests/test_pet_catalog.py -v`
- [ ] Verify 7 total tests pass (5 existing + 2 new)
- [ ] Document test output in PR body

## Human Review Tasks

- [ ] Human reviewer validates test coverage
- [ ] Human reviewer approves PR
- [ ] Human merges to main

## Out of Scope

- UI changes (frontend filter is already correct)
- Backend logic changes (filtering is already correct)
- Schema migrations
- New dependencies
