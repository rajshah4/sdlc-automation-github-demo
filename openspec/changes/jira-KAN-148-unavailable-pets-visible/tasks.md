# Tasks

- [x] Review Jira issue KAN-148 and understand business impact
- [x] Check wiki documentation (`docs/wiki/petstore-catalog-availability.md`)
- [x] Review log evidence (`docs/logs/pending-pet-visible.ndjson` - error code `PENDING_PET_VISIBLE`)
- [x] Analyze catalog backend (`app/petstore_app/catalog.py`) - confirmed correct
- [x] Analyze web frontend (`app/web/app.js`) - identified filtering logic
- [x] Create OpenSpec-style change folder and artifacts
- [ ] Implement frontend fix to strengthen availability filtering
- [ ] Add regression test to validate pending pets excluded from default results
- [ ] Run focused catalog tests (`pytest app/tests/test_pet_catalog.py -v`)
- [ ] Verify fix manually by opening web UI and confirming Nova not visible
- [ ] Run full test suite (`pytest app/tests/ -v`)
- [ ] Create draft PR with evidence waypoints and validation results
- [ ] Add `openhands-review` label to PR for code review work cell
- [ ] Post status update to Jira KAN-148 with PR link
