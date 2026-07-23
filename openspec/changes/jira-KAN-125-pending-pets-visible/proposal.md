# Change: Fix Pending Pets Visible in Available Catalog

## Why

Support has reported that customers can see and interact with pets that have a pending status when they should only see available pets. This violates the product rule that the default customer-facing catalog must show only pets with `status="available"`. Pending pets should only appear when explicitly requested by support or operations staff, never in the default experience.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-125
- Trigger: Jira webhook `jira:issue_created`
- Automation: SDLC Automation Demo - Jira Request To PR

## Assumptions

- The backend `search_pets()` function in `catalog.py` correctly defaults to `status="available"`.
- The bug is likely in the frontend UI (`app.js`) where the filter may not be consistently applied.
- Based on log evidence (`PENDING_PET_VISIBLE` for pet-103/Nova), pending pets are leaking through to the UI.
- The fix should not alter the ability for support staff to explicitly query `status="pending"` pets when needed.

## Non-Goals

- Changing authentication or authorization mechanisms
- Modifying the backend adoption order validation (already correct)
- Altering deployment or infrastructure settings
- Redesigning the entire UI
- Adding new dependencies

## What Changes

- Ensure the frontend UI filter robustly excludes pending pets from the default available-pets display
- Add explicit regression tests to verify pending pets never appear in the default catalog view
- Potentially add visual indicators or additional validation to prevent future regressions

## Impact

- App behavior: Pending pets will no longer appear in customer-facing search results
- Tests: New regression tests will catch this bug class in the future
- Humans: Requires review approval before merge; QA validation will verify the fix works in the UI

## Human Gates

- Scope approval: This fix addresses the reported bug within existing product rules
- Review approval: Required before merge
- Merge approval: Required from authorized team member
- Deployment approval: Required before production release
