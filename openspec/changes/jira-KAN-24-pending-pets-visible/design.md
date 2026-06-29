# Design

## Context

The Petstore catalog search function (`app/petstore_app/catalog.py::search_pets`) has a `status` parameter that defaults to `"available"`. The current implementation at line 50 uses:

```python
if normalized_status and normalized_status != pet.status:
    continue
```

This check allows empty status strings to bypass filtering entirely because an empty string is falsy in Python. When `normalized_status=""`, the condition `if normalized_status and ...` evaluates to `False`, skipping the status filter and returning all pets regardless of status.

Evidence shows Nova (pet-103) with `status="pending"` appearing in available-pet searches, correlating with the `PENDING_PET_VISIBLE` error code in `docs/logs/pending-pet-visible.ndjson`.

## Decision

- Change the status normalization logic (line 41) to treat empty or whitespace-only strings as `"available"`
- Remove the truthy check from the status filtering condition (line 50)
- This preserves the default behavior while closing the empty-string bypass
- No changes needed to function signature or other search parameters

## Risks

- Risk: Existing code may depend on empty status strings bypassing the filter
  - Mitigation: Static UI (`app/web/app.js`) already filters to available pets client-side; backend tests show explicit status values; no evidence of empty-status usage in the codebase
- Risk: Performance impact from additional string checks
  - Mitigation: Negligible - the `.strip()` operation is already present, we're just adding a fallback

## Validation Plan

- Add test for empty status string returning only available pets
- Add test for whitespace-only status string returning only available pets
- Add test for default search (no status param) returning only available pets
- Verify existing tests continue to pass (explicit status="pending" search)
- Run full test suite: `python3 -m pytest app/tests/test_pet_catalog.py -v`
