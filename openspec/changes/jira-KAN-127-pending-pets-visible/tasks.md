# Tasks

- [x] Create OpenSpec-style change artifacts (proposal, spec, design, tasks)
- [x] Validate change folder structure
- [ ] Fix `app/petstore_app/catalog.py` to properly enforce status filtering
- [ ] Add regression tests to `app/tests/test_pet_catalog.py`
- [ ] Run existing tests to verify no regressions
- [ ] Run full test suite
- [ ] Create draft PR with evidence waypoints
- [ ] Post status update to Jira KAN-127

## Evidence Waypoints

- **Stop 1 - Ticket**: Jira KAN-127 "Customers are seeing pets that are not available" - business language report from support
- **Stop 2 - Wiki/Docs**: `docs/wiki/petstore-catalog-availability.md` confirms default search must exclude pending pets; Nova (pet-103) has status="pending"
- **Stop 3 - Logs**: `docs/logs/pending-pet-visible.ndjson` shows error code `PENDING_PET_VISIBLE` with pet-103 in available-pets experience
- **Stop 4 - Repo/Files**: `app/petstore_app/catalog.py` line 50 has bug - `if normalized_status and normalized_status != pet.status` allows empty status bypass
- **Stop 5 - Tests/PR**: Add regression tests, validate fix, create draft PR

## Implementation Notes

The bug is in the status filter condition at line 50 of `catalog.py`. The check `if normalized_status and ...` allows empty strings to bypass filtering. Fix: ensure status always defaults to "available" and always apply the filter.
