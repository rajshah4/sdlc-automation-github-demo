# Change: Add Regression Tests for Pending Pet Catalog Filtering

## Why

Support reported that customers searching the available pets catalog saw Nova, a pet whose adoption status is pending. Product rules require that the default customer-facing catalog shows only pets with status="available". This change adds explicit regression tests to prevent pending pets from appearing in default search results.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-62
- Trigger: Jira ticket KAN-62
- Automation: SDLC Automation Demo with sidekick-v2 context scouts

## Assumptions

- The current catalog filter implementation in `app/petstore_app/catalog.py` and `app/web/app.js` is correct and properly excludes pending pets
- The bug was either fixed previously or the log represents a temporary condition that has been resolved
- Adding explicit regression tests will prevent this issue from recurring
- The product rule is stable: default searches must exclude pending pets, but explicit `status="pending"` searches should still work for support workflows

## Non-Goals

- Modifying the core filtering logic (it appears to be working correctly)
- Changing the frontend JavaScript implementation (it has Playwright tests that verify the behavior)
- Altering product rules about pending pet visibility
- Adding new features beyond regression test coverage

## What Changes

- Add `test_default_search_excludes_pending_pets()` to verify Nova (pet-103) does not appear in default search
- Add `test_default_dog_search_excludes_pending_dogs()` to verify Nova does not appear when filtering by species=dog
- Both tests explicitly assert that pet-103 (Nova, pending status) is excluded from results
- Tests also verify that all returned pets have status="available"

## Impact

- App behavior: No change to production code, only test additions
- Tests: Two new regression tests added to `app/tests/test_pet_catalog.py`
- Humans: PR requires human review and merge approval

## Human Gates

- Scope approval: Required before implementation (satisfied by ticket creation)
- Review approval: Required before merge
- Merge approval: Required, not automated
- Deployment approval: N/A for test-only changes
