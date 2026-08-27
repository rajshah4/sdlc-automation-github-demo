# Change: Fix Pending Pets Visible in Default Catalog Search

## Why

Customers are seeing pets in the adoption catalog that should not be available yet. When pets have `status="pending"`, they should only appear in explicit pending-status searches used by support staff, not in the default customer-facing catalog experience. This creates customer confusion and extra operational burden.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-124
- Trigger: Jira webhook (jira:issue_created)
- Automation: SDLC Automation Demo - Jira Request To PR

## Assumptions

- The bug is in the catalog search filter logic when handling empty or missing status parameters
- Nova (pet-103) with status="pending" is the known test case based on log evidence
- Support workflows that explicitly request `status="pending"` should continue to work unchanged
- No API contract changes are required; this is a backend filter fix

## Non-Goals

- Changing the Pet data model or status values
- Adding new API endpoints or UI controls for status filtering
- Modifying adoption flow, payment processing, or authentication
- Schema migrations or database changes
- Changes to support/operations tools that explicitly request pending pets

## What Changes

- Fix `search_pets()` in `app/petstore_app/catalog.py` to ensure empty status strings default to "available" filtering
- Add regression test coverage to prevent pending pets from appearing when status parameter is empty or bypassed
- Default catalog search will correctly exclude pending pets in all cases

## Impact

- App behavior: Default catalog searches will never show pending pets, even when status filter is explicitly set to empty string
- Tests: New regression test added to verify empty status parameter behavior
- Humans: PR requires review approval before merge; QA automation will validate the fix independently

## Human Gates

- Scope approval: Automated workflow proceeds for safe catalog filter fix
- Review approval: Human reviewer must approve PR before merge
- Merge approval: Human must merge the PR
- Deployment approval: Human controls deployment timing
