# Change: Fix Pending Pets Visible in Default Catalog

## Why

Support reports that some customers are able to see and start adoption flows for pets that should not be available yet. This is confusing customers and creating extra work for operations. The default catalog search must show only available pets.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-53
- Trigger: jira:issue_created
- Automation: sdlc-automation-github-demo Jira-to-PR workflow

## Assumptions

- The bug is in the catalog search filter logic, not in the pet data or UI
- The intended behavior is documented in `docs/wiki/petstore-catalog-availability.md`
- `PENDING_PET_VISIBLE` error code in logs confirms the regression
- No schema changes or new dependencies are required
- The fix should be minimal and focused on the status filter

## Non-Goals

- Changing how pending pets are stored or managed
- Modifying the UI beyond what the backend fix requires
- Altering adoption workflow or order validation
- Adding new pet statuses or catalog features
- Changing API authentication or authorization

## What Changes

- Fix the `search_pets()` function in `app/petstore_app/catalog.py` to properly filter out pending pets in default searches
- Add regression test to ensure pending pets never appear in default available-only searches
- Preserve the ability to explicitly request pending pets when `status="pending"` is specified

## Impact

- App behavior: Default catalog searches will correctly exclude pending pets; explicit pending searches still work
- Tests: New regression test added to prevent this bug from recurring
- Humans: Requires PR review approval and merge approval; no deployment configuration changes needed

## Human Gates

- Scope approval: Automated (narrow bug fix within established behavior)
- Review approval: Required (human must review the PR)
- Merge approval: Required (human must approve and merge)
- Deployment approval: Standard deployment process applies
