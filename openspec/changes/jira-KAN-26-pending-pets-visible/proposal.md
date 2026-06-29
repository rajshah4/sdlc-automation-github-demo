# Change: Fix unavailable pets appearing in catalog

## Why

Support reports that customers can still find pets in the catalog that the adoption team does not consider available. This is causing confusing handoffs when families ask to adopt an animal that should not be shown as available.

## Source

- Jira issue: https://rajshah4.atlassian.net/browse/KAN-26
- Jira Issue Key: KAN-26
- API URL: https://api.atlassian.com/ex/jira/19c67202-a774-4b89-9aed-0466783f68e2/rest/api/3/issue/10351
- Issue Type: Task (bug)
- Labels: `bug`, `jira-to-story-demo`, `openhands-demo`, `live-smoke`
- Automation: `sdlc-story` (Jira-triggered work cell)
- Evidence: `PENDING_PET_VISIBLE` error code from `docs/logs/pending-pet-visible.ndjson`

## Assumptions

- The issue describes catalog behavior showing pending pets as available
- Nova is `pet-103` with `status="pending"` per `docs/wiki/petstore-catalog-availability.md`
- The request is limited to default catalog availability behavior
- Explicit pending-pet searches by support/operations should continue to work when `status="pending"` is requested
- The bug is in the backend API endpoint, not the static UI filter

## Non-Goals

- Runtime remediation, deployment changes, cloud resource changes, auth, persistence, or unrelated UI changes are out of scope
- Changes to the incident mode simulation system
- Schema changes or data migrations
- Payment or adoption workflow changes

## What Changes

- The `/api/pets` endpoint will use the existing `search_pets()` function from `catalog.py` to respect status filtering
- Default catalog API responses will exclude pending pets (only show `status="available"`)
- Explicit pending-pet searches will continue to work when `status="pending"` is passed
- Focused regression tests will cover the pending-pet visibility bug

## Evidence Waypoints

- **Stop 1 - Ticket**: Jira KAN-26 sparse bug report says customers can find pets that are not available, causing confusing adoption handoffs
- **Stop 2 - Wiki/Docs**: `docs/wiki/petstore-catalog-availability.md` confirms default catalog must show only `status="available"` pets; Nova is `pet-103` with `status="pending"`; `PENDING_PET_VISIBLE` indicates catalog regression
- **Stop 3 - Logs**: `docs/logs/pending-pet-visible.ndjson` shows error code `PENDING_PET_VISIBLE` with `pending_pet_ids: ["pet-103"]` and customer impact message
- **Stop 4 - Repo/Files**: `app/petstore_app/cloud_run_app.py` line 239 `/api/pets` endpoint uses `visible_pets()` instead of `catalog.search_pets()`, bypassing status filtering; `app/petstore_app/catalog.py` has correct filtering logic that is not being used
- **Stop 5 - Tests/PR**: Regression tests added to `test_cloud_run_app.py` and draft PR for human review

## Impact

- **App behavior**: The `/api/pets` API endpoint will correctly filter to available-only pets by default
- **Tests**: New API-level regression tests cover the default available behavior and explicit pending searches
- **Humans**: Reviewers approve the product scope, implementation approach, and merge decision

## Human Gates

- **Scope approval**: Jira issue review and PR review
- **Review approval**: GitHub PR review
- **Merge approval**: Repository maintainers
- **Deployment approval**: Outside this automation
