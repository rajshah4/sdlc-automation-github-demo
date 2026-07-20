# Change: Fix pending pets visible in available catalog

## Why

Support reports that customers are able to see and start adoption flows for pets that should not be available yet. This creates confusion for customers and extra work for operations. The catalog search is incorrectly showing pending pets when an empty status filter is provided.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-116
- Story title: Customers are seeing pets that are not available
- Automation: `sdlc-story` via replicated-factory-20260720-121303
- Evidence: `PENDING_PET_VISIBLE` log signal

## Assumptions

- Nova maps to `pet-103` and has `status="pending"` in the Petstore seed data.
- The bug occurs when `search_pets()` is called with an empty status string (`status=""`), bypassing the availability filter.
- The request is limited to fixing the catalog availability filter logic.
- Explicit pending-pet searches should continue to work when callers request `status="pending"`.

## Non-Goals

- Deployment changes, auth, persistence, and unrelated UI changes are out of scope.
- Adding new pet statuses or changing the data model.
- Modifying adoption flow logic beyond catalog filtering.

## What Changes

- Fix `search_pets()` to treat empty status strings as "available" (the default).
- Ensure default available-pets search excludes pending pets in all cases.
- Explicit pending-pet searches still return pending pets when requested.
- Add focused regression tests to prevent empty-status bypass.

## Evidence Waypoints

- `Stop 1 - Ticket`: Jira KAN-116 reports customers seeing pets that should not be available yet.
- `Stop 2 - Wiki/Docs`: `docs/wiki/petstore-catalog-availability.md` confirms only available pets should show by default.
- `Stop 3 - Logs`: `docs/logs/pending-pet-visible.ndjson`, error code `PENDING_PET_VISIBLE`, `pending_pet_ids`: `["pet-103"]`.
- `Stop 4 - Repo/Files`: `app/petstore_app/catalog.py` line 50 has the bug - empty status string bypasses filter.
- `Stop 5 - Tests/PR`: regression tests and draft PR for human review.

## Impact

- App behavior: adopters see only adoptable pets by default, even when empty status is provided.
- Tests: catalog tests cover default available behavior, empty status string, and explicit pending searches.
- Humans: reviewers approve the product scope and merge decision.

## Human Gates

- Scope approval: Jira issue and PR review.
- Review approval: GitHub PR review.
- Merge approval: repository maintainers.
- Deployment approval: outside this automation.
