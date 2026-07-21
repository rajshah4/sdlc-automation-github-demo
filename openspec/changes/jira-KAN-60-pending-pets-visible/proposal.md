# Change: Add regression tests for pending pet visibility

## Why

Support reported that Nova (a pending pet) appeared in the available pets list. While the current code correctly filters by status="available", there is insufficient test coverage to prevent this regression from recurring.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-60
- Trigger: Jira ticket created
- Automation: SDLC sidekick demo

## Assumptions

- The current catalog filtering logic is correct (verified by manual testing)
- The bug was a past regression that has been fixed
- The primary gap is missing regression test coverage
- Pet-103 (Nova) has status="pending" and must not appear in default available pet searches

## Non-Goals

- Changing the catalog filtering logic (it works correctly)
- Modifying UI behavior beyond adding test coverage
- Adding new pet statuses or workflow states
- Changing adoption workflow

## What Changes

- Add comprehensive regression tests for default catalog behavior
- Add explicit test that pending pets (including Nova) are excluded from default search
- Add test for no-filter search to ensure only available pets are returned
- Document test coverage in OpenSpec artifacts

## Impact

- App behavior: No change to runtime behavior
- Tests: New regression tests added to prevent PENDING_PET_VISIBLE errors
- Humans: PR reviewers should verify tests cover the documented regression

## Human Gates

- Scope approval: Required before implementation
- Review approval: Required before merge
- Merge approval: Required by repo owner
- Deployment approval: No deployment changes required
