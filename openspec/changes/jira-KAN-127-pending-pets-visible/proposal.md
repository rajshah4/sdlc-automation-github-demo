# Change: Fix Pending Pets Visible in Default Search

## Why

Support reports that customers are seeing pets marked as "pending" in their default available-pets search experience. This violates the Petstore availability rule that default searches must show only available pets. Pending pets should only appear when explicitly requested by support or operations workflows.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-127
- Issue key: KAN-127
- Summary: "Customers are seeing pets that are not available"
- Description: "Support reports that some customers are able to see and start adoption flows for pets that should not be available yet. This is confusing customers and creating extra work for operations. Please investigate and fix."
- Trigger: jira:issue_created
- Automation: SDLC Automation Demo - Jira Request To PR

## Assumptions

- The issue is in the `search_pets()` function in `app/petstore_app/catalog.py`
- Log evidence `PENDING_PET_VISIBLE` confirms pet-103 (Nova) appeared in available-pets search
- The fix should preserve explicit pending searches (when `status="pending"` is requested)
- No schema, deployment, or auth changes are needed
- This is a catalog filtering regression that is safe to fix with minimal code changes

## Non-Goals

- Changing UI behavior beyond what the backend fix naturally enables
- Adding new pet statuses or lifecycle states
- Modifying adoption flow validation
- Changing authentication or authorization
- Adding new dependencies or external services

## What Changes

- `app/petstore_app/catalog.py`: Fix the `search_pets()` function to properly enforce the default status filter
- `app/tests/test_pet_catalog.py`: Add regression tests proving pending pets stay out of default available searches

## Impact

- App behavior: Default pet search will correctly exclude pending pets; explicit pending searches remain functional
- Tests: New regression tests added to prevent future catalog filtering bugs
- Humans: Operations will no longer receive customer confusion reports about pending pets appearing prematurely

## Human Gates

- Scope approval: ✓ (minimal catalog filter fix)
- Review approval: Required (PR must be reviewed before merge)
- Merge approval: Required (humans approve merge decision)
- Deployment approval: Required (humans approve deployment timing)
