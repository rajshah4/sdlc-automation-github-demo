# Change: Fix pending pets visible in default search

## Why

Support reports that customers can see and start adoption flows for pets that should not be available yet. This creates confusion for customers and extra work for operations staff. The default pet search must return only available pets, but pending pets like Nova (pet-103) are appearing in search results when the status parameter is set to an empty string.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-133
- Trigger: jira:issue_created webhook
- Automation: sdlc-story
- Evidence: `PENDING_PET_VISIBLE` error code in `docs/logs/pending-pet-visible.ndjson`

## Assumptions

- The bug occurs when the status parameter is set to an empty string, bypassing the status filter
- All legitimate callers either use the default or explicitly pass a valid status ("available" or "pending")
- No system components intentionally rely on empty-string status to show all pets
- Nova maps to `pet-103` and has `status="pending"` in the Petstore catalog
- Explicit pending-pet searches should continue to work when callers request `status="pending"`

## Non-Goals

- Changing the default status value (remains "available")
- Adding new status values beyond "available" and "pending"
- Modifying the web UI or adoption flows
- Adding authentication or authorization
- Changing deployment or environment configuration

## What Changes

- Status filter in `search_pets()` now defaults empty strings to "available"
- Status filter always applies (no longer bypassable with empty string)
- Default available-pets search excludes pending pets in all cases
- Explicit pending-pet searches still return pending pets when requested
- New regression test covers empty status string behavior

## Evidence Waypoints

- `Stop 1 - Ticket`: Jira KAN-133 reports customers seeing pets that are not available
- `Stop 2 - Wiki/Docs`: `docs/wiki/petstore-catalog-availability.md` confirms default search must exclude pending pets
- `Stop 3 - Logs`: `docs/logs/pending-pet-visible.ndjson` contains `PENDING_PET_VISIBLE` error for pet-103 (Nova)
- `Stop 4 - Repo/Files`: `app/petstore_app/catalog.py` line 50 conditional allows empty string to bypass status filter
- `Stop 5 - Tests/PR`: Added regression test and created draft PR for human review

## Impact

- App behavior: customers see only adoptable pets by default, even when empty status passed
- Tests: catalog tests cover empty status string and confirm pending pets excluded
- Humans: reviewers approve the product scope and merge decision

## Human Gates

- Scope approval: Jira issue and GitHub PR review
- Review approval: GitHub PR review by team member
- Merge approval: repository maintainers
- Deployment approval: operations team decides timing
