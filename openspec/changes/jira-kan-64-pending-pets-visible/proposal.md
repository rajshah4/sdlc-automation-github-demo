# Change: Fix Pending Pets Appearing in Available Catalog

## Why

Support reports that customers searching the available pets catalog still see Nova, a pet whose adoption status is pending. This violates the product rule that default pet search must return only available pets.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-64
- Trigger: Sidekick v2 demo workflow
- Automation: Jira-to-PR implementation agent with docs, logs, and repo scout context

## Assumptions

- Nova (pet-103) is correctly marked with `status="pending"` in both backend and frontend data
- The backend `search_pets()` function defaults to `status="available"` and filters correctly
- The issue is in the frontend rendering logic where the status filter needs strengthening
- No database schema or API contract changes are needed

## Non-Goals

- Changing how pending pets are stored or represented
- Adding a UI toggle to show/hide pending pets (support workflows already have explicit `status="pending"` queries)
- Modifying the adoption workflow or pending pet validation logic

## What Changes

- Refactor `app/web/app.js` filter to check status first with early return for non-available pets
- Add comprehensive regression test `test_default_search_excludes_pending_pets()` in `app/tests/test_pet_catalog.py`

## Impact

- App behavior: Customers will no longer see pending pets like Nova in the available pets catalog
- Tests: New regression test catches catalog availability violations at the backend level
- Humans: Support tickets about unavailable pets appearing as adoptable will be reduced

## Human Gates

- Scope approval: provided by Jira ticket KAN-64
- Review approval: required before merge
- Merge approval: required by branch protection
- Deployment approval: not needed for this static UI change
