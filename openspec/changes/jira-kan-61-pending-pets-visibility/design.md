# Design

## Context

The Petstore catalog allows customers to search for adoptable pets. Product rules (AGENTS.md line 29-30) require that default pet search returns only pets with `status="available"`. Pending pets can be shown only when explicitly requested. Nova (pet-103) has `status="pending"` and must not appear in customer-facing default search results.

Evidence waypoints:
- **Stop 1 - Ticket**: KAN-61 reports "Customers are seeing pets that are not available" with Nova as the example
- **Stop 2 - Wiki/Docs**: `AGENTS.md` and `docs/wiki/petstore-catalog-availability.md` define the available-only rule and the `PENDING_PET_VISIBLE` error marker
- **Stop 3 - Logs**: `docs/logs/pending-pet-visible.ndjson` shows error event from 2026-06-29 with `pending_pet_ids:["pet-103"]` visible in `operation:"web.available_pets"`
- **Stop 4 - Repo/Files**: Both backend (`app/petstore_app/catalog.py` line 50) and frontend (`app/web/app.js` line 17) implement correct status filters
- **Stop 5 - Tests/PR**: Existing tests implicitly validate behavior but lack explicit Nova-exclusion regression coverage

## Decision

- Add explicit regression test `test_default_search_excludes_pending_pets()` to `app/tests/test_pet_catalog.py`
- Test calls `search_pets()` with no status parameter (uses default `status="available"`)
- Assert pet-103 (Nova) is NOT in results
- Assert all results have `status="available"`
- Use `PENDING_PET_VISIBLE` in assertion messages to match error code from logs
- No code changes to catalog.py or app.js needed—filter logic is already correct

## Risks

- **Low risk**: Test-only change with no behavior modification
- **Mitigation**: Run all existing catalog tests to ensure no regressions
- **Monitoring**: `PENDING_PET_VISIBLE` error marker aligns with observability pattern

## Validation Plan

Run backend tests:
```bash
cd /workspace/project/sdlc-automation-github-demo
python3 -m pytest app/tests/test_pet_catalog.py -v
```

Expected: All 6 tests pass, including new `test_default_search_excludes_pending_pets`

Optional frontend validation: The existing Playwright test already validates default view excludes Nova (line 154) and searching for "nova" shows empty state (lines 171-176).
