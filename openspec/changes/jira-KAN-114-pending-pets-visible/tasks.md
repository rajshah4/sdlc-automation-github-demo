# Tasks

- [x] Review wiki documentation at `docs/wiki/petstore-catalog-availability.md`
- [x] Review error logs at `docs/logs/pending-pet-visible.ndjson`
- [x] Identify root cause in `app/petstore_app/catalog.py`
- [x] Create OpenSpec-style change folder with proposal, design, spec, and tasks
- [x] Validate OpenSpec structure
- [ ] Update `search_pets()` to normalize empty status to "available"
- [ ] Add regression test for empty status string
- [ ] Run focused validation: `pytest app/tests/test_pet_catalog.py -v`
- [ ] Verify fix with REPL test
- [ ] Open draft PR with evidence waypoints
- [ ] Add `openhands-qa` label to PR for automated QA validation
