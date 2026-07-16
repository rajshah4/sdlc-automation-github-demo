# Change: Fix Pending Pets Appearing in Available Pet Search

## Why

Support reports that customers are seeing and starting adoption flows for pets with `status="pending"` that should not be visible in the default available-pets experience. This creates customer confusion and extra operational work.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-114
- Trigger: Replicated Jira delegated factory
- Automation: story-to-pr work cell

## Assumptions

- The bug occurs when the catalog search receives an empty string for the status parameter, causing the status filter to be skipped entirely.
- The default behavior must always filter to `status="available"` unless explicitly overridden.
- Explicit requests for `status="pending"` from support/operations workflows must continue to work.
- No schema, data migration, or deployment changes are required.

## Non-Goals

- Do not change the Pet data structure or add new statuses.
- Do not add authentication, authorization, or access control.
- Do not modify the UI beyond what is explicitly requested.
- Do not add new dependencies or services.

## What Changes

- Update `search_pets()` in `app/petstore_app/catalog.py` to treat empty status strings as "available" instead of disabling the status filter.
- Add regression test coverage to ensure pending pets never appear when status is empty or unspecified.

## Impact

- App behavior: Default searches and empty-status searches will now correctly exclude pending pets.
- Tests: New test case added to verify the fix.
- Humans: PR review required before merge; QA automation will validate the change.

## Human Gates

- Scope approval: Automated (Jira factory)
- Review approval: Required
- Merge approval: Required
- Deployment approval: Required
