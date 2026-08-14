# Design

## Context

The Petstore catalog stores pet availability in the `status` field. Default search behavior must return available pets only, while explicit status searches can inspect pending pets for support or operational workflows.

The current `search_pets()` function in `app/petstore_app/catalog.py` has a subtle bug:
- Line 41 normalizes the status: `normalized_status = status.strip().lower()`
- Line 50 checks: `if normalized_status and normalized_status != pet.status:`

The problem: when `status=""` is passed (empty string), `normalized_status` becomes `""` which is falsy in Python, causing the `if normalized_status` check to fail and skip the status filter entirely. This allows pending pets to leak into results.

## Decision

Fix the normalization logic to treat empty or blank status values as the default "available" status:

```python
normalized_status = status.strip().lower() or "available"
```

This ensures:
- `status="available"` → `"available"` (normal case)
- `status=""` → `"available"` (empty string defaults to available)
- `status="  "` → `"available"` (blank string defaults to available)
- `status="pending"` → `"pending"` (explicit override works)

The fix is minimal, safe, and maintains backward compatibility for all valid use cases while closing the empty-string bypass.

## Alternative Considered

We could validate that status is non-empty and raise an error, but this would be a breaking change. The current function signature has `status: str = "available"`, indicating a default is intended. Normalizing empty strings to the default is the safer, more defensive approach.

## Risks

- Low risk: The change only affects the edge case where status is explicitly passed as an empty string, which is already a bug scenario.
- Explicit pending-pet searches (`status="pending"`) are preserved and will continue to work.
- All existing tests pass and cover the intended behavior.

## Validation Plan

- Add regression test: `test_search_pets_defaults_to_available_when_status_empty()` to prove empty status doesn't bypass the filter.
- Add regression test: `test_search_pets_excludes_pending_from_default_search()` to prove Nova (pet-103) stays out of default results.
- Run focused catalog tests: `python3 -m pytest app/tests/test_pet_catalog.py -v`
- Run full test suite: `python3 -m pytest -q`
- Document evidence and residual risk in the PR.
