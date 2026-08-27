# Change: Fix Pending Pets Visibility in Catalog Search

## Why

Customers are seeing pets that should not be available for adoption yet (pets with `status="pending"`). This violates the core catalog availability rule that default customer-facing searches must show only pets with `status="available"`. The bug creates customer confusion and generates extra operational work.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-139
- Trigger: Jira webhook `jira:issue_created`
- Automation: SDLC Automation Demo - Jira Request To PR

## Assumptions

- The bug is in the catalog search logic, not in data or UI presentation
- Empty status parameter should default to "available" per business rules
- Explicit `status="pending"` searches should continue to work for operations workflows
- No schema, auth, or deployment changes are needed

## Non-Goals

- Changing adoption workflow or status transitions
- Modifying pet data structure or storage
- UI changes beyond what currently uses the search function
- Adding new status values or states

## What Changes

- Catalog search function will enforce that empty status parameters default to "available"
- Status filter logic will be simplified to always apply the normalized status
- Tests will verify that pending pets never appear in default searches

## Impact

- App behavior: Default pet searches and empty-status searches will now correctly exclude pending pets
- Tests: New regression test added to verify pending pets are excluded from default results
- Humans: PR requires scope review, code review, merge approval, and deployment approval per SDLC policy

## Human Gates

- Scope approval: Confirm this fix addresses the reported symptom
- Review approval: Code review via `openhands-review` label automation
- Merge approval: Human must approve and merge the PR
- Deployment approval: Human must approve deployment of the fix
