# Tasks: Fix Pending Pet Visibility

## Implementation Tasks

- [x] Create OpenSpec change folder
- [x] Write proposal.md with why, what, impact, assumptions, non-goals
- [x] Write design.md with root cause analysis and evidence waypoints
- [ ] Fix filter logic in `app/petstore_app/catalog.py` line 50
- [ ] Add regression test: `test_search_pets_excludes_pending_by_default`
- [ ] Add edge case test: `test_search_pets_with_empty_status_excludes_pending`
- [ ] Run test suite
- [ ] Validate OpenSpec change folder
- [ ] Open draft PR with KAN-55 reference
- [ ] Add openhands-qa label for QA handoff

## Human Gates

- [ ] Code review approval
- [ ] QA validation passes
- [ ] Merge approval
- [ ] Deployment approval (if applicable)

## Acceptance Criteria

From KAN-55:
- ✅ Nova (pet-103, status=pending) must NOT appear in default available-pets search
- ✅ Default search must return only pets with status="available"
- ✅ Explicit pending searches (`status="pending"`) must still work
- ✅ Regression tests prevent this bug from recurring
