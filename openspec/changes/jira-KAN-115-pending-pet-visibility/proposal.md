# Change: Verify default catalog search excludes pending pets

## Why

Support reports that customers are able to see and start adoption flows for pets that should not be available yet. The default catalog search must show only available pets to customers.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-115
- Jira title: Customers are seeing pets that are not available
- Trigger: Jira-based factory automation
- Automation: `replicated-factory-20260716-212419` story-to-pr work cell

## Assumptions

- The backend `search_pets()` function already defaults to `status="available"` and correctly filters pending pets.
- The backend adoption logic already rejects pending pets.
- The frontend UI already filters by `status === "available"`.
- The missing piece is **explicit test coverage** that verifies the default search behavior excludes pending pets.
- Nova maps to `pet-103` with `status="pending"` in the Petstore catalog.

## Non-Goals

- Deployment changes, authentication, database persistence are out of scope.
- Schema changes or new dependencies are not required.
- No backend code changes needed; implementation already correct.
- No frontend code changes needed; filter already correct.

## What Changes

- Add focused regression test that verifies default `search_pets()` call (no parameters) returns only available pets and excludes Nova (pet-103).
- Document evidence waypoints showing backend, frontend, and adoption logic already correctly handle pending pets.

## Evidence Waypoints

- `Stop 1 - Ticket`: Jira KAN-115 reports "Customers are seeing pets that are not available"
- `Stop 2 - Wiki/Docs`: `docs/wiki/petstore-catalog-availability.md` confirms Nova is pet-103 with status="pending" and PENDING_PET_VISIBLE logs indicate catalog regressions
- `Stop 3 - Logs`: `docs/logs/pending-pet-visible.ndjson` shows ERROR with code PENDING_PET_VISIBLE for pet-103
- `Stop 4 - Repo/Files`: Reviewed `app/petstore_app/catalog.py` (status filter correct), `app/petstore_app/adoptions.py` (rejects pending pets), `app/web/app.js` (UI filter correct)
- `Stop 5 - Tests/PR`: Add missing regression test and create PR

## Impact

- App behavior: No code changes; behavior already correct.
- Tests: Add missing test case for default search to prevent future regressions.
- Humans: Reviewers verify test coverage and approve merge.

## Human Gates

- Scope approval: Jira issue review.
- Review approval: GitHub PR review.
- Merge approval: Repository maintainers.
- Deployment approval: Outside this automation scope.
