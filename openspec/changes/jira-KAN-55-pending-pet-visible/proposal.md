# Change: Fix Pending Pet Visibility in Available Pets Search

## Why

Customers searching for available pets are seeing Nova (pet-103), which has `status="pending"` and should not be adoptable. This violates the product rule that default pet searches must return only available pets. The bug creates a poor customer experience and breaks the catalog contract.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-55
- Trigger: Manual demo execution (DEMO_STEP 3)
- Automation: SDLC Automation Demo (Jira-to-PR workflow)

## Assumptions

- The default status parameter value `"available"` is the correct product intent
- The bug is in the filter condition, not in the default parameter declaration
- Explicit pending searches (when caller passes `status="pending"`) must continue to work
- No other status values are currently in use beyond "available" and "pending"

## Non-Goals

- Do not add new status values
- Do not change the function signature or API contract
- Do not modify adoption logic, UI, or telemetry
- Do not alter explicit status searches (e.g., `status="pending"`)

## What Changes

Fix the status filter logic in `app/petstore_app/catalog.py` so that when an empty status parameter is passed, it correctly defaults to filtering for available pets only, preventing pending pets from leaking into the default search results.

## Impact

- App behavior: Default pet searches will correctly exclude pending pets
- Tests: Add regression tests to prevent this bug from recurring
- Humans: Requires code review approval, merge approval, and deployment approval

## Human Gates

- Scope approval: Required before implementation
- Review approval: Required before merge
- Merge approval: Required by branch protection
- Deployment approval: Required for production release
