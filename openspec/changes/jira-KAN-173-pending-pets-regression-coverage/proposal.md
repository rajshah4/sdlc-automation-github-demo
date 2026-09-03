# Change: Pending Pets Regression Coverage

## Why

Support reports that some customers are able to see and start adoption flows for pets that should not be available yet. This is confusing customers and creating extra work for operations. Log evidence shows a `PENDING_PET_VISIBLE` error indicating pending pets appeared in the available-pets experience. While the current code correctly filters pending pets, missing test coverage leaves the codebase vulnerable to regression.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-173
- Trigger: jira:issue_created
- Automation: sdlc-automation-github-demo Jira webhook integration

## Evidence Waypoints

- **Stop 1 - Ticket**: Jira KAN-173 "Customers are seeing pets that are not available"
- **Stop 2 - Wiki/Docs**: `docs/wiki/petstore-catalog-availability.md` confirms default search must show only `status="available"` pets
- **Stop 3 - Logs**: `docs/logs/pending-pet-visible.ndjson` shows `PENDING_PET_VISIBLE` error for pet-103 (Nova) on 2026-06-29
- **Stop 4 - Repo/Files**: 
  - `app/petstore_app/catalog.py` line 50: status filter logic is correct (`if normalized_status and normalized_status != pet.status`)
  - `app/web/app.js` line 17: frontend filter is correct (`pet.status === "available"`)
  - Pet data line 23: Nova (pet-103) has `status="pending"`
- **Stop 5 - Tests/PR**: Missing explicit regression tests for default search and search-by-name scenarios

## Assumptions

- The current backend and frontend filtering logic is correct and working as intended
- The historical `PENDING_PET_VISIBLE` log represents a past incident that could recur without proper test coverage
- Adding explicit regression tests will prevent reintroduction of the bug
- Nova (pet-103) will remain the designated pending-status demo pet

## Non-Goals

- Changing the catalog search filtering logic (it's already correct)
- Modifying the frontend UI code (it's already correct)
- Adding new pet status types beyond available/pending
- Implementing UI-level testing (focused on backend test coverage)
- Changing deployment or infrastructure

## What Changes

- Add explicit regression test: `test_search_pets_default_excludes_pending_pets()` to verify Nova is excluded from zero-parameter searches
- Add edge case test: `test_search_pets_by_name_excludes_pending_pets()` to verify searching for "nova" returns empty results when using default status filter
- Document the regression coverage in test docstrings referencing KAN-173 and PENDING_PET_VISIBLE

## Impact

- **App behavior**: No changes to application behavior (already correct)
- **Tests**: Two new focused test cases in `app/tests/test_pet_catalog.py` 
- **Humans**: Reviewers should verify tests fail when status filter is incorrectly removed and pass with current implementation

## Human Gates

- **Scope approval**: Reviewer confirms regression test addition is appropriate response to incident
- **Review approval**: Reviewer verifies test coverage addresses the PENDING_PET_VISIBLE scenario
- **Merge approval**: Reviewer approves PR after verifying tests pass
- **Deployment approval**: Standard deployment process (no special deployment concerns)
