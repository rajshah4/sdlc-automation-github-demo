# Change: Exclude Pending Pets from Available Catalog

## Why

Customers report seeing animals that should not be adoptable in the available pets list. The catalog must show only available pets by default, never pending ones. This is a regression that violates the core Petstore availability contract.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-37
- Trigger: Jira webhook `jira:issue_created` with label `control-experiment`
- Automation: Jira-to-PR control work cell (sidekick experiment)

## Assumptions

- The bug is in the catalog search status filtering logic, not in data, infrastructure, or deployment configuration.
- Empty or falsy status values should be treated as "available" (the default behavior).
- Explicit `status="pending"` searches must continue to work for support and operations workflows.
- Nova (pet-103) has `status="pending"` and is the test case for this regression.

## Non-Goals

- Cloud infrastructure remediation
- Deployment or environment changes
- Auth, IAM, or secrets changes
- Data persistence or schema changes
- UI redesign beyond what is necessary to verify the fix
- Changes to adoption or other non-catalog behavior

## What Changes

- Fix the status filtering logic in `search_pets()` to always enforce the status default.
- When status is empty or falsy, treat it as "available" rather than bypassing status filtering.
- Add regression tests to prove pending pets never appear in default or available-only searches.

## Impact

- App behavior: Default catalog searches will correctly exclude pending pets. Explicit pending searches remain functional.
- Tests: New regression tests added to prevent future status filter bypass.
- Humans: Requires PR review approval and merge approval before deployment.

## Human Gates

- Scope approval: Required from demo operator or product owner
- Review approval: Required before merge
- Merge approval: Required before deployment
- Deployment approval: Required for production release
