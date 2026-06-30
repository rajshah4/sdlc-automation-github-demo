# Design

## Context

The Petstore catalog stores pet availability in the `status` field. Default search behavior should return available pets only, while explicit status searches can inspect pending pets for support or operational workflows.

The `search_pets()` function in `app/petstore_app/catalog.py` has a logic bug at line 50 where the status filter uses `if normalized_status and normalized_status != pet.status:`. When `status` is passed as an empty string or whitespace, `normalized_status` becomes an empty string after `.strip().lower()`. An empty string evaluates to `False` in a boolean context, so the entire status filter is skipped, causing all pets to be returned regardless of status.

## Decision

- Change line 50 from `if normalized_status and normalized_status != pet.status:` to `if normalized_status != pet.status:`
- Add regression test `test_search_pets_default_status_excludes_pending()` to verify default search excludes Nova (pet-103)
- Preserve explicit `status="pending"` searches for support workflows
- Run focused catalog tests before opening PR

## Risks

- A broad fix could hide pending pets from support workflows that explicitly request them - mitigated by keeping the explicit status parameter path unchanged
- Other callers might be passing empty status strings - mitigated by the function's default parameter of `status="available"`

## Validation Plan

- Run `python -m pytest app/tests/test_pet_catalog.py -v` to verify all catalog tests pass
- Verify existing test `test_search_pets_can_find_pending_pets_when_requested` still passes (confirms explicit pending searches work)
- Verify new test `test_search_pets_default_status_excludes_pending` passes (confirms the bug is fixed)
