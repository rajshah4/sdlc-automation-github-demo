# Design

## Context

The Petstore catalog search function `search_pets()` accepts an optional `status` parameter that defaults to `"available"`. The current implementation checks `if normalized_status and normalized_status != pet.status:` to filter by status. When an empty string is passed for status, it becomes falsy after normalization, causing the status filter to be completely skipped. This allows pending pets to appear in results that should be available-only.

Relevant evidence:
- Wiki: `docs/wiki/petstore-catalog-availability.md` specifies that default customer-facing searches must show only available pets.
- Log: `docs/logs/pending-pet-visible.ndjson` contains error code `PENDING_PET_VISIBLE` confirming the catalog availability regression.
- Code: `app/petstore_app/catalog.py` line 50 contains the buggy filter logic.
- Data: Nova (pet-103) has `status="pending"` and is incorrectly returned when `status=""`.

## Decision

- Normalize empty status strings to `"available"` before the filter logic runs.
- Change line 41 from `normalized_status = status.strip().lower()` to `normalized_status = status.strip().lower() or "available"`.
- This ensures the status filter is never bypassed and maintains backward compatibility with explicit status requests.

## Risks

- Risk: Breaking explicit `status=""` callers who expect all pets.
  - Mitigation: The product rule (per wiki) requires default searches to be available-only; returning all pets was never correct behavior. No known valid use case for `status=""` that differs from `status=None` or default.

- Risk: Performance impact from the additional normalization.
  - Mitigation: The change is a simple string operation; no measurable performance impact for catalog data of this size.

## Validation Plan

- Add test `test_search_pets_treats_empty_status_as_available()` that calls `search_pets(status="")` and verifies Nova is excluded.
- Run existing test suite to ensure no regressions: `pytest app/tests/test_pet_catalog.py -v`
- Verify the fix with direct Python REPL test: `search_pets(status="")` should return only available pets.
