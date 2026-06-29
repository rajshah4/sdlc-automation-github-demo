# Tasks

- [x] Gather evidence from Jira ticket (Stop 1)
- [x] Search wiki/docs for product rules (Stop 2)
- [x] Search logs for error evidence (Stop 3)
- [x] Identify root cause in repo/files (Stop 4)
- [x] Create OpenSpec-style change artifacts
- [ ] Implement fix in `cloud_run_app.py` `visible_pets()` function
- [ ] Update `test_bad_catalog_filter_exposes_pending_pet` test expectations
- [ ] Run focused validation on cloud_run_app tests
- [ ] Run catalog tests to ensure no regression
- [ ] Run full test suite
- [ ] Create feature branch and commit changes
- [ ] Open draft PR with evidence and context
- [ ] Post Jira comment with Stop 5 summary and PR link

## Implementation Checklist

### Code Changes
- [ ] Remove incident mode conditional from `visible_pets()` function
- [ ] Ensure function always returns `[pet for pet in PETS if pet.status == "available"]`

### Test Changes
- [ ] Update `test_bad_catalog_filter_exposes_pending_pet` to expect Nova excluded from results
- [ ] Verify `test_visible_pets_excludes_pending_by_default` still passes
- [ ] Confirm `test_search_pets_can_find_pending_pets_when_requested` still works (explicit searches)

### Validation
- [ ] Run `pytest app/tests/test_cloud_run_app.py -v`
- [ ] Run `pytest app/tests/test_pet_catalog.py -v`
- [ ] Run `pytest app/tests/ -v` (full suite)

### Documentation
- [ ] PR description includes all evidence waypoints
- [ ] PR links to OpenSpec change folder
- [ ] PR includes assumptions, acceptance criteria, and human gates
- [ ] Jira comment summarizes evidence, changes, tests, and PR link
