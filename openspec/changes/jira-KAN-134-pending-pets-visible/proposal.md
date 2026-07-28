# Change: Fix Pending Pets Visible in Default Search

## Why

Support reports that customers are seeing pets with `status="pending"` in the default available-pets experience. This violates the product rule that default search must return only available pets. Pending pets should only appear when explicitly requested by support or operations staff investigating a case.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-134
- Trigger: Jira webhook `jira:issue_created`
- Automation: SDLC Automation Demo - Jira Request to PR

## Assumptions

- The bug occurs when the `status` parameter is passed as an empty string to `search_pets()`
- The catalog behavior is in `app/petstore_app/catalog.py`
- Fixing the status filter logic will resolve the customer-facing issue
- No UI changes are required; this is a backend catalog behavior fix
- The fix should preserve explicit `status="pending"` searches for support workflows

## Non-Goals

- UI changes to hide pending pets in the frontend
- Changes to pet data model or status values
- Auth or permission-based filtering
- New dependencies or external integrations
- Deployment or infrastructure changes

## What Changes

- `app/petstore_app/catalog.py`: Update `search_pets()` to treat empty or whitespace-only status values as `"available"`
- `app/tests/test_pet_catalog.py`: Add regression test proving empty status defaults to available-only results

## Impact

- App behavior: Default and empty-status searches will exclude pending pets; explicit `status="pending"` searches still work
- Tests: New test coverage for the empty-status edge case
- Humans: Requires PR review and merge approval before deployment

## Human Gates

- Scope approval: Auto-approved for catalog regression fix (safe, narrow change)
- Review approval: Required before merge
- Merge approval: Required before merge
- Deployment approval: Required for production release
