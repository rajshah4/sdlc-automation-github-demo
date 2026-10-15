# Design

## Context

The Petstore demo has catalog search behavior in `app/petstore_app/catalog.py`:

- **Backend**: `search_pets()` function with default `status="available"` parameter (line 31).
- **Product rule**: Default pet search returns only available pets. Pending pets can be shown only when explicitly requested (per `docs/wiki/petstore-catalog-availability.md`).
- **Known fixture**: Nova is `pet-103` with `status="pending"` (catalog.py line 23).
- **Evidence**: `docs/logs/pending-pet-visible.ndjson` shows `PENDING_PET_VISIBLE` error with `pending_pet_ids: ["pet-103"]`.

## Investigation Findings

**Stop 1 - Ticket**: Jira KAN-239 reports customers seeing pets that should not be available yet.

**Stop 2 - Wiki/Docs**: `docs/wiki/petstore-catalog-availability.md` confirms "Default customer-facing catalog search must show only pets with status='available'" and "pending pets must not appear in the default available-pets experience."

**Stop 3 - Logs**: `docs/logs/pending-pet-visible.ndjson` shows error code `PENDING_PET_VISIBLE` with Nova (pet-103) appearing incorrectly.

**Stop 4 - Repo/Files**: 
- `app/petstore_app/catalog.py` line 50: Status filter has conditional `if normalized_status and normalized_status != pet.status`
- Line 41: `normalized_status = status.strip().lower()` - empty string after strip becomes falsy
- Bug: When `status=""` is passed, normalized_status is falsy, so line 50's condition short-circuits and status filter is bypassed
- Result: All pets including pending ones are returned

### Root Cause

The `search_pets` function allows bypassing the status filter when an empty status string is passed:

```python
# Line 41:
normalized_status = status.strip().lower()
# If status="", then normalized_status="" (falsy)

# Line 50:
if normalized_status and normalized_status != pet.status:
    continue
# The "normalized_status and" check allows skipping the filter when empty
```

## Decision

Fix line 41 to ensure empty strings default to "available":

```python
normalized_status = status.strip().lower() or "available"
```

This ensures:
- Empty strings default to "available" and filter is always applied
- Matches product requirements and default parameter intent
- Minimal change, no breaking API changes
- Aligns with wiki documentation

Alternative approaches considered and rejected:
1. Remove `normalized_status and` check - less explicit about intent
2. Raise ValueError for empty status - breaking change
3. Keep current behavior - violates product rules

## Risks

- **Regression**: Change is isolated to one line and covered by new test
- **Backward compatibility**: Empty string was allowing unfiltered results (bug), so fixing it corrects behavior rather than breaking it

## Validation Plan

- [x] Create OpenSpec change artifacts
- [ ] Validate artifacts with `validate_open_spec.py`
- [ ] Modify `catalog.py` line 41
- [ ] Add test `test_search_pets_defaults_empty_status_to_available()` in `test_pet_catalog.py`
- [ ] Run backend tests: `python3 -m pytest app/tests/test_pet_catalog.py`
- [ ] Verify new test fails before fix and passes after fix
