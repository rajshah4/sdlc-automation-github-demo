# Change: Fix Pending Pets Appearing in Available Catalog

## Why

Customer support reports that pets customers cannot actually adopt are showing up when shoppers browse available pets. This causes confusion and failed adoption attempts. The catalog's default search must return only pets with `status="available"`, per the product requirements in `docs/wiki/petstore-catalog-availability.md`.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-51
- Trigger: Sidekick demo DEMO_STEP 3
- Automation: `sdlc-story`
- Evidence: `PENDING_PET_VISIBLE` log in `docs/logs/pending-pet-visible.ndjson`

## Assumptions

- The bug is in the `search_pets()` function's status filter logic, which skips filtering when `normalized_status` evaluates to an empty string
- Explicit pending pet searches (`status="pending"`) must continue to work for support workflows
- No database, schema, or API contract changes are required
- The fix can be completed with a single line change and focused tests

## Non-Goals

- Changing the web UI or `cloud_run_app.py` incident mode simulation
- Modifying the `visible_pets()` function used by the web frontend
- Adding new status values or catalog features
- Updating authentication, authorization, or deployment configuration

## What Changes

- Fix the `search_pets()` function in `app/petstore_app/catalog.py` to properly enforce status filtering
- Add regression test to verify default search excludes pending pets
- Verify existing explicit pending-pet searches continue to work

## Evidence Waypoints

- `Stop 1 - Ticket`: KAN-51 reports pets that cannot be adopted are showing in available list
- `Stop 2 - Wiki/Docs`: `docs/wiki/petstore-catalog-availability.md` confirms default search must show only `status="available"`
- `Stop 3 - Logs`: `docs/logs/pending-pet-visible.ndjson` shows `PENDING_PET_VISIBLE` error with `pet-103` (Nova)
- `Stop 4 - Repo/Files`: `app/petstore_app/catalog.py` line 50 has the bug - empty string status skips the filter
- `Stop 5 - Tests/PR`: Added regression test and creating PR

## Impact

- App behavior: Customers see only adoptable pets in the default catalog view
- Tests: Catalog tests cover default available behavior and explicit pending searches
- Humans: Reviewers approve the product scope and merge decision

## Human Gates

- Scope approval: Jira issue and PR review
- Review approval: GitHub PR review
- Merge approval: Repository maintainers
- Deployment approval: Outside this automation
