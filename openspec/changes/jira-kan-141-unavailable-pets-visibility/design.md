# Design: Fix unavailable pets catalog visibility

## Context

The `search_pets()` function in `app/petstore_app/catalog.py` has a logic bug on line 50:

```python
if normalized_status and normalized_status != pet.status:
    continue
```

When `status=""` (empty string) is passed as a parameter:
1. `normalized_status = status.strip().lower()` results in `""`
2. Empty string is falsy in Python
3. The condition `if normalized_status and ...` evaluates to False
4. The status filter is completely skipped
5. ALL pets (including pending ones) are returned

This violates the product rule that "Default pet search returns only available pets" as documented in `docs/wiki/petstore-catalog-availability.md`.

## Decision

**Option A (Chosen):** Treat empty status as "available" (maintain safe default)

Change line 41 to handle empty status:
```python
normalized_status = (status.strip().lower() if status and status.strip() else "available")
```

This ensures:
- Empty string defaults to "available"
- None defaults to "available" (via the default parameter value)
- Explicit status values are honored

**Option B (Rejected):** Only filter when status is explicitly provided

This would require changing the status parameter default to `None` and conditionally applying the filter. Rejected because it complicates the API contract and makes the safe default less obvious.

## Risks

**Low risk change:**
- Single line modification to normalize empty strings to "available"
- Maintains existing API contract and default behavior
- Backward compatible - no breaking changes to callers
- Well-covered by existing tests plus new regression test

**Potential edge cases:**
- Whitespace-only strings (e.g., `"   "`) - handled by `.strip()` which converts them to empty string
- Case variations - handled by `.lower()` normalization
- None values - already handled by default parameter value `status="available"`

## Validation Plan

1. **Unit Tests**: Run `pytest app/tests/test_pet_catalog.py -v`
   - All existing tests must pass
   - New regression test must pass: `test_search_pets_empty_status_returns_only_available`

2. **Integration Verification**: Confirm all call patterns work correctly
   - `search_pets()` - defaults to available
   - `search_pets(status="")` - returns only available
   - `search_pets(status="available")` - returns available
   - `search_pets(status="pending")` - returns pending (for ops workflows)

3. **UI Test** (optional): Run Playwright test to confirm no UI regression
   - `node app/web/tests/catalog-search.playwright.mjs`

### Implementation Details

Files changed:
- `app/petstore_app/catalog.py` - Fix status normalization logic (1 line)
- `app/tests/test_pet_catalog.py` - Add regression test for empty status

Safety characteristics:
- Minimal, focused change (1 line of logic)
- Existing tests provide coverage for the happy path
- New test prevents regression
- No changes to data model, API surface, or UI behavior
- Change is backward compatible - callers already expect available pets by default
