# Change: Fix Pending Pets Appearing in Available Search

## Why

Support reports that customers are seeing and can start adoption flows for pets that should not be available yet (status="pending"). This creates customer confusion and operational burden. The default pet search must show only available pets, with pending pets visible only when explicitly requested by support or operations workflows.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-122
- Trigger: Jira issue created webhook
- Automation: jira-request-to-pr

## Evidence Trail

- **Stop 1 - Ticket**: KAN-122 "Customers are seeing pets that are not available" describes the symptom in business language
- **Stop 2 - Wiki/Docs**: `docs/wiki/petstore-catalog-availability.md` confirms default search must exclude pending pets; Nova (pet-103) is the known pending pet
- **Stop 3 - Logs**: `docs/logs/pending-pet-visible.ndjson` shows error code `PENDING_PET_VISIBLE` for pet-103 in the `petstore-web` component
- **Stop 4 - Repo/Files**: `app/petstore_app/catalog.py` line 41 and 50-51 contain the bug: when `status=""` is passed explicitly, the filter is bypassed due to falsy check
- **Stop 5 - Tests/PR**: Added regression test, fixed the filter logic, verified with pytest

## Assumptions

- The bug is in the Python backend `search_pets()` function, not the JavaScript UI
- Explicitly passing `status=""` (empty string) should default to "available" behavior, not bypass the filter
- Existing tests pass but do not cover the edge case of explicitly passing empty string
- The fix is safe: it only affects the empty-string edge case and preserves all other behavior
- No schema changes, auth changes, or new dependencies required

## Non-Goals

- Changing the UI search interface
- Modifying adoption order validation (already correct in `adoptions.py`)
- Adding new pet statuses beyond "available" and "pending"
- Changing how pending pets are requested by support workflows
- Deployment configuration or environment changes

## What Changes

- `app/petstore_app/catalog.py` line 41: ensure `normalized_status` defaults to "available" when status is empty or whitespace-only
- `app/tests/test_pet_catalog.py`: add regression test that verifies empty status string filters correctly

## Impact

- **App behavior**: Calling `search_pets(status="")` will now return only available pets instead of all pets
- **Tests**: New test `test_search_pets_defaults_to_available_when_status_is_empty` proves the fix
- **Humans**: PR requires review approval before merge; no deployment changes needed

## Human Gates

- Scope approval: ✓ (small backend filter fix)
- Review approval: required (PR must be reviewed before merge)
- Merge approval: required (no auto-merge)
- Deployment approval: required (humans control production changes)
