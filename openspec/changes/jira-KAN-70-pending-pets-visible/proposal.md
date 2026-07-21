# Change: Fix Pending Pets Visibility in Default Catalog Search

## Why

Customers are seeing pets with `status="pending"` in the default available-pets experience. This violates the product rule that default catalog searches must show only available pets. Pending pets should only appear when explicitly requested by support or operations workflows.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-70
- Trigger: Jira issue created (jira:issue_created)
- Automation: Jira-to-PR work cell

## Assumptions

- The bug is in the catalog search filter logic when status is an empty string or not properly validated
- Explicit requests for `status="pending"` should continue to work for support workflows
- The fix requires only catalog filter logic changes, no schema or UI changes

## Non-Goals

- Changing the pending pet workflow or status values
- Adding new pet status types
- Modifying adoption flows or operations tools
- UI changes beyond what's needed for correct filtering

## What Changes

- Fix `search_pets()` in `app/petstore_app/catalog.py` to enforce available-only default when status is empty or not specified
- Add regression test to verify pending pets are excluded from default search
- Add test to verify empty status string defaults to available-only behavior

## Impact

- App behavior: Default catalog searches will correctly exclude pending pets
- Tests: New focused regression tests added
- Humans: Support reports of pending pets in customer experience should stop

## Human Gates

- Scope approval: Awaiting human confirmation this fix addresses the reported issue
- Review approval: Human code review required before merge
- Merge approval: Human approval required
- Deployment approval: Human approval required for production deployment
