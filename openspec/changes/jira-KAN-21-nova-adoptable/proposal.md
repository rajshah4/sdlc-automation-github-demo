# Change: Fix pending pet Nova showing as adoptable in catalog

## Why

Support reports that Nova appears in the available-pets catalog but should not be available to customers. This is a catalog regression where pending-status pets incorrectly appear in the default customer-facing experience.

## Source

- Jira issue: KAN-21 "Nova is showing up as adoptable"
- Jira URL: https://rajiv-shah.atlassian.net/browse/KAN-21
- Trigger: Jira webhook event `jira:issue_created`
- Automation: Jira-triggered `openhands-build` work cell
- Evidence: `PENDING_PET_VISIBLE` log error code

## Assumptions

- Nova maps to `pet-103` and has `status="pending"` in the Petstore seed data (confirmed in catalog.py).
- The request is limited to fixing default catalog visibility behavior.
- Explicit pending-pet searches (for support/operations) should continue to work when callers explicitly request `status="pending"`.
- The bug is in the `visible_pets()` function in `cloud_run_app.py`, not the `search_pets()` function in `catalog.py`.

## Non-Goals

- Runtime remediation API endpoints and incident mode infrastructure remain unchanged.
- Deployment changes, cloud resource changes, auth, persistence, and unrelated UI changes are out of scope.
- Health check behavior and status reporting remain unchanged.

## What Changes

- `app/petstore_app/cloud_run_app.py`: Fix `visible_pets()` function to always filter to `status="available"` pets, removing the incident mode bypass.
- `app/tests/test_cloud_run_app.py`: Update `test_bad_catalog_filter_exposes_pending_pet` to reflect correct behavior.
- Focused regression tests confirm pending pets stay out of default available results.

## Evidence Waypoints

- **Stop 1 - Ticket**: Jira KAN-21 reports Nova (pending pet) showing as adoptable when she should not be available to customers.
- **Stop 2 - Wiki/Docs**: `docs/wiki/petstore-catalog-availability.md` confirms default catalog search must show only `status="available"` pets; pending pets must not appear in default experience.
- **Stop 3 - Logs**: `docs/logs/pending-pet-visible.ndjson` shows `PENDING_PET_VISIBLE` error code for `pet-103` (Nova) in `web.available_pets` operation.
- **Stop 4 - Repo/Files**: Bug in `app/petstore_app/cloud_run_app.py` lines 92-95: `visible_pets()` returns all pets when in INCIDENT_MODE instead of filtering to available only.
- **Stop 5 - Tests/PR**: Regression test coverage and draft PR for human review.

## Impact

- **App behavior**: Default catalog experience shows only available pets; pending pets like Nova are correctly excluded.
- **Tests**: Existing test `test_visible_pets_excludes_pending_by_default` continues to pass; `test_bad_catalog_filter_exposes_pending_pet` updated to expect correct filtering.
- **Humans**: Jira and PR reviewers approve scope; repository maintainers approve merge; deployment decisions remain with operations team.

## Human Gates

- Scope approval: Jira issue review and PR review.
- Review approval: GitHub PR review.
- Merge approval: Repository maintainers.
- Deployment approval: Outside this automation scope.
