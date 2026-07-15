# Design

## Context

The Petstore catalog module (`app/petstore_app/catalog.py`) provides a `search_pets()` function that filters the pet catalog by various criteria including status, species, tags, and name query. The function accepts a `status` parameter with a default value of `"available"`.

The current implementation has a bug in the status filter logic at line 50:

```python
if normalized_status and normalized_status != pet.status:
    continue
```

This condition checks if `normalized_status` is truthy. When `status=""` (empty string) is passed explicitly, the condition evaluates to False because empty strings are falsy in Python. This causes the status filter to be skipped entirely, allowing pending pets to appear in results.

According to `docs/wiki/petstore-catalog-availability.md`:
- Default customer-facing catalog search must show only pets with `status="available"`
- Support and operations workflows may explicitly request `status="pending"`
- Nova (pet-103) has `status="pending"` and should not appear in default available-pets results

The log evidence in `docs/logs/pending-pet-visible.ndjson` shows error code `PENDING_PET_VISIBLE` indicating this regression occurred in the customer experience.

## Decision

**Change the status filter logic to enforce the default "available" status even when empty or falsy status values are provided.**

Replace the current line 50 condition:
```python
if normalized_status and normalized_status != pet.status:
```

With:
```python
if normalized_status != pet.status:
```

This ensures the status filter is always applied. Since `normalized_status` is set from `status.strip().lower()` and status has a default value of `"available"`, the filter will always compare against a valid status string.

**Alternative considered and rejected:** Adding explicit empty-string handling (`if status == "": status = "available"`) before normalization. This is more verbose and less direct than fixing the filter condition itself.

## Risks

- **Risk:** Breaking change if any existing code relies on passing `status=""` to bypass the status filter.
  - **Mitigation:** The existing test suite includes a test for explicit pending status search (`test_search_pets_can_find_pending_pets_when_requested`), which will continue to pass. Review logs and code for any legitimate use of empty-status bypass pattern; if found, document and handle explicitly.

- **Risk:** Other filter conditions may have similar truthy-check bugs.
  - **Mitigation:** Inspect other filter conditions (species, tag) for similar patterns. The `query` parameter intentionally allows empty strings (meaning "match all names"), so its truthy check is correct.

## Validation Plan

1. Run existing catalog tests to ensure no regressions:
   ```bash
   python -m pytest app/tests/test_pet_catalog.py -v
   ```

2. Add focused regression tests:
   - Test that default search excludes pending pets
   - Test that explicit empty-string status still applies available filter
   - Test that explicit pending status search still works

3. Verify the fix addresses the log evidence:
   - Confirm pet-103 (Nova) does not appear in `search_pets()` default results
   - Confirm pet-103 (Nova) does appear in `search_pets(status="pending")` results
