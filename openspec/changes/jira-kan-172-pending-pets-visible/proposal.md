# Change: Prevent Pending Pets from Appearing in Default Catalog Search

## Why

Support reports that some customers are able to see and start adoption flows for pets that should not be available yet. This is confusing customers and creating extra work for operations. The default pet catalog search must return only available pets, but pending pets are leaking through when empty or whitespace-only status values are passed to the search function.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-172
- Trigger: Jira webhook `issue_created`
- Automation: SDLC Automation Demo - Jira issue to PR

## Assumptions

- The bug is caused by the status filtering logic in `catalog.py` that bypasses filtering when `status=""` is passed
- No changes to the Pet data model or external dependencies are needed
- The fix can be implemented by normalizing empty/whitespace status values to "available"
- Existing tests will continue to pass after the fix

## Non-Goals

- Adding new pet statuses beyond "available" and "pending"
- Modifying the UI or API endpoints that call the catalog
- Changing the Pet data structure or adding database persistence
- Adding authentication or authorization checks

## What Changes

- Update `app/petstore_app/catalog.py` to treat empty or whitespace-only status values as "available"
- Add test coverage for edge cases: empty status string, whitespace-only status string
- Ensure pending pets are never returned in default searches

## Impact

- App behavior: Empty or whitespace status values will now correctly filter to only available pets
- Tests: Add new test cases for edge cases previously uncovered
- Humans: Operations will no longer need to handle customer confusion about pending pets appearing in search results

## Human Gates

- Scope approval: Completed - fix is scoped to catalog filtering logic only
- Review approval: Required - awaiting code review
- Merge approval: Required - awaiting human approval
- Deployment approval: Required - awaiting deployment decision
