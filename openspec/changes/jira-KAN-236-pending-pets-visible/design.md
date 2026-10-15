# Design

## Context

The petstore catalog maintains a list of pets with various statuses: "available" for pets ready for adoption, and "pending" for pets in training or processing. The `search_pets()` function in `catalog.py` filters pets by multiple criteria including status.

The current implementation has a bug in line 50-51:
```python
if normalized_status and normalized_status != pet.status:
    continue
```

The `if normalized_status` condition causes the status filter to be skipped when `normalized_status` is an empty string. This allows pending pets to leak into results that should be available-only.

## Decision

- Remove the `and normalized_status` condition from the status filter check
- The status filter will be enforced unconditionally, using the default value "available" when not specified
- If an empty string is somehow passed, no pets will match (correct behavior)
- This is a one-line change with zero backward-compatibility risk for valid callers

## Evidence Waypoints

- **Stop 1 - Ticket**: Jira KAN-236 reports customers seeing pets that should not be available
- **Stop 2 - Wiki/Docs**: `docs/wiki/petstore-catalog-availability.md` confirms default search must show only available pets; Nova (pet-103) is pending
- **Stop 3 - Logs**: `docs/logs/pending-pet-visible.ndjson` shows `PENDING_PET_VISIBLE` error with pet-103 leaking into available results
- **Stop 4 - Repo/Files**: `app/petstore_app/catalog.py` line 50 has the buggy conditional; existing tests verify explicit pending searches work
- **Stop 5 - Tests/PR**: Add regression test, fix the filter, validate all tests pass, open draft PR

## Risks

- **Backward compatibility**: No risk. Valid callers already pass explicit status values or use the default. Empty-string status is not a documented or tested use case.
- **Test coverage**: Existing tests verify the happy paths; we're adding a regression test for the empty-status edge case.
- **Pending pet access**: No risk. Explicit `status="pending"` searches for support workflows continue working unchanged.

## Validation Plan

- Add test: `test_search_pets_with_empty_status_returns_no_results()`
- Run: `pytest app/tests/test_pet_catalog.py -v`
- Verify: All tests pass including the new regression test
- Expected: 5 passing tests (4 existing + 1 new)
