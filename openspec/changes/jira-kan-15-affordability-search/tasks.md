# Tasks

## OpenSpec Artifacts
- [x] Create `openspec/changes/jira-kan-15-affordability-search/` folder
- [x] Write proposal.md with business requirement interpretation
- [x] Write design.md with implementation approach
- [x] Write tasks.md checklist
- [ ] Write specs/petstore-catalog/spec.md with acceptance criteria
- [ ] Validate OpenSpec artifacts with `scripts/validate_open_spec.py`

## Implementation
- [ ] Add `max_adoption_fee_cents` parameter to `search_pets()` in `app/petstore_app/catalog.py`
- [ ] Add non-negative validation for the fee parameter
- [ ] Add filter logic to exclude pets above the maximum fee

## Testing
- [ ] Add `test_search_pets_filters_by_max_adoption_fee` for basic fee filtering
- [ ] Add `test_search_pets_combines_fee_cap_with_existing_filters` for filter combinations
- [ ] Add `test_search_pets_rejects_negative_max_adoption_fee` for validation
- [ ] Run focused catalog tests: `pytest app/tests/test_pet_catalog.py -v`
- [ ] Run full test suite: `pytest app/tests/ -v`

## Documentation & PR
- [ ] Create feature branch from current state
- [ ] Commit OpenSpec artifacts and implementation
- [ ] Open draft PR with:
  - Link to OpenSpec change folder
  - Link to Jira issue KAN-15
  - Assumptions and interpretation of business language
  - Test results
  - Files changed summary
- [ ] Post Jira comment with PR link and evidence

## Human Gates
- [ ] Human review: Does the interpretation match product intent?
- [ ] Human review: Are the test scenarios sufficient?
- [ ] Human review: Is the implementation the smallest safe change?
- [ ] Human approval: Ready to merge?
