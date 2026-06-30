# Design

## Context

The `search_pets` function in `app/petstore_app/catalog.py` has a parameter `status: str = "available"`, but the filtering logic at line 50 uses:

```python
if normalized_status and normalized_status != pet.status:
    continue
```

The `and` condition means when `normalized_status` is an empty string (after stripping), the status filter is skipped entirely, allowing pending pets through.

Line 41 normalizes the status: `normalized_status = status.strip().lower()`

When `status=""` is passed (empty string), `normalized_status` becomes `""`, which is falsy. The condition `if normalized_status and ...` short-circuits, bypassing the status filter.

## Decision

Fix the filter logic at line 50 by removing the `and normalized_status` check to always apply the status filter:

```python
# Before:
if normalized_status and normalized_status != pet.status:
    continue

# After:
if normalized_status != pet.status:
    continue
```

This ensures the status filter is always applied when a status value is provided (including the default `"available"`).

Alternative approaches considered:
- Guard at function entry to reject empty status strings (rejected: overly defensive)
- Explicit default assignment for empty status (rejected: default parameter already handles this)
- Change default to None (rejected: changes API signature unnecessarily)

## Risks

- Risk: Single-line change in well-tested module
- Mitigation: Existing tests for explicit pending searches ensure we don't break operations workflows
- Risk: No external dependencies or API changes
- Mitigation: Backward compatible with all existing explicit status queries

## Validation Plan

1. Run existing test suite to ensure no regressions
2. Add focused regression test `test_search_pets_excludes_pending_by_default`
3. Verify existing test `test_search_pets_filters_by_species_and_status` now passes correctly
