# Change: Fix Pending Pets Visible in Available Catalog

## Why

Customers are seeing pets that should not be available yet. Support reports indicate pending pets appear in the available-pets catalog experience, causing confusion and creating extra operational work.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-24
- Trigger: Jira issue created webhook
- Automation: jira-to-story work cell

## Assumptions

- The bug is in the catalog search logic, not in deployment or cloud infrastructure
- Empty status strings are bypassing the intended availability filter
- No schema changes or new dependencies are needed
- The fix should preserve explicit pending-pet search capability for support workflows

## Non-Goals

- Cloud remediation or deployment changes
- Auth, secrets, or IAM changes
- UI redesign beyond what's needed for correctness
- Changes to adoption order validation
- Database or persistence layer changes

## What Changes

- Catalog search will treat empty or whitespace-only status strings as "available"
- Default search continues to return only available pets
- Explicit `status="pending"` searches remain supported for operations workflows
- Add regression test coverage for empty status strings

## Impact

- App behavior: Empty status parameters will default to "available" instead of bypassing the filter
- Tests: New test coverage for the empty-status edge case and default search regression
- Humans: QA approval needed before merge; deployment approval controlled separately

## Human Gates

- Scope approval: Jira issue defines the business problem; implementation inferred from code and docs
- Review approval: Required before merge
- Merge approval: Required
- Deployment approval: Required
