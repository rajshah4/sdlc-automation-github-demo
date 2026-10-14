# Design

## Context

The Petstore catalog module (`app/petstore_app/catalog.py`) provides a `search_pets` function with a default `status="available"` parameter. The current implementation checks `if normalized_status and normalized_status != pet.status:` which fails when an empty string is passed because empty strings are falsy in Python. This allows pending pets to appear in results when they should be filtered out.

The product rule explicitly states: "Default pet search returns only available pets. Pending pets can be shown only when explicitly requested and cannot be adopted."

Evidence from `docs/logs/pending-pet-visible.ndjson` shows error code `PENDING_PET_VISIBLE` confirming pet-103 (Nova) appeared in the available-pets experience.

## Decision

- Change the status filter condition from `if normalized_status and normalized_status != pet.status:` to `if normalized_status != pet.status:`
- This ensures the filter is applied even when `normalized_status` is an empty string
- The default parameter value remains `status="available"` so existing callers are unaffected
- Explicit `status="pending"` searches continue to work for operations workflows

## Risks

- Low risk: The change is a one-line fix to a boolean condition
- Existing tests verify that explicit pending searches work; they should continue to pass
- The fix makes the behavior match the documented product rule

## Validation Plan

- Add regression test: `test_search_pets_excludes_pending_by_default_even_with_empty_status`
- Run existing test suite: `pytest app/tests/test_pet_catalog.py -v`
- Verify Nova (pet-103) does not appear in default species="dog" searches
- Verify explicit status="pending" searches still return Nova
