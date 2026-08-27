# Tasks: Normalize Adopter Email Whitespace

**Change ID:** jira-kan-160-normalize-adopter-email-whitespace

## Implementation Tasks

- [x] Create OpenSpec change artifacts (proposal, design, spec, tasks)
- [ ] Add email normalization line in `create_adoption_order()` function
- [ ] Add focused regression tests for whitespace scenarios
- [ ] Run tests and verify all pass
- [ ] Create draft pull request
- [ ] Add `openhands-review` label to PR

## Test Tasks

- [ ] Test: Valid email with leading whitespace succeeds
- [ ] Test: Valid email with trailing whitespace succeeds
- [ ] Test: Valid email with both-sided whitespace succeeds
- [ ] Test: Whitespace-only input is rejected
- [ ] Test: Existing fee/donation/total behavior unchanged (regression)
- [ ] Test: Existing pending pet rejection unchanged (regression)
- [ ] Test: Existing invalid email rejection unchanged (regression)
- [ ] Test: Existing negative donation rejection unchanged (regression)

## Validation Tasks

- [ ] Run `python3 -m pytest -q app/tests/test_adoptions.py`
- [ ] Verify 8 tests pass (4 existing + 4 new)
- [ ] Verify no regressions in other test files

## Human Gates

**Before implementation:**
- Confirm silent normalization is acceptable (no user notification or logging)
- Confirm `.strip()` whitespace handling is sufficient (space, tab, newline, carriage return)

**Before merge:**
- Human review of code change and tests
- Human approval of PR
- Human-controlled merge to main branch
