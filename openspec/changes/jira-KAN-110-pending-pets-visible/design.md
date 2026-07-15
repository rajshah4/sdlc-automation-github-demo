# Design: Fix Status Filter Bypass Bug

## Context

In `app/petstore_app/catalog.py` lines 50-51, the status filter uses:

```python
if normalized_status and normalized_status != pet.status:
    continue
```

The `and normalized_status` check treats empty string as falsy, allowing the filter to be skipped when `normalized_status` is empty. This happens when:
- A caller passes `status=""`
- A caller passes `status="  "` (whitespace only, becomes empty after `.strip()`)

This bug allows pending pets (like Nova, pet-103) to appear in catalog results when they should be filtered out. The logs confirm `PENDING_PET_VISIBLE` errors, and the wiki documents that only `status="available"` pets should appear in default searches.

## Decision

Remove the falsy check so the status filter always applies:

```python
if normalized_status != pet.status:
    continue
```

**Rationale:**
1. The default parameter `status: str = "available"` ensures normal callers get valid filtering
2. Empty status will now correctly filter to pets with empty status (none exist, so returns nothing)
3. Explicit pending searches (`status="pending"`) continue to work for operations
4. The fix is minimal, focused, and doesn't change the function signature

**Files Changed:**
- `app/petstore_app/catalog.py`: Remove `and normalized_status` from line 50
- `app/tests/test_pet_catalog.py`: Add regression test for empty status

## Risks

- **Low risk**: The change is minimal and well-tested
- **Backward compatibility**: Callers passing empty status will now get empty results instead of all pets, which is the correct behavior
- **Support workflows**: Explicit `status="pending"` searches remain fully functional
- **Validation**: Existing tests cover normal usage; new test covers the bug case

## Validation Plan

1. Run existing test suite to ensure no regressions
2. Run new regression test proving empty status doesn't bypass filter
3. Verify default search excludes pending pets (existing test coverage)
4. Verify explicit pending search still works for operations workflows
