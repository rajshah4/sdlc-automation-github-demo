# Change: Fix Pending Pets Appearing in Default Search

## Why

Support reports that customers can see and start adoption flows for pets with `status="pending"`. This violates the product rule that default pet searches must return only available pets. The `PENDING_PET_VISIBLE` error log confirms pet-103 (Nova) appeared in the available-pets experience, which creates confusion and extra operational work.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-238
- Trigger: Jira webhook `jira:issue_created`
- Automation: `jira-issue-to-pr`
- Evidence: `PENDING_PET_VISIBLE` log at `docs/logs/pending-pet-visible.ndjson`

## Assumptions

- Nova maps to `pet-103` and has `status="pending"` in the Petstore seed data
- The bug is in the filter logic in `catalog.py`, not the data or UI layer
- Current tests are insufficient to catch this regression
- No customers depend on the buggy behavior (seeing pending pets by default)
- Explicit pending-pet searches should continue to work when callers request `status="pending"`

## Non-Goals

- Changing the function signature or adding new parameters
- Modifying the UI or adoption flow logic
- Adding new pet statuses or complex filtering rules
- Changing operations workflows or tooling
- Deployment changes, auth, persistence, or schema migrations

## What Changes

- Fix the status filter logic in `search_pets()` to enforce the default `status="available"` parameter
- Default available-pets search excludes pending pets
- Explicit pending-pet searches still return pending pets when requested
- Add focused regression test to verify pending pets are excluded by default

## Evidence Waypoints

- `Stop 1 - Ticket`: Jira issue KAN-238 says customers are seeing pets that are not available
- `Stop 2 - Wiki/Docs`: `docs/wiki/petstore-catalog-availability.md` confirms default search must show only available pets
- `Stop 3 - Logs`: `docs/logs/pending-pet-visible.ndjson` shows error code `PENDING_PET_VISIBLE` with `pending_pet_ids: ["pet-103"]`
- `Stop 4 - Repo/Files`: Bug found in `app/petstore_app/catalog.py` status filter logic
- `Stop 5 - Tests/PR`: Regression test added and draft PR opened for human review

## Impact

- App behavior: Customers see only adoptable pets in default search results; operations can still explicitly search for pending pets
- Tests: Catalog tests now cover default available-only behavior and explicit pending searches
- Humans: Reviewers approve the product scope and merge decision

## Human Gates

- Scope approval: Jira issue and PR review
- Review approval: GitHub PR review
- Merge approval: Repository maintainers
- Deployment approval: Outside this automation
