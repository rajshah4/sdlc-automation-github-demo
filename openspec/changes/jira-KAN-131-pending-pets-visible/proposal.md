# Change: Fix Pending Pets Visible in Default Search

## Why

Customers are seeing pets with pending status in the default available-pets experience. This violates the catalog availability rule that default searches must show only available pets. This confusion creates extra work for operations and diminishes customer trust.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-131
- Trigger: Jira webhook issue_created event
- Automation: SDLC Automation Demo - Jira Request To PR

## Assumptions

- The bug is in the catalog search logic where empty status parameters bypass the availability filter
- No UI changes are required; this is a backend filter bug
- Existing explicit `status="pending"` searches for operations workflows must continue to work
- The fix can be deployed without data migration or environment changes

## Non-Goals

- UI changes to pet search interface
- Changes to adoption workflow or pending pet management
- New features for status filtering
- Database schema changes

## What Changes

- `app/petstore_app/catalog.py`: Fix status filter logic to treat empty status parameter as "available"
- `app/tests/test_pet_catalog.py`: Add regression test verifying empty status returns only available pets

## Impact

- App behavior: Empty or missing status parameters will now correctly filter to available pets only
- Tests: New test case added to prevent regression
- Humans: Operations team will see reduced customer confusion tickets; PR requires review and merge approval

## Human Gates

- Scope approval: Auto-approved (bug fix within guardrails)
- Review approval: Required before merge
- Merge approval: Required
- Deployment approval: Required before production release
