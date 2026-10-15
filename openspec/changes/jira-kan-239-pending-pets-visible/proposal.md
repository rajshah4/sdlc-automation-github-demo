# Change: Prevent Pending Pets from Appearing in Default Search

## Why

Support reports that customers are seeing pets with "pending" status in the available-pets experience. According to product rules and the wiki documentation, only pets with "available" status should appear in default customer-facing searches. Pending pets should only be visible when explicitly requested by support or operations staff.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-239
- Trigger: Jira webhook (issue created)
- Automation: jira-issue-to-pr

## Assumptions

- The bug is in the backend `search_pets` function, which allows bypassing the status filter when an empty status string is passed.
- The frontend UI correctly filters by status and is not the source of the bug.
- The fix should ensure that the default "available" status filter is always applied unless explicitly overridden with a valid status value.

## Non-Goals

- Changing the UI implementation or adding new UI features.
- Modifying the adoption flow logic (it already correctly prevents adopting non-available pets).
- Adding new pet statuses or status validation beyond the fix.

## What Changes

- The `search_pets` function in `app/petstore_app/catalog.py` will be modified to ensure that an empty status string defaults to "available" instead of bypassing the status filter.
- A new test will be added to verify that passing an empty status string returns only available pets.

## Impact

- App behavior: Customers will no longer see pending pets in default searches, even if the backend receives an empty status parameter.
- Tests: New test added to verify the fix. Existing tests continue to pass.
- Humans: This fix requires code review and QA approval before merging. No customer-facing breaking changes.

## Human Gates

- Scope approval: Automated (Jira webhook trigger)
- Review approval: Required (openhands-review label will be added to PR)
- QA approval: Required (reviewer will determine if openhands-qa is needed)
- Merge approval: Required (human must approve and merge the PR)
