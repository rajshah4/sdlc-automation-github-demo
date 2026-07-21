# Tasks

- [x] Create OpenSpec-style change artifacts (proposal, spec, design, tasks).
- [ ] Add `max_adoption_fee_cents` parameter to `search_pets()` in `catalog.py`.
- [ ] Add validation for negative fee values in `search_pets()`.
- [ ] Implement fee filtering logic in `search_pets()`.
- [ ] Add "Max Adoption Fee" input field to `app/web/index.html`.
- [ ] Update `app/web/app.js` to support fee filtering.
- [ ] Add backend test for matching pets at or below maximum fee.
- [ ] Add backend test for excluding pets above maximum fee.
- [ ] Add backend test for rejecting negative maximum fees.
- [ ] Add backend test for optional fee filter (no filter applied when not specified).
- [ ] Run `pytest app/tests/test_pet_catalog.py` to verify all tests pass.
- [ ] Validate OpenSpec-style change folder with validation script.
- [ ] Create draft PR with OpenSpec change link, evidence, and human-review notes.
- [ ] Add `openhands-review` label to PR.
- [ ] Post status comment back to Jira with PR link.
