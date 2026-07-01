# Design: Fix Pending Pets Visible Bug

## Context

Customers are reporting that they can see and start adoption flows for pets that should not be available yet. This is causing confusion and creating extra work for operations staff.

## Problem

The `search_pets()` function in `app/petstore_app/catalog.py` has a bug in the status filtering logic at line 50:

```python
if normalized_status and normalized_status != pet.status:
    continue
```

When `status=""` (empty string) is passed, `normalized_status` becomes `""` which is falsy in Python. This causes the `if` condition to evaluate to `False`, skipping the status filter entirely and allowing pending pets to appear in results.

## Root Cause

The bug is that the condition checks truthiness of `normalized_status` before comparing it. An empty string is falsy, so the filter is not applied. However, the function has `status="available"` as the default, so in normal usage the filter should always be active.

## Evidence

- **Wiki**: `docs/wiki/petstore-catalog-availability.md` confirms default searches must show only `status="available"` pets
- **Logs**: `docs/logs/pending-pet-visible.ndjson` shows `PENDING_PET_VISIBLE` error code with `pet-103` (Nova) incorrectly visible
- **Code**: `app/petstore_app/catalog.py` line 50 has the flawed conditional
- **Tests**: Existing test `test_search_pets_filters_by_species_and_status` expects only available pets in default search

## Solution

Change line 50 from:
```python
if normalized_status and normalized_status != pet.status:
```

To:
```python
if normalized_status != pet.status:
```

This ensures the status filter is always applied when a status is provided (including the default "available" status).

## Why This Fix Is Safe

1. The function parameter has a default `status="available"`, so `normalized_status` will always be `"available"` unless explicitly overridden
2. The normalization at line 41 ensures `normalized_status` is always a lowercase string, never `None`
3. Existing tests verify that:
   - Default searches return only available pets
   - Explicit `status="pending"` searches still work
4. No API contract changes - the function signature remains identical
5. No database, schema, or deployment changes required

## Alternative Considered

We could have changed the normalization logic or added special handling for empty strings, but that would be more complex. The simplest fix is to remove the unnecessary truthiness check since the status parameter always has a value.

## Decision

Remove the truthiness check from the status filter condition. Change line 50 in `app/petstore_app/catalog.py` from `if normalized_status and normalized_status != pet.status:` to `if normalized_status != pet.status:`.

This ensures the status filter is always applied, respecting the default `status="available"` parameter while still allowing explicit pending searches.

## Risks

- **Low**: This is a one-line fix to restore intended behavior documented in the wiki
- **Testing coverage**: Existing tests already verify both default (available-only) and explicit pending searches
- **Backward compatibility**: No API changes; function signature unchanged
- **Deployment**: No configuration, schema, or infrastructure changes required
- **Rollback**: Simple one-line revert if needed

## Files Changed

- `app/petstore_app/catalog.py` - Fix status filter logic (1 line)
- `app/tests/test_pet_catalog.py` - Add regression test

## Validation Plan

1. Run existing unit tests to ensure no regressions
2. Add new test `test_default_search_excludes_pending_pets` to verify pending pets never appear in default results
3. Verify test passes with the fix
4. Manual smoke test: confirm default search returns only Scout, Mochi, Pip (not Nova)
