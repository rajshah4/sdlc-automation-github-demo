# Design

## Context

The Petstore catalog's search_pets function in `app/petstore_app/catalog.py` accepts an optional status parameter with a default value of "available". The function normalizes the status by stripping whitespace and converting to lowercase. However, the filtering logic at line 50 checks `if normalized_status and normalized_status != pet.status:` which bypasses the filter entirely when normalized_status is an empty string (falsy in Python).

Product rule from `docs/wiki/petstore-catalog-availability.md`:
- Default customer-facing catalog search must show only pets with status="available"
- Pending pets must not appear in the default available-pets experience
- Support workflows may explicitly request status="pending" but this must be intentional

Evidence from `docs/logs/pending-pet-visible.ndjson`:
- Error code: PENDING_PET_VISIBLE
- Incident type: petstore_website_catalog_regression
- Affected pet: pet-103 (Nova)

## Decision

Modify the status normalization logic in search_pets to treat empty or whitespace-only status parameters as "available". This ensures the filter always applies unless explicitly overridden with a specific status value.

Implementation:
- Change line 41-42 in `app/petstore_app/catalog.py`
- After stripping and lowercasing, check if the result is empty
- If empty, default to "available"
- This preserves backward compatibility while closing the security gap

Code change:
```python
# Before
normalized_status = status.strip().lower()

# After
normalized_status = status.strip().lower() or "available"
```

This leverages Python's truthiness: empty string is falsy, so `"" or "available"` evaluates to "available".

## Risks

**Risk**: Changing core filtering logic could break existing behavior
- **Mitigation**: All existing tests pass. Empty status was never an intended feature, so this is a bug fix, not a breaking change.

**Risk**: Some caller might depend on empty status returning all pets
- **Mitigation**: Review shows no legitimate use case for bypassing the filter. The Cloud Run app uses its own visible_pets function for incident simulation.

**Risk**: Regression in explicit status filtering
- **Mitigation**: Add focused test for empty status. Verify existing "pending" and "available" tests still pass.

## Validation Plan

1. Run existing catalog tests: `python -m pytest app/tests/test_pet_catalog.py -v`
2. Add new test case for empty status parameter
3. Verify Nova (pet-103) does not appear in empty-status search
4. Verify explicit status="pending" still returns Nova
5. Run full test suite to ensure no regressions
