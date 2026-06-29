# Change: Fix unavailable pets appearing in available catalog

## Why

Support reports that Nova appears in the available-pets experience even though she is not adoptable. The catalog should not show pending pets in default available results.

## Source

- GitHub issue: https://github.com/example-org/sdlc-automation-github-demo/issues/123
- Trigger label: `openhands-build`
- Automation: `sdlc-story`
- Evidence: `PENDING_PET_VISIBLE` log or fixture signal

## Assumptions

- Nova maps to `pet-103` and has `status="pending"` in the Petstore seed data.
- The request is limited to default catalog availability behavior.
- Explicit pending-pet searches should continue to work when callers request `status="pending"`.

## Non-Goals

- Runtime remediation, deployment changes, cloud resource changes, auth, persistence, and unrelated UI changes are out of scope.

## What Changes

- Default available-pets search excludes pending pets.
- Explicit pending-pet searches still return pending pets when requested.
- Focused regression tests cover the pending-pet visibility bug.

## Evidence Waypoints

- `Stop 1 - Ticket`: sparse bug report says customers are seeing pets that are not available.
- `Stop 2 - Wiki/Docs`: `docs/wiki/petstore-catalog-availability.md`.
- `Stop 3 - Logs`: `docs/logs/pending-pet-visible.ndjson`, error code `PENDING_PET_VISIBLE`.
- `Stop 4 - Repo/Files`: catalog and Cloud Run surfaces plus focused tests.
- `Stop 5 - Tests/PR`: regression tests and draft PR for human review.

## Impact

- App behavior: adopters see only adoptable pets by default.
- Tests: catalog tests cover default available behavior and explicit pending searches.
- Humans: reviewers approve the product scope and merge decision.

## Human Gates

- Scope approval: GitHub issue and PR review.
- Review approval: GitHub PR review.
- Merge approval: repository maintainers.
- Deployment approval: outside this automation.
