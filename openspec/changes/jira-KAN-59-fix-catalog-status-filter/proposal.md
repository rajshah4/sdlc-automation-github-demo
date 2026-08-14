# Change: Fix catalog status filter to exclude non-adoptable pets

## Why

Customers are seeing pets on the available pets page that they cannot adopt. The default pet search must return only pets with `status="available"`, but currently it returns pending pets when the status filter is bypassed.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-59
- Trigger: Jira issue created with label `basic-jira-pr`
- Automation: SDLC Automation Demo - Jira to PR

## Evidence Waypoints

- **Stop 1 - Ticket**: Jira KAN-59 reports "Available pets page shows animals customers cannot adopt"
- **Stop 2 - Wiki/Docs**: `docs/wiki/petstore-catalog-availability.md` confirms default search must show only `status="available"` pets
- **Stop 3 - Logs**: `docs/logs/pending-pet-visible.ndjson` shows `PENDING_PET_VISIBLE` error for pet-103 (Nova)
- **Stop 4 - Repo/Files**: `app/petstore_app/catalog.py` line 50 has faulty status filter logic
- **Stop 5 - Tests/PR**: Added regression test for empty status parameter

## Assumptions

- The bug is in `catalog.py` `search_pets()` function, not in the Cloud Run web layer
- The status filter logic incorrectly allows empty strings to bypass the filter
- Fixing the filter condition will restore correct behavior
- No schema, auth, or cloud resource changes are needed

## Non-Goals

- Not fixing the Cloud Run incident mode feature (that's a demo SRE tool)
- Not changing the UI or web frontend
- Not adding new catalog features
- Not modifying adoption or telemetry behavior

## What Changes

- Fix `search_pets()` status filter to properly handle empty status strings
- Ensure default behavior always filters to `status="available"`
- Add regression test to prevent future bypass of status filter

## Impact

- App behavior: Default catalog search will correctly return only available pets
- Tests: New regression test added for status filter edge case
- Humans: PR requires review approval before merge

## Human Gates

- Scope approval: Auto-approved for basic bug fix
- Review approval: Required
- Merge approval: Required
- Deployment approval: Required
