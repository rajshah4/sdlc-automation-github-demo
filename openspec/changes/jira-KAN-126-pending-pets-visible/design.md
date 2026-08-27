# Design

## Context

The `search_pets()` function in `app/petstore_app/catalog.py` has a default parameter `status: str = "available"`. However, when callers pass an empty string or whitespace-only status, the normalization step `status.strip().lower()` produces an empty string, which is falsy, causing the status filter check `if normalized_status and normalized_status != pet.status` to be skipped entirely.

**Evidence Waypoints:**
- Stop 1 - Ticket: Jira KAN-126 reports customers seeing unavailable pets
- Stop 2 - Wiki/Docs: `docs/wiki/petstore-catalog-availability.md` confirms default search must be available-only
- Stop 3 - Logs: `docs/logs/pending-pet-visible.ndjson` shows `PENDING_PET_VISIBLE` error for `pet-103` (Nova)
- Stop 4 - Repo/Files: `app/petstore_app/catalog.py` lines 41 and 50-51 show the empty-string bypass

## Decision

- Change line 41 in `app/petstore_app/catalog.py` from `normalized_status = status.strip().lower()` to `normalized_status = (status.strip().lower() or "available")`
- This ensures empty or whitespace status parameters default to "available"
- Default `status="available"` works as before
- Empty string `status=""` becomes `"available"`
- Whitespace `status="  "` becomes `"available"`
- Explicit `status="pending"` still works for support queries

## Risks

- Callers currently relying on `status=""` to see all pets will now see only available pets. This is the correct behavior per requirements, so any such callers are buggy and this fix corrects them. Risk: Low

## Validation Plan

- Add regression test: `test_search_pets_treats_empty_status_as_available()` to verify empty status excludes pending pets
- Add edge case test: `test_search_pets_treats_whitespace_status_as_available()` to verify whitespace handling
- Run full test suite with `pytest app/tests/test_pet_catalog.py -v`
- Verify existing tests still pass (especially `test_search_pets_can_find_pending_pets_when_requested`)
