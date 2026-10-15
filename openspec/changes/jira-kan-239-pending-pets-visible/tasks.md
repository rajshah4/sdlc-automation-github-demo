# Tasks

## Implementation

- [x] Create OpenSpec change artifacts (proposal, design, tasks, spec)
- [ ] Validate change artifacts with `validate_open_spec.py`
- [ ] Modify `app/petstore_app/catalog.py` line 41 to default empty status to "available"
- [ ] Add test for empty status string in `app/tests/test_pet_catalog.py`
- [ ] Run tests to verify the fix

## Verification

- [ ] Backend tests pass
- [ ] Manual verification that `search_pets(status="")` returns only available pets

## Human Review

- [ ] Open draft PR with change artifacts and implementation
- [ ] Add `openhands-review` label to trigger code review
- [ ] Code review approval
- [ ] QA verification (if requested by reviewer)
- [ ] Merge approval
