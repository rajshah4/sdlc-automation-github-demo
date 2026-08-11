# Change: Fix unavailable pets appearing in available catalog

## Why

Support reports that customers are able to see and start adoption flows for pets that should not be available yet. This is confusing customers and creating extra work for operations. The catalog must not show pending pets in default available results.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-148
- Summary: "Customers are seeing pets that are not available"
- Automation: Jira webhook → `sdlc-story`
- Evidence: `PENDING_PET_VISIBLE` log signal in `docs/logs/pending-pet-visible.ndjson`

## Assumptions

- Nova maps to `pet-103` and has `status="pending"` in the Petstore seed data (confirmed in `docs/wiki/petstore-catalog-availability.md`).
- The request is limited to default catalog availability behavior in the web frontend.
- Explicit pending-pet searches should continue to work when callers request `status="pending"`.
- The backend `catalog.py` already filters by status correctly; the issue is in the frontend display logic.

## Non-Goals

- Deployment changes, authentication, persistence, payment processing, and unrelated UI features are out of scope.
- Changes to adoption flow validation (separate concern, may need follow-up ticket).

## What Changes

- Frontend pet list rendering explicitly filters out non-available pets before display.
- Default available-pets search continues to exclude pending pets.
- Explicit pending-pet searches still return pending pets when explicitly requested by support/operations.
- Regression tests validate that pending pets never appear in default available results.

## Evidence Waypoints

- `Stop 1 - Ticket`: Jira KAN-148 - "Customers are seeing pets that are not available" with description about adoption flows for unavailable pets.
- `Stop 2 - Wiki/Docs`: `docs/wiki/petstore-catalog-availability.md` - confirms default search must show only `status="available"` and that Nova (`pet-103`) is pending.
- `Stop 3 - Logs`: `docs/logs/pending-pet-visible.ndjson` - error code `PENDING_PET_VISIBLE`, signals catalog regression, identifies `pet-103` as the visible pending pet.
- `Stop 4 - Repo/Files`: `app/web/app.js` (frontend filtering), `app/petstore_app/catalog.py` (backend filtering - already correct), `app/tests/test_pet_catalog.py` (existing backend tests).
- `Stop 5 - Tests/PR`: Add frontend validation test, verify backend behavior unchanged, create draft PR for human review.

## Impact

- App behavior: customers see only adoptable pets by default in the web UI.
- Tests: frontend and backend tests validate available-only default behavior.
- Operations: reduced support burden from customers confused by unavailable pets.
- Humans: reviewers approve product scope, implementation approach, and merge decision.

## Human Gates

- Scope approval: Jira issue and PR review.
- Review approval: GitHub PR review with `openhands-review` label.
- QA approval: Functional testing via `openhands-qa` label (triggered by review work cell).
- Merge approval: repository maintainers.
- Deployment approval: outside this automation.
