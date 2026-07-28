# Design

## Context

The Petstore catalog stores pet availability in the `status` field. Default search behavior should return available pets only, while explicit status searches can inspect pending pets for support or operational workflows.

The current implementation has a bug where passing an empty string for the status parameter bypasses the status filter entirely. Line 41 normalizes the status with `normalized_status = status.strip().lower()`, and line 50 checks `if normalized_status and normalized_status != pet.status:`. When status is an empty string, normalized_status is falsy, causing the entire status filter to be skipped.

## Decision

- Modify status normalization to default empty strings to "available"
- Remove the conditional check that allows bypassing the status filter
- Preserve `status="available"` as the default when no parameter is passed
- Preserve explicit `status="pending"` searches for support workflows
- Add regression test for empty status string behavior

### Implementation Changes

File: `app/petstore_app/catalog.py`

1. Line 41: Change from `normalized_status = status.strip().lower()` to `normalized_status = status.strip().lower() if status.strip() else "available"`
2. Line 50: Change from `if normalized_status and normalized_status != pet.status:` to `if normalized_status != pet.status:`

### Test Coverage

Add `test_search_pets_with_empty_status_defaults_to_available()` to verify empty strings default to showing only available pets and exclude Nova (pet-103).

## Risks

- A broad fix could hide pending pets from support workflows that explicitly request them.
  - Mitigation: Explicit `status="pending"` searches are preserved and tested.
- Existing code that relies on empty-string bypass behavior would break.
  - Mitigation: No legitimate use case should rely on empty string showing all pets; product requirement is default-to-available.

## Validation Plan

- Run focused catalog tests: `pytest app/tests/test_pet_catalog.py`
- Verify new test passes: `test_search_pets_with_empty_status_defaults_to_available`
- Verify existing tests still pass: `test_search_pets_can_find_pending_pets_when_requested`
- Run full test suite before opening PR
