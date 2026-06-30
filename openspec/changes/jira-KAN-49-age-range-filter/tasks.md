# Tasks

- [x] Create OpenSpec-style change folder at `openspec/changes/jira-KAN-49-age-range-filter/`
- [x] Write `proposal.md` with source, assumptions, non-goals, and human gates
- [x] Write `specs/catalog/spec.md` with acceptance criteria as requirements and scenarios
- [x] Write `design.md` with implementation decisions and validation plan
- [ ] Add `min_age_months` and `max_age_months` parameters to `search_pets()` in `app/petstore_app/catalog.py`
- [ ] Add parameter validation (non-negative, min ≤ max)
- [ ] Add age filtering logic to pet search loop
- [ ] Add test cases for minimum age filtering
- [ ] Add test cases for maximum age filtering
- [ ] Add test cases for combined age range
- [ ] Add test cases for negative age rejection
- [ ] Add test cases for inverted range rejection
- [ ] Add test case for age + status filter interaction
- [ ] Run `python3 -m pytest -q app/tests/test_pet_catalog.py`
- [ ] Document evidence waypoints in PR body
- [ ] Open draft PR with link to this change folder
- [ ] Post summary to Jira issue KAN-49
- [ ] Add `openhands-qa` label to trigger QA automation
