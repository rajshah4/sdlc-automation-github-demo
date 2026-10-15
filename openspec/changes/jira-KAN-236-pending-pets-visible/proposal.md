# Change: Fix Pending Pets Visible in Available Search

## Why

Customers are seeing and starting adoption flows for pets that should not be available yet. This creates confusion and extra work for operations. The default pet search must return only available pets, but pending pets are leaking through when the status filter is bypassed.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-236
- Trigger: Jira issue created webhook
- Automation: jira-issue-to-pr

## Assumptions

- The bug is in the catalog search filter logic, not in the data or UI layer
- Fixing the status filter enforcement is safe and backward-compatible
- Existing explicit `status="pending"` searches for support workflows must continue working
- No database or deployment changes are required

## Non-Goals

- UI changes or visual updates
- Changes to adoption workflow logic
- Database schema modifications
- Performance optimization
- Additional status types beyond available/pending

## What Changes

- Fix the status filter in `search_pets()` to always enforce the status constraint
- Remove the conditional that allowed status filtering to be bypassed with empty strings
- Add regression test to ensure pending pets never appear in default available searches

## Impact

- App behavior: Default pet searches will correctly exclude pending pets; explicit pending searches continue working
- Tests: Add focused regression test for the fixed behavior
- Humans: Customers will no longer see pets that are not yet available; operations workload reduced

## Human Gates

- Scope approval: Required before merge
- Review approval: Required via openhands-review label
- Merge approval: Required from human reviewer
- Deployment approval: Required before production release
