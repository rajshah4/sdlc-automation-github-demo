# Design

## Context

In `app/petstore_app/catalog.py`, the `search_pets()` function has a default parameter `status: str = "available"` (line 31). Nova (pet-103) is defined with `status="pending"` (line 23). According to product rules in AGENTS.md and docs/wiki/petstore-catalog-availability.md, default searches must return only available pets, and pending pets should only appear when explicitly requested.

The bug occurs at line 50: `if normalized_status and normalized_status != pet.status:`. When an empty status is passed, `normalized_status.strip().lower()` returns `""`, which is falsy, causing the entire status filter to be skipped and allowing all pets (including pending) to pass through.

## Decision

- Change line 50 from `if normalized_status and normalized_status != pet.status:` to `if normalized_status != pet.status:`
- This ensures the status filter always applies when normalized_status has a value
- The default parameter `status="available"` will correctly filter out pending pets
- Explicit pending searches with `status="pending"` will continue to work as intended
- No changes to function signature, API contract, or other filter logic

## Risks

- Risk: Breaking explicit pending searches
  - Mitigation: Existing test `test_search_pets_can_find_pending_pets_when_requested` validates this behavior
- Risk: Breaking other status values if added in the future
  - Mitigation: Current codebase only uses "available" and "pending"; future status values would follow the same filter pattern
- Risk: Edge cases with whitespace or case variations
  - Mitigation: `normalized_status = status.strip().lower()` handles normalization correctly

## Validation Plan

- Run existing test suite to ensure no regressions
- Add `test_search_pets_excludes_pending_by_default()` to verify default behavior
- Add `test_search_pets_with_empty_status_excludes_pending()` to test edge case
- Verify Nova (pet-103) is excluded from default results
- Verify explicit `status="pending"` searches still return Nova
