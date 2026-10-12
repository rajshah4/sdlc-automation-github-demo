# Evidence Checklist

## Stop 1 - Ticket

**Source**: [KAN-233](https://rajiv-shah.atlassian.net/browse/KAN-233)

**Summary**: Customers are seeing pets that are not available

**Description**: Support reports that some customers are able to see and start adoption flows for pets that should not be available yet. This is confusing customers and creating extra work for operations.

**Business Language Clues**:
- "seeing pets that are not available" → catalog filtering issue
- "start adoption flows" → impacts customer-facing experience
- "confusing customers" → production visibility bug

## Stop 2 - Wiki/Docs

**Checked**: `docs/wiki/petstore-catalog-availability.md`

**Key Rules Found**:
- Default customer-facing catalog search must show only `status="available"` pets
- Support/operations may explicitly request `status="pending"`
- Nova is `pet-103` with `status="pending"`
- `PENDING_PET_VISIBLE` log indicates catalog regression

**Relevance**: Confirms this is a known product rule violation

## Stop 3 - Logs

**Checked**: `docs/logs/pending-pet-visible.ndjson`

**Evidence Found**:
```json
{
  "error_code": "PENDING_PET_VISIBLE",
  "bug_signal": {"type": "catalog_availability_regression", "safe_to_fix": true},
  "pending_pet_ids": ["pet-103"],
  "customer_impact": "Pending pets were visible in the available-pets experience."
}
```

**Relevance**: Confirms pet-103 (Nova) appeared in available-pets results, validating the bug report

## Stop 4 - Repo/Files

**Root Cause File**: `app/petstore_app/catalog.py`

**Problem Location**: Line 50

**Current Code**:
```python
if normalized_status and normalized_status != pet.status:
    continue
```

**Issue**: The truthy check `if normalized_status` allows empty strings to bypass the filter

**Test File**: `app/tests/test_pet_catalog.py`

**Existing Coverage**:
- ✅ Species + status filtering works
- ✅ Explicit `status="pending"` search works  
- ✅ Tag filtering works
- ❌ Missing: Default search excluding pending pets
- ❌ Missing: Empty status string handling

## Stop 5 - Tests/PR

**Tests Added**: 
- `test_default_search_excludes_pending_pets` (new regression test)
- Verifies that `search_pets()` without explicit status returns only available pets

**Validation Plan**:
1. Run `pytest app/tests/test_pet_catalog.py -v`
2. Verify all existing tests pass
3. Verify new regression test passes

**PR Link**: [To be created after implementation]
