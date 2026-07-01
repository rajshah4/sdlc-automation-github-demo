# Tasks: KAN-60 Pending Pet Visibility Tests

## Implementation Tasks

- [x] Create OpenSpec change folder
- [x] Write proposal.md
- [x] Write design.md
- [x] Write spec delta
- [ ] Add test_default_search_excludes_pending_pets
- [ ] Add test_nova_excluded_from_default_search
- [ ] Add test_all_available_pets_included_by_default
- [ ] Run test suite and verify all tests pass
- [ ] Create implementation branch
- [ ] Commit changes
- [ ] Open PR with evidence waypoints
- [ ] Add openhands-qa label to PR

## Validation

- Run: `pytest app/tests/test_pet_catalog.py -v`
- Expected: All tests pass, including 3 new regression tests
- Verify: Nova (pet-103) is explicitly tested as excluded

## Human Review Gates

- PR opened for human review
- Tests demonstrate proper coverage
- No production code changes required
