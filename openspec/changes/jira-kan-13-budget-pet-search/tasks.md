# Tasks

- [ ] Create OpenSpec-style change artifacts (proposal, spec delta, design, tasks)
- [ ] Validate OpenSpec folder structure with validation script
- [ ] Add `max_adoption_fee_cents` parameter to `search_pets()` in `app/petstore_app/catalog.py`
- [ ] Implement fee filtering logic (pets where `adoption_fee_cents <= max_adoption_fee_cents`)
- [ ] Add validation to reject negative `max_adoption_fee_cents` values
- [ ] Add test: pets within budget are included, pets above budget are excluded
- [ ] Add test: negative fee caps are rejected with ValueError
- [ ] Add test: budget filtering preserves status filtering behavior
- [ ] Run focused validation: `pytest -q app/tests/test_pet_catalog.py`
- [ ] Verify log scenario: $75 budget excludes Scout ($125)
- [ ] Create branch and commit changes
- [ ] Open draft PR against `jira-direct-budget-demo-base`
- [ ] Document assumptions, evidence, and human review requirements in PR
- [ ] Post status comment to Jira KAN-13
