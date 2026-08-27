# Change: Fix Pending Pets Appearing in Default Search

## Why

Support reports that customers are seeing pets with "pending" status in their search results when these pets should not be available for adoption yet. This violates the core product rule that default pet searches should return only available pets. The issue is confusing customers and creating operational burden.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-140
- Trigger: Jira webhook `jira:issue_created`
- Automation: SDLC Automation Demo - Jira Request To PR

## Assumptions

- The backend `search_pets()` function is the source of truth for pet filtering
- Empty status parameter should be treated as requesting "available" pets only
- Explicit `status="pending"` requests should continue to work for authorized contexts
- No changes to pet data, authentication, or UI rendering are required

## Non-Goals

- Changing how pending pets are managed or transitioned to available
- Adding access controls or authorization for viewing pending pets
- Modifying the frontend filtering logic (already correct)
- Altering adoption flow or order processing

## What Changes

- Backend catalog search will enforce "available" as the default when an empty status string is passed
- The filter logic will no longer be bypassed when `status=""` is explicitly provided
- All existing behavior for explicit status values remains unchanged

## Impact

- App behavior: Empty status parameter now correctly defaults to "available" filter
- Tests: Added regression test to verify empty status defaults to available-only results
- Humans: Customers will no longer see pending pets in default search results; operations workload reduced

## Human Gates

- Scope approval: Required before implementation
- Review approval: Required via `openhands-review` label
- Merge approval: Required from human reviewer
- Deployment approval: Required before production deployment
