# Design

## Context

The Petstore demo has a static HTML/JS frontend (`app/web/`) and a Python backend (`app/petstore_app/catalog.py`). The backend `search_pets()` function correctly defaults to `status="available"`. The frontend contains a hardcoded pets array with Nova marked as `status="pending"`. The logs show `PENDING_PET_VISIBLE` error for pet-103 on 2026-06-29T12:00:00Z.

## Decision

- Refactor the frontend filter in `app/web/app.js` to check `pet.status !== "available"` first and return false immediately, making the availability requirement explicit
- Add `test_default_search_excludes_pending_pets()` regression test to verify Nova is excluded from default search results

## Risks

- **Risk**: Change might affect pending pet queries used by support workflows  
  **Mitigation**: Existing test `test_search_pets_can_find_pending_pets_when_requested()` verifies explicit `status="pending"` queries still work
- **Risk**: UI behavior might differ from backend behavior  
  **Mitigation**: Playwright tests verify UI and backend alignment

## Validation Plan

- Run `python3 -m pytest app/tests/test_pet_catalog.py -v` to verify all 6 tests pass including new regression test
- Run Playwright UI tests to verify Nova is not visible in default catalog view
- Verify logs no longer show `PENDING_PET_VISIBLE` errors after deployment
