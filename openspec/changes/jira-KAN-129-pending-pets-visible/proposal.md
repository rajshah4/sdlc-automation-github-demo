# Change: Fix Pending Pets Visible in Default Search

## Why

Support reports that customers can see and start adoption flows for pets with `status="pending"` that should not be available yet. This creates customer confusion and operational overhead. The product rule states that default pet search must return only available pets.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-129
- Trigger: Jira webhook `jira:issue_created`
- Automation: SDLC Automation Demo - Jira Request To PR

## Evidence Waypoints

**Stop 1 - Ticket**: Jira KAN-129 reports customers seeing unavailable pets and creating operational overhead.

**Stop 2 - Wiki/Docs**: `docs/wiki/petstore-catalog-availability.md` confirms that default catalog search must show only `status="available"` pets. Pending pets should only appear when explicitly requested by support/operations workflows.

**Stop 3 - Logs**: `docs/logs/pending-pet-visible.ndjson` shows error code `PENDING_PET_VISIBLE` with `pending_pet_ids: ["pet-103"]` (Nova), confirming catalog availability regression.

**Stop 4 - Repo/Files**: `app/petstore_app/catalog.py` - The `search_pets()` function has a status filtering vulnerability: when an empty string is passed for the `status` parameter, the filter is bypassed entirely due to the condition `if normalized_status and normalized_status != pet.status:` treating empty string as falsy.

**Stop 5 - Tests/PR**: Added regression test to verify empty status defaults to "available". PR link to follow.

## Assumptions

- The only valid non-empty status values are "available" and "pending"
- Any empty, whitespace, or unspecified status should default to "available"
- Explicit `status="pending"` requests (for support/operations) must continue to work
- The root cause is in the backend catalog filter, not in the UI or adoption flow

## Non-Goals

- Adding new pet statuses (e.g., "adopted", "unavailable")
- Changing adoption flow logic
- Modifying UI behavior beyond fixing the underlying data filter
- Adding authentication or authorization checks
- Validating or restricting status values beyond empty string handling

## What Changes

- `app/petstore_app/catalog.py`: Modify status normalization to treat empty/whitespace status as "available"
- `app/tests/test_pet_catalog.py`: Add regression test for empty status string scenario

## Impact

- App behavior: Default pet search will correctly exclude pending pets when empty status is passed
- Tests: One new regression test added; all existing tests continue to pass
- Humans: Product owner approval of fix approach, code review, QA validation, merge approval, deployment authorization

## Human Gates

- Scope approval: Required before implementation
- Review approval: Required before merge
- Merge approval: Required before deployment
- Deployment approval: Required before production release
