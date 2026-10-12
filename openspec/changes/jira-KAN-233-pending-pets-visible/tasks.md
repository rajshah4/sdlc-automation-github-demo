# Tasks

## Implementation

- [x] Review issue description and acceptance criteria
- [x] Check wiki docs (`docs/wiki/petstore-catalog-availability.md`)
- [x] Review log evidence (`docs/logs/pending-pet-visible.ndjson`)
- [x] Identify root cause in `app/petstore_app/catalog.py`
- [ ] Fix status filter logic in `catalog.py` line 50
- [ ] Add regression test for default available-only behavior
- [ ] Run test suite and verify all tests pass

## Validation

- [ ] Verify `test_search_pets_filters_by_species_and_status` still passes
- [ ] Verify `test_search_pets_can_find_pending_pets_when_requested` still passes
- [ ] New test proves pending pets excluded from default search
- [ ] Run `pytest app/tests/test_pet_catalog.py -v`

## Delivery

- [ ] Create feature branch
- [ ] Commit changes with clear message
- [ ] Push branch to remote
- [ ] Open draft PR with evidence waypoints
- [ ] Add `openhands-review` label to PR
- [ ] Post Jira comment with PR link and validation results

## Human Gates

- [ ] Human review of PR
- [ ] Human approval of merge
- [ ] Human decision on deployment timing
