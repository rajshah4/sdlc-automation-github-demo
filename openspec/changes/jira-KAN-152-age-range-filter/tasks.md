# Tasks: Age Range Filter Implementation

## Evidence Waypoints

- [x] Stop 1 - Ticket: Jira KAN-152 "Customers cannot filter pets by age range"
- [x] Stop 2 - Wiki/Docs: Checked `docs/wiki/petstore-catalog-availability.md` - confirms default status="available" behavior must be preserved
- [x] Stop 3 - Logs: No log evidence for this feature request (feature, not a bug)
- [x] Stop 4 - Repo/Files: Located `app/petstore_app/catalog.py` and `app/tests/test_pet_catalog.py`
- [ ] Stop 5 - Tests/PR: Tests to be added and run, PR to be created

## Implementation Tasks

- [ ] Add `min_age_months` and `max_age_months` parameters to `search_pets()` signature
- [ ] Add validation for negative age values
- [ ] Add validation for inverted ranges (min > max)
- [ ] Add age filtering logic after existing filters
- [ ] Add test for minimum age filter
- [ ] Add test for maximum age filter
- [ ] Add test for combined age range
- [ ] Add test for age filter with other filters (species)
- [ ] Add parametrized test for negative age validation
- [ ] Add test for inverted range validation
- [ ] Run existing tests to ensure no regressions
- [ ] Run new tests to verify feature works
- [ ] Create feature branch
- [ ] Commit changes with clear message
- [ ] Push branch to remote
- [ ] Create draft PR with OpenSpec reference
- [ ] Add `openhands-review` label to PR

## Validation Plan

1. Run existing tests: `python3 -m pytest -q app/tests/test_pet_catalog.py`
2. Verify all existing tests still pass (no regressions)
3. Verify new age filtering tests pass
4. Confirm backwards compatibility (existing callers work)

## Success Criteria

✓ All existing tests pass (no regressions)
✓ All new tests pass (feature works correctly)
✓ Validation prevents negative ages and inverted ranges
✓ Age filtering works standalone and with other filters
✓ Default status="available" behavior preserved
✓ Draft PR created with clear documentation
✓ Code review triggered via label
