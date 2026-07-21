# Change: Fix unavailable pets appearing in available catalog

## Why

Support reports that Nova is showing up in the available pets list even though she should not be adoptable. The catalog must not show pending pets in the default available-pets experience.

## Source

- GitHub issue: https://github.com/rajshah4/sdlc-automation-github-demo/issues/78
- Issue title: "Customers are seeing pets that are not available"
- Issue body: "Support says Nova is showing up in the available pets list even though she should not be adoptable."
- Trigger label: `openhands-build`
- Automation: `sdlc-story`
- Evidence: `PENDING_PET_VISIBLE` error code in `docs/logs/pending-pet-visible.ndjson`

## Assumptions

- Nova maps to `pet-103` and has `status="pending"` in the Petstore seed data.
- The bug occurs when empty or blank status values bypass the status filter in `search_pets()`.
- The request is limited to default catalog availability behavior.
- Explicit pending-pet searches should continue to work when callers request `status="pending"`.
- No API endpoint changes are needed; this is a backend catalog function fix.

## Non-Goals

- Deployment changes, auth, persistence, and unrelated UI changes are out of scope.
- No changes to the static web UI are required; the UI already correctly filters by available status.
- No new dependencies or schema migrations.

## What Changes

- Ensure the catalog `search_pets()` function always defaults to "available" status, even when an empty string is passed.
- Default available-pets search reliably excludes pending pets.
- Explicit pending-pet searches still return pending pets when requested with `status="pending"`.
- Add focused regression tests to prove pending pets stay out of default available results.

## Evidence Waypoints

- `Stop 1 - Ticket`: GitHub issue #78 reports "Nova is showing up in the available pets list even though she should not be adoptable."
- `Stop 2 - Wiki/Docs`: Checked `docs/wiki/petstore-catalog-availability.md` which confirms: "Default customer-facing catalog search must show only pets with `status="available"`" and that Nova is pet-103 with pending status.
- `Stop 3 - Logs`: Found `docs/logs/pending-pet-visible.ndjson` with error code `PENDING_PET_VISIBLE` showing pet-103 (Nova) was visible in the available-pets experience.
- `Stop 4 - Repo/Files`: Identified `app/petstore_app/catalog.py` where `search_pets()` function has a bug - when status is an empty string, the filter check `if normalized_status and normalized_status != pet.status` skips the status filter entirely.
- `Stop 5 - Tests/PR`: Will add regression tests and create draft PR for human review.

## Impact

- App behavior: Adopters see only adoptable pets by default, even when status is blank/empty.
- Tests: Catalog tests cover default available behavior and edge cases with empty status strings.
- Humans: Reviewers approve the product scope and merge decision.

## Human Gates

- Scope approval: GitHub issue #78 and PR review.
- Review approval: GitHub PR review.
- Merge approval: Repository maintainers.
- Deployment approval: Outside this automation.
