# Change: Fix pending pets appearing in available catalog

## Why

Support reports that customers are able to see and start adoption flows for pets that should not be available yet. This is confusing customers and creating extra work for operations. The catalog should not show pending pets in default available results.

## Source

- Jira issue: KAN-22 (https://rajiv-shah.atlassian.net/browse/KAN-22)
- Trigger: `jira:issue_created` webhook event from Jira
- Automation: `openhands-build` (Jira work cell)
- Evidence: `PENDING_PET_VISIBLE` error code in logs showing pet-103 (Nova)
- Note: This change was triggered by Jira integration, not a GitHub issue

## Assumptions

- Nova maps to `pet-103` and has `status="pending"` in the Petstore seed data.
- The request is limited to default catalog availability behavior.
- Explicit pending-pet searches should continue to work when callers request `status="pending"`.
- The `/api/pets` endpoint should use the proven `search_pets()` function for consistency.

## Non-Goals

- Runtime remediation, deployment changes, cloud resource changes, auth, persistence, and unrelated UI changes are out of scope.
- Changes to the incident mode simulation (which is used for demo purposes).

## What Changes

- The `/api/pets` endpoint will use `search_pets()` from catalog.py for consistent filtering logic.
- Default available-pets search excludes pending pets.
- Explicit pending-pet searches still return pending pets when requested.
- Focused regression tests cover the pending-pet visibility bug.

## Evidence Waypoints

- `Stop 1 - Ticket`: Jira KAN-22 sparse bug report says customers are seeing pets that are not available.
- `Stop 2 - Wiki/Docs`: `docs/wiki/petstore-catalog-availability.md` confirms default search must show only status="available" pets.
- `Stop 3 - Logs`: `docs/logs/pending-pet-visible.ndjson`, error code `PENDING_PET_VISIBLE`, pet-103 (Nova) visible.
- `Stop 4 - Repo/Files`: `app/petstore_app/catalog.py`, `app/petstore_app/cloud_run_app.py`, and `app/tests/test_pet_catalog.py`.
- `Stop 5 - Tests/PR`: regression tests added and draft PR for human review.

## Impact

- App behavior: adopters see only adoptable pets by default.
- Code consistency: `/api/pets` endpoint uses the same logic as `search_pets()`.
- Tests: catalog tests cover default available behavior and explicit pending searches.
- Humans: reviewers approve the product scope and merge decision.

## Human Gates

- Scope approval: Jira issue and PR review.
- Review approval: GitHub PR review.
- Merge approval: repository maintainers.
- Deployment approval: outside this automation.
