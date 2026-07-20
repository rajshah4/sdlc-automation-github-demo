# Design

## Context

The Petstore catalog stores pet availability in the `status` field. Default search behavior should return available pets only, while explicit status searches can inspect pending pets for support or operational workflows.

The current bug exists in `app/petstore_app/catalog.py` at line 50:
```python
if normalized_status and normalized_status != pet.status:
    continue
```

When `status=""` is passed, `normalized_status` becomes an empty string, causing `if normalized_status` to evaluate to `False`, which skips the entire status filter. This allows all pets (including pending ones) to appear in results.

## Decision

- Change the status filter logic to treat empty or missing status as "available".
- Normalize the status parameter early: if empty after stripping, set it to "available".
- Preserve `status="available"` as the default parameter value.
- Ensure explicit `status="pending"` searches continue to work.
- Add regression coverage for empty status string and default behavior.

## Implementation

In `app/petstore_app/catalog.py`:

1. After stripping the status, check if it's empty and default to "available":
   ```python
   normalized_status = status.strip().lower()
   if not normalized_status:
       normalized_status = "available"
   ```

2. The existing filter logic at line 50 will then work correctly since `normalized_status` is always non-empty.

## Risks

- Minimal - the change ensures empty status always means "available", which matches the intent.
- Explicit `status="pending"` searches are preserved.
- No impact on other search parameters (species, tags, query).

## Validation Plan

- Add test case for `search_pets(status="")` to verify it excludes pending pets.
- Run existing catalog tests to ensure no regression.
- Verify explicit pending searches still work: `search_pets(status="pending")`.
- Run the full pytest suite before opening the PR.
