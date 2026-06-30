# Change: Fix pending pets appearing in available catalog

## Why

Support reports that customers are seeing pets that should not be available yet. This is confusing customers and creating extra work for operations. The default catalog should show only available pets.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-54
- Issue key: KAN-54
- Summary: "Customers are seeing pets that are not available"
- Automation: `sdlc-story` (Jira webhook trigger)
- Evidence: `PENDING_PET_VISIBLE` error code in logs

## Assumptions

- Nova (`pet-103`) has `status="pending"` and should not appear in default available-pets results.
- The issue is limited to default catalog availability behavior in the web API.
- Explicit pending-pet searches should continue to work when callers request `status="pending"`.
- The bug is in the `/api/pets` endpoint's `visible_pets()` function which bypasses the catalog filter.

## Non-Goals

- Runtime remediation, deployment changes, cloud resource changes, auth, persistence, and unrelated UI changes are out of scope.
- Admin endpoints and incident simulation features remain unchanged.

## What Changes

- Default `/api/pets` endpoint returns only available pets.
- The `visible_pets()` function respects catalog availability rules.
- Explicit pending-pet searches still work when requested via `search_pets(status="pending")`.
- Focused regression tests verify pending pets don't appear in default results.

## Evidence Waypoints

- **Stop 1 - Ticket**: Jira KAN-54 sparse report "Customers are seeing pets that are not available"
- **Stop 2 - Wiki/Docs**: `docs/wiki/petstore-catalog-availability.md` defines availability rules
- **Stop 3 - Logs**: `docs/logs/pending-pet-visible.ndjson` with error code `PENDING_PET_VISIBLE`
- **Stop 4 - Repo/Files**: `app/petstore_app/cloud_run_app.py` (visible_pets function), `app/petstore_app/catalog.py`
- **Stop 5 - Tests/PR**: Add regression test, validate fix, open draft PR

## Impact

- **App behavior**: Customers see only adoptable pets in default search results
- **API**: `/api/pets` endpoint filters to available pets only
- **Tests**: New regression test ensures pending pets remain hidden
- **Humans**: PR review and merge approval required before deployment

## Human Gates

- Scope approval: Jira issue and PR review
- Review approval: GitHub PR review
- Merge approval: Repository maintainers
- Deployment approval: Outside this automation
