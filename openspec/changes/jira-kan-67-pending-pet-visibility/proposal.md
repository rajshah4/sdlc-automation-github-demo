# Change: Fix Pending Pet Visibility in Available Catalog

## Why

Support reports that customers are seeing pets with pending status in the available-pets catalog experience. Pending pets should only be visible to operations staff who explicitly request them, not to customers browsing available pets for adoption.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-67
- Trigger: Jira ticket KAN-67 - "Customers are seeing pets that are not available"
- Automation: SDLC sidekick demo implementation agent

## Assumptions

- The catalog filtering logic is already correct in `app/petstore_app/catalog.py` with default `status="available"`
- The web UI JavaScript in `app/web/app.js` has the correct filter `pet.status === "available"`
- The issue has been resolved but lacks comprehensive regression test coverage
- No schema changes, auth changes, or new dependencies are required

## Non-Goals

- Changing the data model for pet status
- Adding new pet status values beyond available/pending
- Modifying adoption workflow logic
- Altering operations staff workflows that legitimately need to view pending pets

## What Changes

- Add regression test to verify pending pets (specifically Nova/pet-103) are excluded from default catalog search
- Add test to verify pending pets can still be found when explicitly requested with `status="pending"`
- Document the fix with evidence waypoints (wiki, logs, tests)

## Impact

- App behavior: No change (filter is already correct)
- Tests: New regression tests prevent future regressions
- Humans: PR reviewer validates test coverage and evidence trail

## Human Gates

- Scope approval: Required - confirm test-only PR is acceptable for resolved issue
- Review approval: Required - human reviewer must approve test additions
- Merge approval: Required - human must merge to main
- Deployment approval: N/A - test-only change
