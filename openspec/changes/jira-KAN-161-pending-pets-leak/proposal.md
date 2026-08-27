# Change: Fix Pending Pets Leaking into Customer-Facing Catalog

## Why

Support reports that customers are seeing pets that should not be available yet. Specifically, some customers can see and start adoption flows for pets with `status="pending"`. This violates our core product rule that the default pet search must return only available pets, creates customer confusion, and generates extra operational work.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-161
- Trigger: Jira webhook `jira:issue_created`
- Automation: Jira Request To PR With Native Sub-Agents

## Assumptions

- The backend `search_pets()` function has the correct default parameter (`status="available"`), but there may be an edge case where the default is not enforced
- The frontend correctly filters by `status === "available"` in the current code, but the log evidence from 2026-06-29 shows pet-103 (Nova) with `status="pending"` leaked through
- No deployment, authentication, or database changes are needed; this is a filtering logic issue
- The fix should be defensive and handle edge cases (null status, empty status, missing status field)

## Non-Goals

- Adding new pet statuses beyond "available" and "pending"
- Changing adoption workflow or status transitions
- Modifying deployment configuration or environment settings
- Adding authentication or authorization changes
- Changing the UI beyond defensive filtering

## What Changes

- Strengthen the backend catalog filtering to ensure robust default behavior
- Add defensive checks in frontend filtering to handle edge cases
- Add comprehensive test coverage for default status filtering and edge cases
- Document the fix and log evidence in the PR

## Impact

- App behavior: The default pet catalog will more reliably filter out pending pets, preventing customer confusion
- Tests: New tests verify default filtering behavior and edge cases (null/empty/missing status)
- Humans: Support team will see fewer operational issues; customers will only see genuinely available pets

## Human Gates

- Scope approval: Automated approval based on log evidence marked `"safe_to_fix": true`
- Review approval: Human reviewer approves the code changes
- Merge approval: Human approves merge to main branch
- Deployment approval: Human approves deployment to production
