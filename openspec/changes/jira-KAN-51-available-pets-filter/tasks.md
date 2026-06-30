# Tasks

## Implementation

- [x] Create OpenSpec change folder
- [x] Write proposal with evidence waypoints
- [x] Write design with root cause analysis
- [ ] Fix status filter bug in `app/petstore_app/catalog.py`
- [ ] Add regression test to `app/tests/test_pet_catalog.py`
- [ ] Run catalog tests to verify fix
- [ ] Create GitHub PR with KAN-51 reference
- [ ] Add `openhands-qa` label to PR

## Human Gates

- [ ] Human review of PR
- [ ] Human approval to merge
- [ ] Human verification in production

## Evidence Waypoints

- **Stop 1 - Ticket**: KAN-51 reports pets that cannot be adopted are showing in available list
- **Stop 2 - Wiki/Docs**: `docs/wiki/petstore-catalog-availability.md` confirms default search must show only `status="available"`
- **Stop 3 - Logs**: `docs/logs/pending-pet-visible.ndjson` shows `PENDING_PET_VISIBLE` error with `pet-103` (Nova)
- **Stop 4 - Repo/Files**: `app/petstore_app/catalog.py` line 50 has the bug - empty string status skips the filter
- **Stop 5 - Tests/PR**: Will add regression test and create PR
