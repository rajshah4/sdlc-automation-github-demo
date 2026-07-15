# Change: Fix Pending Pets Visible in Available Catalog

## Why

Support reports that customers are seeing pets with "pending" status in the available-pets catalog. This creates confusion for customers and generates extra work for operations. The default catalog search must show only available pets.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-110
- Trigger: Replicated Jira delegated factory
- Automation: story-to-pr work cell

## Evidence Waypoints

**Stop 1 - Ticket**: Jira KAN-110 reports customers seeing pets that are not available.

**Stop 2 - Wiki/Docs**: `docs/wiki/petstore-catalog-availability.md` confirms default catalog search must show only `status="available"` pets. Nova (pet-103) has `status="pending"` and should not appear in default searches.

**Stop 3 - Logs**: `docs/logs/pending-pet-visible.ndjson` contains `PENDING_PET_VISIBLE` error code indicating pet-103 (Nova) appeared in available-pets experience.

**Stop 4 - Repo/Files**: `app/petstore_app/catalog.py` lines 50-51 contain the bug. The condition `if normalized_status and normalized_status != pet.status:` allows empty/whitespace status values to bypass the status filter entirely. When `status=""` or `status="  "` is passed, `normalized_status` becomes an empty string (falsy), causing the filter to be skipped.

**Stop 5 - Tests/PR**: Added focused test proving empty status bypasses filter. Fix removes the problematic `and normalized_status` check to ensure status filter always applies.

## Assumptions

- The bug manifests when code paths pass empty or whitespace-only status strings to `search_pets()`
- Removing the falsy check on `normalized_status` is safe because the default `status="available"` ensures a value is always present in normal usage
- Explicit pending pet searches (`status="pending"`) must continue to work for support/operations workflows

## Non-Goals

- UI changes to prevent empty status submission
- Schema validation for status values
- Adding authentication or authorization checks
- Changing pet data model or storage

## What Changes

- Remove `and normalized_status` from status filter condition in `search_pets()`
- The status filter will now always apply, preventing empty/whitespace status from bypassing the filter
- Add regression test proving empty status does not bypass the filter

## Impact

- App behavior: Default catalog searches will reliably show only available pets
- Tests: New regression test added to prevent future regressions
- Humans: Code review approval required before merge

## Human Gates

- Scope approval: Authorized by Jira ticket KAN-110
- Review approval: Required before merge
- Merge approval: Required
- Deployment approval: Standard deployment process
